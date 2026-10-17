"""Phase 4: Pydantic request/response schemas for FastAPI endpoints.

These models define the API contract for the REST interface, wrapping
the existing tool_schemas.py models in HTTP-friendly request/response envelopes.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────
# Request Models
# ─────────────────────────────────────────────────────────

class EvaluateRequest(BaseModel):
    """Request body for the /api/v1/evaluate endpoint."""
    resume_text: str = Field(
        ...,
        description="Raw text of the candidate's resume.",
        min_length=50,
    )
    jd_text: str = Field(
        ...,
        description="Raw text of the target job description.",
        min_length=50,
    )
    target_role: str = Field(
        ...,
        description="Title of the target job role.",
        min_length=2,
    )


class RAGEvaluateRequest(BaseModel):
    """Request body for the /api/v1/evaluate/rag endpoint.
    
    Only requires resume_text and target_role — the JD is auto-retrieved
    from the RAG index, or can be optionally provided.
    """
    resume_text: str = Field(
        ...,
        description="Raw text of the candidate's resume.",
        min_length=50,
    )
    target_role: str = Field(
        ...,
        description="Title of the target job role.",
        min_length=2,
    )
    jd_text: Optional[str] = Field(
        default=None,
        description="Optional JD text. If not provided, the best-matching JD is auto-retrieved.",
    )


class ExtractSkillsRequest(BaseModel):
    """Request body for the /api/v1/extract-skills endpoint."""
    text: str = Field(
        ...,
        description="Raw text of a resume or job description.",
        min_length=20,
    )
    source_type: str = Field(
        default="resume",
        description="Whether this text is a 'resume' or 'job_description'.",
        pattern=r"^(resume|job_description)$",
    )


class MatchScoreRequest(BaseModel):
    """Request body for the /api/v1/match-score endpoint."""
    resume_skills: Dict[str, Any] = Field(
        ...,
        description="Extracted skills dictionary from the candidate resume.",
    )
    jd_skills: Dict[str, Any] = Field(
        ...,
        description="Extracted skills dictionary from the target job description.",
    )
    resume_text: str = Field(
        ...,
        description="Full raw resume text for experience evaluation.",
    )
    jd_text: str = Field(
        ...,
        description="Full raw job description text for context.",
    )


class RewriteBulletsRequest(BaseModel):
    """Request body for the /api/v1/rewrite-bullets endpoint."""
    bullet_points: List[str] = Field(
        ...,
        description="List of original resume bullet point strings to optimize.",
        min_length=1,
    )
    target_role: str = Field(
        ...,
        description="Title of the target job role.",
    )
    missing_skills: List[str] = Field(
        default_factory=list,
        description="Optional list of missing critical skills to address.",
    )
    use_rag: bool = Field(
        default=False,
        description="Whether to use RAG-retrieved best practice examples for grounding.",
    )


class SimilarJDsRequest(BaseModel):
    """Request body for the /api/v1/similar-jds endpoint."""
    resume_text: str = Field(
        ...,
        description="Raw text of the candidate's resume.",
        min_length=50,
    )
    k: int = Field(
        default=3,
        description="Number of similar JDs to retrieve.",
        ge=1,
        le=10,
    )


class HITLReviewRequest(BaseModel):
    """Request body for submitting human review to a HITL pipeline."""
    approval: str = Field(
        ...,
        description="Review decision: 'approved', 'rejected', or 'edited'.",
        pattern=r"^(approved|rejected|edited)$",
    )
    feedback: str = Field(
        default="",
        description="Optional reviewer comments.",
    )
    edited_rewrites: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Modified rewrites if the reviewer edited them.",
    )


# ─────────────────────────────────────────────────────────
# Response Models
# ─────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    """Response for the /health endpoint."""
    status: str = "healthy"
    version: str = "0.1.0"
    phase: str = "Phase 4: RAG + API + HITL"


class EvaluateResponse(BaseModel):
    """Response for evaluation endpoints."""
    status: str = Field(..., description="'success' or 'error'.")
    target_role: str = Field(..., description="The target role evaluated against.")
    match_results: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Match scoring results.",
    )
    rewrites: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Rewritten bullet points.",
    )
    rag_enhanced: bool = Field(
        default=False,
        description="Whether RAG context was used.",
    )
    human_review: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Human review metadata if HITL was used.",
    )


class ExtractSkillsResponse(BaseModel):
    """Response for the /api/v1/extract-skills endpoint."""
    status: str = "success"
    source_type: str
    skills: Dict[str, Any]


class MatchScoreResponse(BaseModel):
    """Response for the /api/v1/match-score endpoint."""
    status: str = "success"
    match_results: Dict[str, Any]


class RewriteBulletsResponse(BaseModel):
    """Response for the /api/v1/rewrite-bullets endpoint."""
    status: str = "success"
    rewrites: Dict[str, Any]
    rag_enhanced: bool = False


class SimilarJDsResponse(BaseModel):
    """Response for the /api/v1/similar-jds endpoint."""
    status: str = "success"
    similar_jds: List[Dict[str, Any]]
    count: int


class HITLStartResponse(BaseModel):
    """Response when starting a HITL pipeline."""
    status: str = "pending_review"
    thread_id: str = Field(..., description="Unique thread ID for this HITL session.")
    pending_rewrites: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Bullet rewrites pending human review.",
    )
    match_results: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Match results for reviewer context.",
    )
    target_role: str = Field(..., description="Target role being evaluated.")


class HITLStatusResponse(BaseModel):
    """Response for checking HITL pipeline status."""
    thread_id: str
    status: str = Field(..., description="'pending_review', 'completed', or 'error'.")
    final_report: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Structured error response."""
    status: str = "error"
    message: str
    detail: Optional[str] = None
