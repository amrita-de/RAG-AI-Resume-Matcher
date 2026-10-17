"""Automated verification tests for Phase 3: LangGraph Orchestration."""

import pytest
from agentic_ai.graph import app
from agentic_ai.sample_data import SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION


class TestLangGraphPipeline:
    """Verify that the LangGraph workflow properly connects nodes and manages state."""

    def test_graph_compilation(self):
        """Verify the graph compiles successfully without edge configuration errors."""
        # 'app' is already compiled in graph.py, so its existence verifies compilation.
        assert app is not None
        assert hasattr(app, "invoke")

    def test_full_pipeline_execution(self):
        """Verify the full pipeline executes end-to-end and populates the final report."""
        inputs = {
            "resume_text": SAMPLE_RESUME,
            "jd_text": SAMPLE_JOB_DESCRIPTION,
            "target_role": "AI Engineer",
        }
        
        # Invoke graph
        result = app.invoke(inputs)
        
        # Verify state propagation
        assert "resume_skills" in result
        assert "jd_skills" in result
        assert "match_results" in result
        assert "rewrites" in result
        assert "final_report" in result
        
        # Verify final report structure
        report = result["final_report"]
        assert report["status"] == "success"
        assert report["target_role"] == "AI Engineer"
        
        # Check that scores propagated properly
        match_results = report["match_results"]
        assert match_results is not None
        assert "overall_score" in match_results
        
        # Check that rewrites propagated properly
        rewrites = report["rewrites"]
        assert rewrites is not None
        assert "rewritten_bullets" in rewrites
        assert "strategic_summary" in rewrites

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
