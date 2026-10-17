"""Automated verification tests for Phase 4: RAG + API + HITL.

Tests cover three pillars:
1. RAG Pipeline — FAISS indexing and retrieval
2. FastAPI API — Endpoint contracts and responses
3. HITL — Graph compilation, interrupt, and resume
"""

import pytest
from agentic_ai.sample_data import SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION


# ═══════════════════════════════════════════════════════
# RAG PIPELINE TESTS
# ═══════════════════════════════════════════════════════

class TestRAGPipeline:
    """Verify RAG vector indexing, retrieval, and mock fallbacks."""

    def test_jd_retrieval_returns_results(self):
        """Verify JD retrieval returns a non-empty list of results."""
        from agentic_ai.rag import retrieve_similar_jds, reset_indices
        reset_indices()

        results = retrieve_similar_jds(SAMPLE_RESUME, k=3)

        assert isinstance(results, list)
        assert len(results) > 0
        assert len(results) <= 3

    def test_jd_retrieval_result_structure(self):
        """Verify each retrieved JD has the expected fields."""
        from agentic_ai.rag import retrieve_similar_jds

        results = retrieve_similar_jds(SAMPLE_RESUME, k=1)

        jd = results[0]
        assert "title" in jd
        assert "company" in jd
        assert "text" in jd
        assert "similarity_score" in jd
        assert isinstance(jd["similarity_score"], float)

    def test_best_practices_retrieval_returns_results(self):
        """Verify best practices retrieval returns relevant examples."""
        from agentic_ai.rag import retrieve_rewrite_context, reset_indices
        reset_indices()

        result = retrieve_rewrite_context(
            bullet="Built REST APIs using FastAPI and PostgreSQL",
            target_role="Backend Engineer",
            k=3,
        )

        assert isinstance(result, dict)
        assert "examples" in result
        assert "target_role" in result
        assert len(result["examples"]) > 0

    def test_best_practices_example_structure(self):
        """Verify each best practice example has required metadata."""
        from agentic_ai.rag import retrieve_rewrite_context

        result = retrieve_rewrite_context(
            bullet="Trained ML models using PyTorch",
            target_role="ML Engineer",
            k=1,
        )

        example = result["examples"][0]
        assert "reference_bullet" in example
        assert "domain" in example
        assert "role_type" in example
        assert "why_effective" in example

    def test_reset_indices_clears_cache(self):
        """Verify reset_indices clears the cached vector stores."""
        from agentic_ai.rag import reset_indices, _jd_vectorstore, _bp_vectorstore
        import agentic_ai.rag as rag_module

        reset_indices()
        assert rag_module._jd_vectorstore is None
        assert rag_module._bp_vectorstore is None


# ═══════════════════════════════════════════════════════
# RAG-ENHANCED GRAPH TESTS
# ═══════════════════════════════════════════════════════

class TestRAGGraph:
    """Verify the RAG-enhanced LangGraph workflow."""

    def test_rag_graph_compilation(self):
        """Verify the RAG workflow compiles without errors."""
        from agentic_ai.graph import rag_app

        assert rag_app is not None
        assert hasattr(rag_app, "invoke")

    def test_rag_pipeline_execution(self):
        """Verify the RAG pipeline executes end-to-end and populates rag_context."""
        from agentic_ai.graph import rag_app

        inputs = {
            "resume_text": SAMPLE_RESUME,
            "jd_text": SAMPLE_JOB_DESCRIPTION,
            "target_role": "AI Engineer",
        }

        result = rag_app.invoke(inputs)

        # Verify all state fields are populated
        assert "resume_skills" in result
        assert "jd_skills" in result
        assert "rag_context" in result
        assert "match_results" in result
        assert "rewrites" in result
        assert "final_report" in result

        # Verify RAG context was retrieved
        assert result["rag_context"] is not None
        assert "examples" in result["rag_context"]

        # Verify final report includes RAG flag
        report = result["final_report"]
        assert report["status"] == "success"
        assert report.get("rag_enhanced") is True


# ═══════════════════════════════════════════════════════
# FASTAPI API TESTS
# ═══════════════════════════════════════════════════════

