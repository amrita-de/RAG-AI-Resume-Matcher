"""Phase 4: FastAPI REST API — Production HTTP interface for the Agentic AI pipeline.

Exposes the full LangGraph pipeline (Phase 3), RAG-enhanced pipeline (Phase 4),
and Human-in-the-Loop approval flows as versioned REST endpoints with
Swagger/OpenAPI documentation.

Launch:
    uvicorn agentic_ai.api:app --reload --host 0.0.0.0 --port 8000
    Then visit: http://localhost:8000/docs
"""

import uuid
import logging
from contextlib import asynccontextmanager

from typing import Optional

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

from agentic_ai.api_schemas import (
    HealthResponse,
    EvaluateRequest,
    EvaluateResponse,
    RAGEvaluateRequest,
    ExtractSkillsRequest,
    ExtractSkillsResponse,
    MatchScoreRequest,
    MatchScoreResponse,
    RewriteBulletsRequest,
    RewriteBulletsResponse,
    SimilarJDsRequest,
    SimilarJDsResponse,
    HITLReviewRequest,
    HITLStartResponse,
    HITLStatusResponse,
    ErrorResponse,
)
from agentic_ai.tools import extract_skills, compute_match_score, suggest_rewrite
from agentic_ai.graph import app as phase3_app, compile_rag_workflow, compile_hitl_workflow
from agentic_ai.rag import retrieve_similar_jds, retrieve_rewrite_context
from agentic_ai.parsers import parse_document
from agentic_ai.sample_data import SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────
# In-memory stores for HITL sessions
# ─────────────────────────────────────────────────────────
_hitl_sessions: dict = {}


# ─────────────────────────────────────────────────────────
# Application Lifespan
# ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle handler."""
    logger.info("Agentic AI API starting up — Phase 4: RAG + API + HITL")
    yield
    logger.info("Agentic AI API shutting down.")


# ─────────────────────────────────────────────────────────
# FastAPI App Initialization
# ─────────────────────────────────────────────────────────
api_app = FastAPI(
    title="Agentic AI Resume Matcher API",
    description=(
        "Production REST API for the Agentic AI Resume & JD Matcher. "
        "Provides skill extraction, match scoring, bullet rewriting, "
        "RAG-enhanced evaluation, and Human-in-the-Loop approval flows."
    ),
    version="0.4.0",
    lifespan=lifespan,
)

# CORS middleware for frontend integration
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Alias so `uvicorn agentic_ai.api:app` works (matches docstring convention)
app = api_app


# ═══════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════

