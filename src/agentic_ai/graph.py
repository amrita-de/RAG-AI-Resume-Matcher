"""Phase 3 & 4: LangGraph Orchestration Workflows.

Phase 3 (original): Wraps the modular Phase 2 tools into an autonomous state machine.
Phase 4 (new): Adds RAG-enhanced retrieval and Human-in-the-Loop approval nodes.

Three workflow variants are available:
1. compile_workflow()      — Original Phase 3 pipeline (backward compatible)
2. compile_rag_workflow()  — Phase 4 RAG-enhanced pipeline with context retrieval
3. compile_hitl_workflow() — Phase 4 full pipeline with RAG + Human-in-the-Loop approval
"""

from typing import TypedDict, Optional, Dict, Any, List
from langgraph.graph import StateGraph, START, END

from agentic_ai.tools import extract_skills, compute_match_score, suggest_rewrite
from agentic_ai.tool_schemas import RewriteOutput, RewrittenBullet


# ─────────────────────────────────────────────────────────
# 1. State Definition
# ─────────────────────────────────────────────────────────
class AgentState(TypedDict):
    """The central state object passed between LangGraph nodes."""
    # Inputs
    resume_text: str
    jd_text: str
    target_role: str
    
    # Intermediate Extraction
    resume_skills: Optional[Dict[str, Any]]
    jd_skills: Optional[Dict[str, Any]]
    
    # Analysis & Outputs
    match_results: Optional[Dict[str, Any]]
    rewrites: Optional[Dict[str, Any]]
    final_report: Optional[Dict[str, Any]]

    # Phase 4: RAG Context
    rag_context: Optional[Dict[str, Any]]

    # Phase 4: Human-in-the-Loop
    human_approval: Optional[str]       # "approved" / "rejected" / "edited"
    human_feedback: Optional[str]       # reviewer comments
    reviewed_rewrites: Optional[Dict[str, Any]]  # edited rewrites from reviewer


# ─────────────────────────────────────────────────────────
# 2. Node Functions (Phase 3 — Original)
# ─────────────────────────────────────────────────────────
def extract_resume_node(state: AgentState) -> dict:
    """Extract skills from the resume text."""
    skills = extract_skills.invoke({
        "text": state["resume_text"],
        "source_type": "resume"
    })
    return {"resume_skills": skills}


def extract_jd_node(state: AgentState) -> dict:
    """Extract skills from the job description text."""
    skills = extract_skills.invoke({
        "text": state["jd_text"],
        "source_type": "job_description"
    })
    return {"jd_skills": skills}


def compute_score_node(state: AgentState) -> dict:
    """Compute the candidate match score by comparing extracted skills."""
    if not state.get("resume_skills") or not state.get("jd_skills"):
        raise ValueError("Skills must be extracted before scoring.")
        
    score_res = compute_match_score.invoke({
        "resume_skills": state["resume_skills"],
        "jd_skills": state["jd_skills"],
        "resume_text": state["resume_text"],
        "jd_text": state["jd_text"],
    })
    return {"match_results": score_res}


def optimize_bullets_node(state: AgentState) -> dict:
    """Rewrite weak resume bullets if impact score is less than perfect."""
    # Extract naive bullets for rewriting based on text structure or pass dummy ones 
    # if we haven't built a bullet extractor. In a full system, a bullet extractor tool would precede this.
    # We will use some simulated extraction or hardcoded bullets for demonstration of the orchestration.
    
    # Find bullet-like lines from the resume text heuristically for optimization
    lines = state["resume_text"].split("\n")
    potential_bullets = [line.strip() for line in lines if line.strip().startswith("-") or line.strip().startswith("•") or len(line.strip()) > 60]
    
    # Fallback if no bullets identified
    if not potential_bullets:
        potential_bullets = [
            "Developed software features using standard tools.",
            "Managed databases and deployed code to production."
        ]
        
    # Pick top 3 bullets for rewriting to save context length
    selected_bullets = potential_bullets[:3]
    
    missing = state["match_results"].get("missing_critical", []) if state.get("match_results") else []
    
    # Build invoke args — include RAG context if available (Phase 4)
    invoke_args = {
        "bullet_points": selected_bullets,
        "target_role": state["target_role"],
        "missing_skills": missing,
    }
    
    # Add RAG context if present in state
    rag_context = state.get("rag_context")
    if rag_context:
        invoke_args["rag_context"] = rag_context
    
    rewrites = suggest_rewrite.invoke(invoke_args)
    return {"rewrites": rewrites}


