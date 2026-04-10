"""
LangGraph Graph Definition — wires nodes and transitions into the full pipeline.
"""
from langgraph.graph import StateGraph, END

from app.orchestration.state import JobAgentState
from app.orchestration.nodes import (
    node_load_profile,
    node_generate_resume,
    node_score_ats,
    node_hunt_jobs,
    node_rank_jobs,
    node_auto_apply,
    node_notify,
)
from app.orchestration.transitions import (
    should_generate_resume,
    should_score_ats,
    should_hunt_jobs,
    should_rank,
    should_apply,
)


def build_graph() -> StateGraph:
    """
    Build and compile the JOBAGENT LangGraph pipeline.

    Flow:
      load_profile
        → generate_resume
          → score_ats
            → hunt_jobs
              → rank_jobs
                → auto_apply
                  → notify
                    → END
    """
    graph = StateGraph(JobAgentState)

    # ─── Register nodes ───────────────────────────────────────────────────────
    graph.add_node("load_profile", node_load_profile)
    graph.add_node("generate_resume", node_generate_resume)
    graph.add_node("score_ats", node_score_ats)
    graph.add_node("hunt_jobs", node_hunt_jobs)
    graph.add_node("rank_jobs", node_rank_jobs)
    graph.add_node("auto_apply", node_auto_apply)
    graph.add_node("notify", node_notify)

    # ─── Set entry point ───────────────────────────────────────────────────────
    graph.set_entry_point("load_profile")

    # ─── Edges ─────────────────────────────────────────────────────────────────
    graph.add_conditional_edges("load_profile", should_generate_resume, {
        "generate_resume": "generate_resume",
        "error": END,
    })
    graph.add_conditional_edges("generate_resume", should_score_ats, {
        "score_ats": "score_ats",
        "error": END,
    })
    graph.add_conditional_edges("score_ats", should_hunt_jobs, {
        "hunt_jobs": "hunt_jobs",
        "error": END,
    })
    graph.add_conditional_edges("hunt_jobs", should_rank, {
        "rank_jobs": "rank_jobs",
        "notify": "notify",
    })
    graph.add_conditional_edges("rank_jobs", should_apply, {
        "auto_apply": "auto_apply",
        "notify": "notify",
    })
    graph.add_edge("auto_apply", "notify")
    graph.add_edge("notify", END)

    return graph.compile()


# Singleton compiled graph
jobagent_graph = build_graph()
