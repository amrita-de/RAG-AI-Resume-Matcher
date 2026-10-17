"""Core LLM baseline evaluation engine using LangChain and Pydantic structured output."""

import os
from typing import Optional, Tuple
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from agentic_ai.schemas import (
    ResumeEvaluation,
    ScoringRubric,
    SkillGapReport,
    BulletOptimization,
)

# Load environment variables from .env
load_dotenv()


SYSTEM_EVALUATION_PROMPT = """You are an elite Principal Technical Recruiter and ATS (Applicant Tracking System) Evaluation Specialist.
Your task is to analyze a candidate's resume against a target Job Description with extreme precision and actionable rigor.

Evaluation Criteria:
1. Skills Alignment:
   - Identify critical mandatory skills explicitly required by the JD that are found in the resume.
   - Flag high-priority missing technical or domain skills.
   - Note secondary or preferred 'nice-to-have' skills absent from the resume.

2. Scoring Rubric (0 - 100):
   - Skills Coverage (0-100): Direct overlap of core languages, libraries, and architectures.
   - Experience Relevance (0-100): Alignment of seniority, domain, and past scope of responsibility.
   - Quantified Impact (0-100): Assessment of whether bullet points demonstrate measurable business/technical outcomes rather than plain duty descriptions.
   - Overall Score (0-100): Weighted synthesis (50% skills, 30% experience, 20% impact).

3. Bullet Point Optimization:
   - Select 3 to 4 weak or generic bullet points from the resume.
   - Rewrite each bullet using Google's XYZ Formula:
     "Accomplished [X], as measured by [Y], by doing [Z]"
   - Start with punchy, high-impact past-tense action verbs (e.g., Architected, Optimized, Pioneered, Reduced).
   - Provide concrete explanations of why the revision improves candidate positioning for this specific JD.

4. Strategic Advice:
   - Provide a 2-3 sentence strategic verdict on candidacy and what the applicant should prioritize before submitting.

Be constructive, specific, and realistic. You must return your analysis strictly conforming to the requested schema.
"""

USER_PROMPT_TEMPLATE = """TARGET JOB DESCRIPTION:
----------------------------------------
{job_description}
----------------------------------------

CANDIDATE RESUME:
----------------------------------------
{resume_text}
----------------------------------------

Perform a deep technical evaluation and generate the structured match assessment."""