def aggregate_report_node(state: AgentState) -> dict:
    """Compile all intermediate results into the final output format."""
    # Use reviewed rewrites (from HITL) if available, otherwise original rewrites
    final_rewrites = state.get("reviewed_rewrites") or state.get("rewrites")
    
    report = {
        "status": "success",
        "target_role": state["target_role"],
        "match_results": state.get("match_results"),
        "rewrites": final_rewrites,
    }
    
    # Include HITL metadata if present
    if state.get("human_approval"):
        report["human_review"] = {
            "approval": state["human_approval"],
            "feedback": state.get("human_feedback"),
        }
    
    # Include RAG metadata if present
    if state.get("rag_context"):
        report["rag_enhanced"] = True
    
    return {"final_report": report}


# ─────────────────────────────────────────────────────────
# 3. Phase 4 Node Functions — RAG & HITL
# ─────────────────────────────────────────────────────────

def retrieve_context_node(state: AgentState) -> dict:
    """Retrieve relevant best practice examples from the RAG index to ground rewrites.
    
    This node runs after skill extraction and before scoring/rewriting.
    It queries the FAISS best practices index with the target role context.
    """
    from agentic_ai.rag import retrieve_rewrite_context
    
    # Use a representative bullet from the resume for context-aware retrieval
    lines = state["resume_text"].split("\n")
    sample_bullets = [
        line.strip() for line in lines
        if line.strip().startswith("-") or line.strip().startswith("•")
    ]
    
    # Use the first bullet as the retrieval query, or the target role
    query_bullet = sample_bullets[0] if sample_bullets else state["target_role"]
    
    rag_context = retrieve_rewrite_context(
        bullet=query_bullet,
        target_role=state["target_role"],
        k=3,
    )
    
    return {"rag_context": rag_context}


def human_review_node(state: AgentState) -> dict:
    """Human-in-the-Loop review node — pauses execution for human approval.
    
    Uses LangGraph's interrupt() to pause the graph at this point.
    The graph can be resumed with Command(resume={"approval": ..., ...})
    after a human has reviewed the pending rewrites.
    """
    from langgraph.types import interrupt
    
    # Present the pending rewrites to the human reviewer
    pending_rewrites = state.get("rewrites", {})
    
    # Interrupt execution and wait for human input
    human_input = interrupt({
        "action_required": "review_rewrites",
        "pending_rewrites": pending_rewrites,
        "target_role": state["target_role"],
        "match_score": state.get("match_results", {}).get("overall_score"),
        "message": "Please review the suggested bullet rewrites. Approve, reject, or edit them.",
    })
    
    # Process the human's response
    approval = human_input.get("approval", "approved")
    feedback = human_input.get("feedback", "")
    edited_rewrites = human_input.get("edited_rewrites")
    
    result = {
        "human_approval": approval,
        "human_feedback": feedback,
    }
    
    if edited_rewrites:
        result["reviewed_rewrites"] = edited_rewrites
    elif approval == "approved":
        result["reviewed_rewrites"] = pending_rewrites
    
    return result