class TestFastAPIEndpoints:
    """Verify FastAPI endpoint contracts and response structures."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        from fastapi.testclient import TestClient
        from agentic_ai.api import api_app
        return TestClient(api_app)

    def test_health_endpoint(self, client):
        """Verify health check returns 200 with expected structure."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "phase" in data

    def test_extract_skills_endpoint(self, client):
        """Verify skill extraction returns structured output."""
        response = client.post("/api/v1/extract-skills", json={
            "text": SAMPLE_RESUME,
            "source_type": "resume",
        })
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert data["source_type"] == "resume"
        assert "skills" in data

    def test_evaluate_endpoint(self, client):
        """Verify full evaluation pipeline returns a complete report."""
        response = client.post("/api/v1/evaluate", json={
            "resume_text": SAMPLE_RESUME,
            "jd_text": SAMPLE_JOB_DESCRIPTION,
            "target_role": "AI Engineer",
        })
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert data["target_role"] == "AI Engineer"
        assert data["match_results"] is not None
        assert data["rewrites"] is not None

    def test_evaluate_rag_endpoint(self, client):
        """Verify RAG-enhanced evaluation works with auto-retrieved JD."""
        response = client.post("/api/v1/evaluate/rag", json={
            "resume_text": SAMPLE_RESUME,
            "target_role": "AI Engineer",
        })
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert data["rag_enhanced"] is True

    def test_similar_jds_endpoint(self, client):
        """Verify similar JDs endpoint returns results."""
        response = client.post("/api/v1/similar-jds", json={
            "resume_text": SAMPLE_RESUME,
            "k": 2,
        })
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert len(data["similar_jds"]) > 0
        assert data["count"] > 0

    def test_rewrite_bullets_endpoint(self, client):
        """Verify bullet rewrite endpoint returns structured output."""
        response = client.post("/api/v1/rewrite-bullets", json={
            "bullet_points": [
                "Built REST APIs using FastAPI",
                "Managed PostgreSQL databases",
            ],
            "target_role": "Backend Engineer",
            "missing_skills": ["Kubernetes"],
            "use_rag": False,
        })
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert "rewrites" in data

    def test_rewrite_bullets_with_rag(self, client):
        """Verify bullet rewrite with RAG context."""
        response = client.post("/api/v1/rewrite-bullets", json={
            "bullet_points": ["Implemented ML models using PyTorch"],
            "target_role": "ML Engineer",
            "use_rag": True,
        })
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert data["rag_enhanced"] is True

    def test_invalid_request_returns_422(self, client):
        """Verify validation errors return 422."""
        response = client.post("/api/v1/extract-skills", json={
            "text": "short",  # Too short (min_length=20)
            "source_type": "resume",
        })
        assert response.status_code == 422


# ═══════════════════════════════════════════════════════
# HITL GRAPH TESTS
# ═══════════════════════════════════════════════════════

class TestHITLPipeline:
    """Verify Human-in-the-Loop graph compilation, interrupt, and resume."""

    def test_hitl_graph_compilation(self):
        """Verify the HITL workflow compiles with a checkpointer."""
        from langgraph.checkpoint.memory import MemorySaver
        from agentic_ai.graph import compile_hitl_workflow

        checkpointer = MemorySaver()
        hitl_app = compile_hitl_workflow(checkpointer=checkpointer)

        assert hitl_app is not None
        assert hasattr(hitl_app, "invoke")

    def test_hitl_interrupt_and_resume(self):
        """Verify the HITL graph pauses at the review node and resumes with approval."""
        from langgraph.checkpoint.memory import MemorySaver
        from langgraph.types import Command
        from agentic_ai.graph import compile_hitl_workflow

        checkpointer = MemorySaver()
        hitl_app = compile_hitl_workflow(checkpointer=checkpointer)

        inputs = {
            "resume_text": SAMPLE_RESUME,
            "jd_text": SAMPLE_JOB_DESCRIPTION,
            "target_role": "AI Engineer",
        }
        config = {"configurable": {"thread_id": "test-hitl-1"}}

        # First invoke — should run up to the interrupt
        result = hitl_app.invoke(inputs, config=config)

        # Verify state has pending rewrites
        state = hitl_app.get_state(config)
        assert state.values.get("rewrites") is not None
        assert state.values.get("match_results") is not None

        # Resume with human approval
        final_result = hitl_app.invoke(
            Command(resume={
                "approval": "approved",
                "feedback": "Looks good!",
            }),
            config=config,
        )

        # Verify final report includes human review metadata
        report = final_result.get("final_report", {})
        assert report["status"] == "success"
        assert report.get("human_review") is not None
        assert report["human_review"]["approval"] == "approved"

    def test_hitl_state_propagation(self):
        """Verify that human approval metadata flows correctly to the final report."""
        from langgraph.checkpoint.memory import MemorySaver
        from langgraph.types import Command
        from agentic_ai.graph import compile_hitl_workflow

        checkpointer = MemorySaver()
        hitl_app = compile_hitl_workflow(checkpointer=checkpointer)

        inputs = {
            "resume_text": SAMPLE_RESUME,
            "jd_text": SAMPLE_JOB_DESCRIPTION,
            "target_role": "ML Engineer",
        }
        config = {"configurable": {"thread_id": "test-hitl-2"}}

        # Run to interrupt
        hitl_app.invoke(inputs, config=config)

        # Resume with rejection
        final_result = hitl_app.invoke(
            Command(resume={
                "approval": "rejected",
                "feedback": "Needs more quantified metrics.",
            }),
            config=config,
        )

        report = final_result.get("final_report", {})
        assert report["human_review"]["approval"] == "rejected"
        assert "metrics" in report["human_review"]["feedback"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