@api_app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint returning API status and version."""
    return HealthResponse()


# ═══════════════════════════════════════════════════════
# CORE ENDPOINTS — Individual Tool Access
# ═══════════════════════════════════════════════════════

@api_app.post(
    "/api/v1/extract-skills",
    response_model=ExtractSkillsResponse,
    tags=["Tools"],
    summary="Extract structured skills from text",
)
async def api_extract_skills(request: ExtractSkillsRequest):
    """Extract technical skills, soft skills, domain knowledge, and certifications
    from a resume or job description."""
    try:
        skills = extract_skills.invoke({
            "text": request.text,
            "source_type": request.source_type,
        })
        return ExtractSkillsResponse(
            source_type=request.source_type,
            skills=skills,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_app.post(
    "/api/v1/match-score",
    response_model=MatchScoreResponse,
    tags=["Tools"],
    summary="Compute ATS match score",
)
async def api_match_score(request: MatchScoreRequest):
    """Compute a detailed ATS match score comparing resume skills against JD requirements."""
    try:
        result = compute_match_score.invoke({
            "resume_skills": request.resume_skills,
            "jd_skills": request.jd_skills,
            "resume_text": request.resume_text,
            "jd_text": request.jd_text,
        })
        return MatchScoreResponse(match_results=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_app.post(
    "/api/v1/rewrite-bullets",
    response_model=RewriteBulletsResponse,
    tags=["Tools"],
    summary="Rewrite resume bullet points",
)
async def api_rewrite_bullets(request: RewriteBulletsRequest):
    """Rewrite resume bullet points using Google's XYZ formula.
    Optionally uses RAG-retrieved best practice examples for grounding."""
    try:
        invoke_args = {
            "bullet_points": request.bullet_points,
            "target_role": request.target_role,
            "missing_skills": request.missing_skills,
        }

        if request.use_rag:
            rag_context = retrieve_rewrite_context(
                bullet=request.bullet_points[0],
                target_role=request.target_role,
            )
            invoke_args["rag_context"] = rag_context

        result = suggest_rewrite.invoke(invoke_args)
        return RewriteBulletsResponse(
            rewrites=result,
            rag_enhanced=request.use_rag,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_app.post(
    "/api/v1/similar-jds",
    response_model=SimilarJDsResponse,
    tags=["RAG"],
    summary="Find similar job descriptions",
)
async def api_similar_jds(request: SimilarJDsRequest):
    """Retrieve the most semantically similar job descriptions from the indexed corpus."""
    try:
        results = retrieve_similar_jds(request.resume_text, k=request.k)
        return SimilarJDsResponse(
            similar_jds=results,
            count=len(results),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════
# PIPELINE ENDPOINTS — Full Workflow Execution
# ═══════════════════════════════════════════════════════

@api_app.post(
    "/api/v1/evaluate",
    response_model=EvaluateResponse,
    tags=["Pipeline"],
    summary="Run full evaluation pipeline",
)
async def api_evaluate(request: EvaluateRequest):
    """Execute the complete Phase 3 LangGraph pipeline: extract → score → rewrite → report."""
    try:
        inputs = {
            "resume_text": request.resume_text,
            "jd_text": request.jd_text,
            "target_role": request.target_role,
        }
        result = phase3_app.invoke(inputs)
        report = result.get("final_report", {})

        return EvaluateResponse(
            status=report.get("status", "success"),
            target_role=report.get("target_role", request.target_role),
            match_results=report.get("match_results"),
            rewrites=report.get("rewrites"),
            rag_enhanced=False,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_app.post(
    "/api/v1/evaluate/rag",
    response_model=EvaluateResponse,
    tags=["Pipeline", "RAG"],
    summary="Run RAG-enhanced evaluation pipeline",
)
async def api_evaluate_rag(request: RAGEvaluateRequest):
    """Execute the Phase 4 RAG-enhanced pipeline with context retrieval.
    
    If jd_text is not provided, the best-matching JD is auto-retrieved from the corpus.
    """
    try:
        jd_text = request.jd_text
        if not jd_text:
            similar_jds = retrieve_similar_jds(request.resume_text, k=1)
            if similar_jds:
                jd_text = similar_jds[0]["text"]
            else:
                raise HTTPException(
                    status_code=400,
                    detail="No JD text provided and no similar JDs found in the index.",
                )

        rag_workflow = compile_rag_workflow()
        inputs = {
            "resume_text": request.resume_text,
            "jd_text": jd_text,
            "target_role": request.target_role,
        }
        result = rag_workflow.invoke(inputs)
        report = result.get("final_report", {})

        return EvaluateResponse(
            status=report.get("status", "success"),
            target_role=report.get("target_role", request.target_role),
            match_results=report.get("match_results"),
            rewrites=report.get("rewrites"),
            rag_enhanced=report.get("rag_enhanced", True),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════
# HITL ENDPOINTS — Human-in-the-Loop Approval Flow
# ═══════════════════════════════════════════════════════

@api_app.post(
    "/api/v1/evaluate/hitl",
    response_model=HITLStartResponse,
    tags=["Pipeline", "HITL"],
    summary="Start HITL evaluation pipeline",
)
async def api_evaluate_hitl_start(request: EvaluateRequest):
    """Start the HITL pipeline. Runs to the human review node, pauses,
    and returns pending rewrites for review."""
    try:
        from langgraph.checkpoint.memory import MemorySaver

        thread_id = str(uuid.uuid4())
        checkpointer = MemorySaver()
        hitl_workflow = compile_hitl_workflow(checkpointer=checkpointer)

        inputs = {
            "resume_text": request.resume_text,
            "jd_text": request.jd_text,
            "target_role": request.target_role,
        }

        config = {"configurable": {"thread_id": thread_id}}

        # Run until interrupt (at human_review_node)
        result = hitl_workflow.invoke(inputs, config=config)

        # Extract the state at the interrupt point
        state = hitl_workflow.get_state(config)
        pending_rewrites = state.values.get("rewrites")
        match_results = state.values.get("match_results")

        # Store session for later resume
        _hitl_sessions[thread_id] = {
            "workflow": hitl_workflow,
            "checkpointer": checkpointer,
            "config": config,
            "status": "pending_review",
        }

        return HITLStartResponse(
            thread_id=thread_id,
            pending_rewrites=pending_rewrites,
            match_results=match_results,
            target_role=request.target_role,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_app.post(
    "/api/v1/evaluate/hitl/{thread_id}/review",
    response_model=EvaluateResponse,
    tags=["Pipeline", "HITL"],
    summary="Submit human review for HITL pipeline",
)
async def api_evaluate_hitl_review(thread_id: str, request: HITLReviewRequest):
    """Submit human approval/rejection/edits and resume the HITL graph execution."""
    session = _hitl_sessions.get(thread_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"HITL session '{thread_id}' not found.")

    if session["status"] != "pending_review":
        raise HTTPException(
            status_code=400,
            detail=f"Session is '{session['status']}', not 'pending_review'.",
        )

    try:
        from langgraph.types import Command

        workflow = session["workflow"]
        config = session["config"]

        # Resume the graph with human input
        human_input = {
            "approval": request.approval,
            "feedback": request.feedback,
        }
        if request.edited_rewrites:
            human_input["edited_rewrites"] = request.edited_rewrites

        result = workflow.invoke(
            Command(resume=human_input),
            config=config,
        )

        report = result.get("final_report", {})
        session["status"] = "completed"

        return EvaluateResponse(
            status=report.get("status", "success"),
            target_role=report.get("target_role", ""),
            match_results=report.get("match_results"),
            rewrites=report.get("rewrites"),
            rag_enhanced=report.get("rag_enhanced", False),
            human_review=report.get("human_review"),
        )
    except Exception as e:
        session["status"] = "error"
        raise HTTPException(status_code=500, detail=str(e))


@api_app.get(
    "/api/v1/evaluate/hitl/{thread_id}/status",
    response_model=HITLStatusResponse,
    tags=["Pipeline", "HITL"],
    summary="Check HITL pipeline status",
)
async def api_evaluate_hitl_status(thread_id: str):
    """Check the current status of a HITL pipeline session."""
    session = _hitl_sessions.get(thread_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"HITL session '{thread_id}' not found.")

    final_report = None
    if session["status"] == "completed":
        try:
            config = session["config"]
            state = session["workflow"].get_state(config)
            final_report = state.values.get("final_report")
        except Exception:
            pass

    return HITLStatusResponse(
        thread_id=thread_id,
        status=session["status"],
        final_report=final_report,
    )


# ═══════════════════════════════════════════════════════
# FILE UPLOAD ENDPOINT — React Frontend Integration
# ═══════════════════════════════════════════════════════

@api_app.post(
    "/api/v1/upload-and-evaluate",
    response_model=EvaluateResponse,
    tags=["Pipeline", "Upload"],
    summary="Upload resume file and evaluate against JD",
)
async def api_upload_and_evaluate(
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    jd_text: str = Form(..., description="Job description text", min_length=50),
    target_role: str = Form(default="Software Engineer", description="Target job role title"),
    pipeline_type: str = Form(default="standard", description="Pipeline: 'standard', 'rag', or 'hitl'"),
):
    """Upload a resume file (PDF, DOCX, TXT) and run the evaluation pipeline.
    
    Supports three pipeline modes:
    - 'standard': Phase 3 LangGraph pipeline
    - 'rag': Phase 4 RAG-enhanced pipeline
    - 'hitl': Phase 4 Human-in-the-Loop pipeline (returns pending rewrites)
    """
    # Validate file type
    allowed_extensions = {".pdf", ".docx", ".doc", ".txt", ".md"}
    filename = resume_file.filename or "upload.txt"
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Accepted: {', '.join(allowed_extensions)}",
        )

    try:
        # Read and parse the uploaded file
        file_bytes = await resume_file.read()
        resume_text = parse_document(file_bytes, filename=filename)

        if len(resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Extracted resume text is too short. Please upload a valid resume file.",
            )

        inputs = {
            "resume_text": resume_text,
            "jd_text": jd_text,
            "target_role": target_role,
        }

        if pipeline_type == "rag":
            rag_workflow = compile_rag_workflow()
            result = rag_workflow.invoke(inputs)
        elif pipeline_type == "hitl":
            # For HITL uploads, delegate to the HITL start endpoint logic
            from agentic_ai.api_schemas import EvaluateRequest as _ER
            req = _ER(resume_text=resume_text, jd_text=jd_text, target_role=target_role)
            hitl_resp = await api_evaluate_hitl_start(req)
            return EvaluateResponse(
                status="pending_review",
                target_role=target_role,
                match_results=hitl_resp.match_results,
                rewrites=hitl_resp.pending_rewrites,
                rag_enhanced=False,
                human_review={"thread_id": hitl_resp.thread_id},
            )
        else:
            result = phase3_app.invoke(inputs)

        report = result.get("final_report", {})

        return EvaluateResponse(
            status=report.get("status", "success"),
            target_role=report.get("target_role", target_role),
            match_results=report.get("match_results"),
            rewrites=report.get("rewrites"),
            rag_enhanced=pipeline_type == "rag",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════
# SAMPLE DATA ENDPOINT — Quick Fill for Frontend
# ═══════════════════════════════════════════════════════

@api_app.get(
    "/api/v1/sample-data",
    tags=["System"],
    summary="Get built-in sample resume and JD for testing",
)
async def api_sample_data():
    """Return the built-in sample resume and job description fixtures."""
    return {
        "resume_text": SAMPLE_RESUME,
        "jd_text": SAMPLE_JOB_DESCRIPTION,
        "target_role": "Senior AI / Full Stack Engineer",
    }