def get_available_provider() -> Tuple[str, Optional[object]]:
    """Determine the active LLM provider based on environment variables."""
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if openai_key:
        from langchain_openai import ChatOpenAI
        return "openai", ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.1)
    elif google_key:
        from langchain_google_genai import ChatGoogleGenerativeAI
        # Set GEMINI_API_KEY for langchain-google-genai if GOOGLE_API_KEY was used
        if not os.getenv("GEMINI_API_KEY") and google_key:
            os.environ["GEMINI_API_KEY"] = google_key
        return "google", ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"), temperature=0.1)
    elif groq_key:
        from langchain_groq import ChatGroq
        return "groq", ChatGroq(model=os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b"), temperature=0.1)
    else:
        return "mock", None


def mock_evaluate_resume(resume_text: str, jd_text: str) -> ResumeEvaluation:
    """Deterministic fallback evaluator used for offline testing or when no API key is supplied."""
    return ResumeEvaluation(
        candidate_name="Amrita De",
        target_role="Senior AI / Full Stack Engineer",
        overall_match_score=84,
        scoring_rubric=ScoringRubric(
            skills_score=88,
            experience_score=80,
            quantified_impact_score=82,
            rubric_summary=(
                "Strong technical alignment across Python, FastAPI, React, and FAISS/LangChain. "
                "Candidate has hands-on agentic and full-stack experience; additional emphasis on Kubernetes, "
                "observability (LangSmith), and enterprise scale will push the score higher."
            ),
        ),
        skills_alignment=SkillGapReport(
            matched_skills=[
                "Python",
                "FastAPI",
                "React.js",
                "TypeScript",
                "LangChain",
                "LangGraph",
                "FAISS",
                "Docker",
                "PostgreSQL",
            ],
            missing_critical_skills=[
                "Kubernetes microservices orchestration",
                "Celery asynchronous task queuing",
            ],
            missing_nice_to_have=[
                "LLM Observability (LangSmith / Phoenix)",
                "RAGAS evaluation framework",
                "Prompt caching & speculative decoding",
            ],
        ),
        bullet_rewrites=[
            BulletOptimization(
                original="Developed an automated resume parsing service using LangChain and OpenAI API to speed up recruiter workflows.",
                improved=(
                    "Architected an automated multi-agent resume parsing pipeline using LangChain and OpenAI API, "
                    "cutting recruiter screening cycle time by 45% across 5,000+ monthly applicants."
                ),
                explanation="Adds quantifiable business impact (45% cycle reduction) and specifies throughput scale.",
                metrics_highlighted="45% screening cycle time reduction",
            ),
            BulletOptimization(
                original="Built and maintained RESTful APIs using FastAPI and PostgreSQL handling 50k daily active requests.",
                improved=(
                    "Engineered asynchronous FastAPI microservices backed by PostgreSQL, sustaining 50,000+ daily requests "
                    "with sub-120ms P99 latency and 99.95% uptime."
                ),
                explanation="Transforms maintenance into engineering leadership with concrete P99 latency and SLA reliability numbers.",
                metrics_highlighted="Sub-120ms P99 latency & 99.95% uptime",
            ),
            BulletOptimization(
                original="Integrated FAISS vector database for semantic search over 20,000 product catalog entries.",
                improved=(
                    "Deployed a local FAISS dense vector search index over 20,000 catalog documents, "
                    "achieving 3x faster retrieval latency and boosting top-3 semantic search accuracy to 91%."
                ),
                explanation="Highlights retrieval latency gains and top-k accuracy metric directly valued for RAG roles.",
                metrics_highlighted="3x retrieval speedup & 91% top-3 accuracy",
            ),
        ],
        strategic_advice=(
            "You possess an excellent baseline for this role with strong LangGraph and FastAPI foundations. "
            "Incorporate mentions of container orchestration (Kubernetes) and agent observability into your summary, "
            "and emphasize the quantitative business outcomes highlighted in the rewritten bullets."
        ),
    )


def evaluate_resume(
    resume_text: str,
    job_description: str,
    force_provider: Optional[str] = None,
) -> Tuple[ResumeEvaluation, str]:
    """Execute the Phase 1 baseline evaluation pipeline using structured outputs.

    Args:
        resume_text: Extracted plain text of candidate resume.
        job_description: Text of target job description.
        force_provider: Optional provider override ('openai', 'google', 'groq', 'mock').

    Returns:
        Tuple of (ResumeEvaluation, provider_name_used).
    """
    if force_provider == "mock":
        return mock_evaluate_resume(resume_text, job_description), "mock"

    provider_name, llm = get_available_provider()

    if force_provider and force_provider != provider_name:
        # User explicitly requested a specific provider
        provider_name = force_provider
        if provider_name == "openai":
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.1)
        elif provider_name == "google":
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"), temperature=0.1)
        elif provider_name == "groq":
            from langchain_groq import ChatGroq
            llm = ChatGroq(model=os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b"), temperature=0.1)
        else:
            llm = None

    if llm is None:
        print("[Evaluator] Notice: No active LLM API key detected (OPENAI_API_KEY, GEMINI_API_KEY, or GROQ_API_KEY).")
        print("[Evaluator] Running deterministic baseline mock evaluator to validate pipeline and schemas.")
        return mock_evaluate_resume(resume_text, job_description), "mock (no api key)"

    # Build LangChain prompt & structured output model
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_EVALUATION_PROMPT),
        ("user", USER_PROMPT_TEMPLATE),
    ])

    structured_llm = llm.with_structured_output(ResumeEvaluation)
    chain = prompt | structured_llm

    result: ResumeEvaluation = chain.invoke({
        "resume_text": resume_text,
        "job_description": job_description,
    })

    return result, provider_name
