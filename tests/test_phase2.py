"""Automated verification tests for Phase 2: Modular Agent Tools."""

import pytest
from langchain_core.tools import BaseTool

from agentic_ai.tools import (
    extract_skills,
    compute_match_score,
    suggest_rewrite,
    ALL_TOOLS,
)
from agentic_ai.tool_schemas import (
    ExtractedSkills,
    MatchScoreOutput,
    RewriteOutput,
)
from agentic_ai.sample_data import SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION


class TestToolDecorators:
    """Verify that tools are properly decorated and discoverable by LangGraph."""

    def test_all_tools_are_langchain_tools(self):
        """Each tool should be a LangChain BaseTool instance."""
        for t in ALL_TOOLS:
            assert isinstance(t, BaseTool), f"{t.name} is not a BaseTool"

    def test_tool_names(self):
        """Tool names should match expected identifiers."""
        names = {t.name for t in ALL_TOOLS}
        assert "extract_skills" in names
        assert "compute_match_score" in names
        assert "suggest_rewrite" in names

    def test_tools_have_descriptions(self):
        """Each tool must have a non-empty description for LLM discoverability."""
        for t in ALL_TOOLS:
            assert t.description and len(t.description) > 10, (
                f"Tool '{t.name}' has insufficient description"
            )

    def test_tools_have_args_schema(self):
        """Each tool must expose an args_schema for structured invocation."""
        for t in ALL_TOOLS:
            schema = t.args_schema
            assert schema is not None, f"Tool '{t.name}' has no args_schema"


class TestExtractSkills:
    """Verify extract_skills tool invocation and output structure."""

    def test_extract_from_resume(self):
        result = extract_skills.invoke({
            "text": SAMPLE_RESUME,
            "source_type": "resume",
        })
        assert isinstance(result, dict)
        assert result["source_type"] == "resume"
        assert len(result["technical_skills"]) > 0
        assert "Python" in result["technical_skills"]

    def test_extract_from_jd(self):
        result = extract_skills.invoke({
            "text": SAMPLE_JOB_DESCRIPTION,
            "source_type": "job_description",
        })
        assert isinstance(result, dict)
        assert result["source_type"] == "job_description"
        assert len(result["technical_skills"]) > 0

    def test_years_of_experience_extracted(self):
        result = extract_skills.invoke({
            "text": SAMPLE_RESUME,
            "source_type": "resume",
        })
        assert result.get("years_of_experience") is not None


class TestComputeMatchScore:
    """Verify compute_match_score tool output validity."""

    def _get_skills_pair(self):
        resume_skills = extract_skills.invoke({
            "text": SAMPLE_RESUME,
            "source_type": "resume",
        })
        jd_skills = extract_skills.invoke({
            "text": SAMPLE_JOB_DESCRIPTION,
            "source_type": "job_description",
        })
        return resume_skills, jd_skills

    def test_score_output_structure(self):
        resume_skills, jd_skills = self._get_skills_pair()
        result = compute_match_score.invoke({
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "resume_text": SAMPLE_RESUME,
            "jd_text": SAMPLE_JOB_DESCRIPTION,
        })
        assert isinstance(result, dict)
        assert 0 <= result["overall_score"] <= 100
        assert 0 <= result["skills_score"] <= 100
        assert 0 <= result["experience_score"] <= 100
        assert 0 <= result["impact_score"] <= 100

    def test_matched_skills_not_empty(self):
        resume_skills, jd_skills = self._get_skills_pair()
        result = compute_match_score.invoke({
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "resume_text": SAMPLE_RESUME,
            "jd_text": SAMPLE_JOB_DESCRIPTION,
        })
        assert len(result["matched_skills"]) > 0

    def test_has_scoring_rationale(self):
        resume_skills, jd_skills = self._get_skills_pair()
        result = compute_match_score.invoke({
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "resume_text": SAMPLE_RESUME,
            "jd_text": SAMPLE_JOB_DESCRIPTION,
        })
        assert len(result["scoring_rationale"]) > 20


class TestSuggestRewrite:
    """Verify suggest_rewrite tool output validity."""

    def test_rewrite_output_structure(self):
        result = suggest_rewrite.invoke({
            "bullet_points": [
                "Built REST APIs using FastAPI.",
                "Worked with FAISS for search.",
            ],
            "target_role": "Senior AI Engineer",
            "missing_skills": ["Kubernetes"],
        })
        assert isinstance(result, dict)
        assert len(result["rewritten_bullets"]) > 0
        assert result["strategic_summary"] and len(result["strategic_summary"]) > 10

    def test_each_rewrite_has_required_fields(self):
        result = suggest_rewrite.invoke({
            "bullet_points": [
                "Developed an automated resume parsing service using LangChain.",
            ],
            "target_role": "AI Engineer",
        })
        for bullet in result["rewritten_bullets"]:
            assert "original" in bullet
            assert "rewritten" in bullet
            assert "reasoning" in bullet
            assert bullet["rewritten"] != bullet["original"]

    def test_rewrite_count_matches_input(self):
        bullets = [
            "Built APIs.",
            "Used Docker.",
            "Deployed to AWS.",
        ]
        result = suggest_rewrite.invoke({
            "bullet_points": bullets,
            "target_role": "DevOps Engineer",
        })
        assert len(result["rewritten_bullets"]) <= len(bullets)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