# ─────────────────────────────────────────────────────────
# 4. Workflow Assembly — Phase 3 Original (Backward Compatible)
# ─────────────────────────────────────────────────────────
def compile_workflow():
    """Assemble the nodes and edges into an executable LangGraph StateMachine."""
    builder = StateGraph(AgentState)

    # Add Nodes
    builder.add_node("extract_resume", extract_resume_node)
    builder.add_node("extract_jd", extract_jd_node)
    builder.add_node("compute_score", compute_score_node)
    builder.add_node("optimize_bullets", optimize_bullets_node)
    builder.add_node("aggregate_report", aggregate_report_node)

    # Define Edges (Parallel extraction -> Scoring -> Rewriting -> Aggregation)
    builder.add_edge(START, "extract_resume")
    builder.add_edge(START, "extract_jd")
    
    builder.add_edge("extract_resume", "compute_score")
    builder.add_edge("extract_jd", "compute_score")
    
    builder.add_edge("compute_score", "optimize_bullets")
    builder.add_edge("optimize_bullets", "aggregate_report")
    builder.add_edge("aggregate_report", END)

    # Compile Graph
    return builder.compile()


# ─────────────────────────────────────────────────────────
# 5. Workflow Assembly — Phase 4 RAG-Enhanced
# ─────────────────────────────────────────────────────────
def compile_rag_workflow():
    """Assemble the RAG-enhanced workflow with context retrieval.
    
    Graph flow:
        START → extract_resume ─┐
                                ├→ retrieve_context → compute_score → optimize_bullets → aggregate_report → END
        START → extract_jd ─────┘
    """
    builder = StateGraph(AgentState)

    # Add Nodes
    builder.add_node("extract_resume", extract_resume_node)
    builder.add_node("extract_jd", extract_jd_node)
    builder.add_node("retrieve_context", retrieve_context_node)
    builder.add_node("compute_score", compute_score_node)
    builder.add_node("optimize_bullets", optimize_bullets_node)
    builder.add_node("aggregate_report", aggregate_report_node)

    # Edges: Parallel extraction → RAG retrieval → Scoring → Rewriting → Aggregation
    builder.add_edge(START, "extract_resume")
    builder.add_edge(START, "extract_jd")
    
    builder.add_edge("extract_resume", "retrieve_context")
    builder.add_edge("extract_jd", "retrieve_context")
    
    builder.add_edge("retrieve_context", "compute_score")
    builder.add_edge("compute_score", "optimize_bullets")
    builder.add_edge("optimize_bullets", "aggregate_report")
    builder.add_edge("aggregate_report", END)

    return builder.compile()


# ─────────────────────────────────────────────────────────
# 6. Workflow Assembly — Phase 4 HITL (RAG + Human Review)
# ─────────────────────────────────────────────────────────
def compile_hitl_workflow(checkpointer=None):
    """Assemble the full HITL workflow with RAG context and human review gate.
    
    Graph flow:
        START → extract_resume ─┐
                                ├→ retrieve_context → compute_score → optimize_bullets → [HITL review] → aggregate_report → END
        START → extract_jd ─────┘
    
    Args:
        checkpointer: LangGraph checkpointer for state persistence across requests.
                      Required for HTTP-based HITL flows. Use MemorySaver for in-memory.
    """
    builder = StateGraph(AgentState)

    # Add Nodes
    builder.add_node("extract_resume", extract_resume_node)
    builder.add_node("extract_jd", extract_jd_node)
    builder.add_node("retrieve_context", retrieve_context_node)
    builder.add_node("compute_score", compute_score_node)
    builder.add_node("optimize_bullets", optimize_bullets_node)
    builder.add_node("human_review", human_review_node)
    builder.add_node("aggregate_report", aggregate_report_node)

    # Edges: Parallel extraction → RAG → Score → Rewrite → HITL Review → Aggregate
    builder.add_edge(START, "extract_resume")
    builder.add_edge(START, "extract_jd")
    
    builder.add_edge("extract_resume", "retrieve_context")
    builder.add_edge("extract_jd", "retrieve_context")
    
    builder.add_edge("retrieve_context", "compute_score")
    builder.add_edge("compute_score", "optimize_bullets")
    builder.add_edge("optimize_bullets", "human_review")
    builder.add_edge("human_review", "aggregate_report")
    builder.add_edge("aggregate_report", END)

    return builder.compile(checkpointer=checkpointer)


# Pre-compiled workflow instances for importing
app = compile_workflow()
rag_app = compile_rag_workflow()
