"""Pydantic data models for structured resume & job description analysis."""

from typing import List, Optional
from pydantic import BaseModel, Field


class BulletOptimization(BaseModel):
    """Represents an optimized resume bullet point following the Google XYZ formula:
    'Accomplished [X], as measured by [Y], by doing [Z]'."""

    original: str = Field(
        ...,
        description="The original bullet point or responsibility statement from the resume.",
    )
    improved: str = Field(
        ...,
        description="The optimized bullet point incorporating strong action verbs and quantified impact.",
    )
    explanation: str = Field(
        ...,
        description="Reasoning explaining why this rewrite better aligns with the target role.",
    )
    metrics_highlighted: Optional[str] = Field(
        default=None,
        description="Specific metric or measurable impact added/emphasized (e.g. '35% latency reduction').",
    )


class SkillGapReport(BaseModel):
    """Categorized skill alignment between candidate resume and job requirements."""

    matched_skills: List[str] = Field(
        default_factory=list,
        description="Key technical and functional skills present in both the resume and the job description.",
    )
    missing_critical_skills: List[str] = Field(
        default_factory=list,
        description="High-priority mandatory skills mentioned in the JD that are absent or under-represented in the resume.",
    )
    missing_nice_to_have: List[str] = Field(
        default_factory=list,
        description="Secondary, preferred, or bonus skills mentioned in the JD not found in the resume.",
    )


class ScoringRubric(BaseModel):
    """Detailed score breakdown across core candidate dimensions."""

    skills_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Score based on coverage of core and secondary technical skills.",
    )
    experience_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Score based on seniority, domain alignment, and relevance of work history.",
    )
    quantified_impact_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Score assessing whether achievements use measurable data and outcomes rather than generic duties.",
    )
    rubric_summary: str = Field(
        ...,
        description="Brief narrative explaining the score allocation.",
    )


class ResumeEvaluation(BaseModel):
    """Comprehensive structured report evaluating resume alignment against a target Job Description."""

    candidate_name: Optional[str] = Field(
        default="Candidate",
        description="Name of candidate extracted from resume, if identifiable.",
    )
    target_role: str = Field(
        ...,
        description="Title or functional focus of target job description.",
    )
    overall_match_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Aggregated ATS match score from 0 (no match) to 100 (ideal match).",
    )
    scoring_rubric: ScoringRubric = Field(
        ...,
        description="Breakdown of candidate scoring across skills, experience, and quantifiable impact.",
    )
    skills_alignment: SkillGapReport = Field(
        ...,
        description="Categorized inventory of matched and missing skills.",
    )
    bullet_rewrites: List[BulletOptimization] = Field(
        default_factory=list,
        description="3 to 5 high-impact bullet point rewrites tailored for the target role.",
    )
    strategic_advice: str = Field(
        ...,
        description="2-3 actionable sentences advising the candidate on how to position themselves for this role.",
    )
