"""LangGraph variant of the research orchestrator.

Requires: pip install langgraph langchain-core
"""

from __future__ import annotations

from typing import Any, TypedDict

try:
    from langgraph.graph import StateGraph, END
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False


class ResearchState(TypedDict, total=False):
    query: str
    plan: list[dict]
    findings: list[dict]
    draft: dict
    critique: dict
    report: dict
    verification: dict
    status: str


def build_graph(orchestrator: Any):
    if not HAS_LANGGRAPH:
        raise ImportError("langgraph is not installed. pip install langgraph")

    def plan_node(state: ResearchState) -> ResearchState:
        tasks = orchestrator.plan(state["query"])
        return {"plan": [{"id": t.id, "description": t.description, "owner": t.owner} for t in tasks]}

    def research_node(state: ResearchState) -> ResearchState:
        findings = []
        for p in state.get("plan", []):
            out = orchestrator.researcher.run({"description": p["description"]})
            findings.append(out)
        return {"findings": findings}

    def synthesize_node(state: ResearchState) -> ResearchState:
        draft = orchestrator.synthesizer.run({
            "query": state["query"],
            "findings": state.get("findings", []),
        })
        return {"draft": draft}

    def critique_node(state: ResearchState) -> ResearchState:
        critique = orchestrator.skeptic.run(state.get("draft", {}))
        return {"critique": critique}

    def revise_node(state: ResearchState) -> ResearchState:
        report = orchestrator.synthesizer.run({
            "query": state["query"],
            "findings": state.get("findings", []),
            "critique": state.get("critique"),
            "mode": "revise",
        })
        return {"report": report}

    def verify_node(state: ResearchState) -> ResearchState:
        v = orchestrator.verifier.run(state.get("report", {}))
        status = "verified" if v.get("verified") else "unverified"
        return {"verification": v, "status": status}

    g = StateGraph(ResearchState)
    g.add_node("plan", plan_node)
    g.add_node("research", research_node)
    g.add_node("synthesize", synthesize_node)
    g.add_node("critique", critique_node)
    g.add_node("revise", revise_node)
    g.add_node("verify", verify_node)

    g.set_entry_point("plan")
    g.add_edge("plan", "research")
    g.add_edge("research", "synthesize")
    g.add_edge("synthesize", "critique")
    g.add_edge("critique", "revise")
    g.add_edge("revise", "verify")
    g.add_edge("verify", END)

    return g.compile()
