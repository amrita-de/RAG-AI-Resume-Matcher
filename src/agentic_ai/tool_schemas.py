"""Phase 2: Pydantic input/output schemas for modular agent tools.

These schemas define the strict data contracts for each individual tool function,
enabling the LLM to understand the exact expected input format and output structure
when calling tools autonomously.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────
# extract_skills tool schemas
# ─────────────────────────────────────────────────

class ExtractSkillsInput(BaseModel):
    """Input schema for the extract_skills tool."""
    text: str = Field(
        ...,
        description="Raw text content of a resume or job description to extract skills from.",
    )
    source_type: str = Field(
        ...,
        description="Whether this text is a 'resume' or 'job_description'.",
        pattern=r"^(resume|job_description)$",
    )


class ExtractedSkills(BaseModel):
    """Output of skill extraction from a single document."""
    source_type: str = Field(
        ...,
        description="Whether skills were extracted from a 'resume' or 'job_description'.",
    )
    technical_skills: List[str] = Field(
        default_factory=list,
        description="Programming languages, frameworks, databases, cloud tools, and infrastructure technologies.",
    )
    soft_skills: List[str] = Field(
        default_factory=list,
        description="Leadership, communication, collaboration, and interpersonal competencies.",
    )
    domain_knowledge: List[str] = Field(
        default_factory=list,
        description="Industry-specific knowledge areas (e.g., 'RAG systems', 'ATS optimization', 'microservices architecture').",
    )
    certifications_and_methodologies: List[str] = Field(
        default_factory=list,
        description="Certifications (AWS, GCP), standards (ISO), or methodologies (Agile, Scrum, CI/CD).",
    )
    years_of_experience: Optional[str] = Field(
        default=None,
        description="Total years of experience if explicitly mentioned (e.g., '3+ years').",
    )


# ─────────────────────────────────────────────────
# compute_match_score tool schemas
# ─────────────────────────────────────────────────

class MatchScoreInput(BaseModel):
    """Input schema for the compute_match_score tool."""
    resume_skills: ExtractedSkills = Field(
        ...,
        description="Skills extracted from the candidate resume.",
    )
    jd_skills: ExtractedSkills = Field(
        ...,
        description="Skills extracted from the target job description.",
    )
    resume_text: str = Field(
        ...,
        description="Full raw resume text for evaluating experience depth and bullet quality.",
    )
    jd_text: str = Field(
        ...,
        description="Full raw job description text for role context.",
    )


class MatchScoreOutput(BaseModel):
    """Output of the match scoring tool."""
    overall_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Weighted ATS match score from 0 (no match) to 100 (ideal candidate).",
    )
    skills_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Direct skill overlap score across technical, domain, and soft competencies.",
    )
    experience_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Seniority, domain relevance, and scope of past responsibilities.",
    )
    impact_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Degree to which resume bullets demonstrate quantified, measurable outcomes.",
    )
    matched_skills: List[str] = Field(
        default_factory=list,
        description="Skills present in both the resume and the JD.",
    )
    missing_critical: List[str] = Field(
        default_factory=list,
        description="Mandatory JD skills absent from the resume.",
    )
    missing_preferred: List[str] = Field(
        default_factory=list,
        description="Nice-to-have JD skills absent from the resume.",
    )
    scoring_rationale: str = Field(
        ...,
        description="2-3 sentence narrative justifying the scoring breakdown.",
    )


# ─────────────────────────────────────────────────
# suggest_rewrite tool schemas
# ─────────────────────────────────────────────────

class RewriteInput(BaseModel):
    """Input schema for the suggest_rewrite tool."""
    bullet_points: List[str] = Field(
        ...,
        description="List of original resume bullet points to optimize.",
    )
    target_role: str = Field(
        ...,
        description="Title of the target role being applied for.",
    )
    missing_skills: List[str] = Field(
        default_factory=list,
        description="Critical skills the candidate is missing that rewrites should try to address.",
    )


class RewrittenBullet(BaseModel):
    """A single rewritten bullet point following the Google XYZ formula."""
    original: str = Field(
        ...,
        description="The original bullet point.",
    )
    rewritten: str = Field(
        ...,
        description="Optimized bullet using XYZ formula: 'Accomplished [X], as measured by [Y], by doing [Z]'.",
    )
    reasoning: str = Field(
        ...,
        description="Why this rewrite improves alignment with the target role.",
    )
    skills_addressed: List[str] = Field(
        default_factory=list,
        description="Skills from the JD that this rewritten bullet now highlights.",
    )


class RewriteOutput(BaseModel):
    """Output of the bullet rewrite tool."""
    rewritten_bullets: List[RewrittenBullet] = Field(
        default_factory=list,
        description="List of optimized bullet points.",
    )
    strategic_summary: str = Field(
        ...,
        description="Brief actionable advice on overall resume positioning for the target role.",
    )
