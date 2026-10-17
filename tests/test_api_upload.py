"""Automated verification tests for the file upload endpoint (Step 5).

Tests multipart file upload with PDF, DOCX, TXT files across
standard, RAG, and HITL pipeline modes.
"""

import io
import pytest
import docx
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from agentic_ai.sample_data import SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from agentic_ai.api import api_app
    return TestClient(api_app)


def _make_test_pdf() -> bytes:
    """Generate an in-memory PDF resume for testing."""
    bio = io.BytesIO()
    doc = SimpleDocTemplate(bio, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Jane Doe - Senior AI Engineer", styles["Title"]),
        Paragraph(
            "Experienced in Python, PyTorch, LangChain, and FastAPI microservices. "
            "Built production ML pipelines serving 500K+ daily predictions. "
            "Led migration of monolithic Django application to FastAPI microservices "
            "architecture with Docker and Kubernetes, reducing deployment time by 60%. "
            "Designed real-time recommendation engine processing 10M events/day using Apache Kafka and Redis.",
            styles["Normal"],
        ),
    ]
    doc.build(story)
    bio.seek(0)
    return bio.read()


def _make_test_docx() -> bytes:
    """Generate an in-memory DOCX resume for testing."""
    doc = docx.Document()
    doc.add_paragraph("John Smith - Full Stack Developer")
    doc.add_paragraph(
        "Expert in React, TypeScript, Node.js, and PostgreSQL. "
        "Built scalable SaaS dashboard serving 100K monthly active users. "
        "Implemented CI/CD pipeline with GitHub Actions reducing deployment errors by 80%. "
        "Designed and deployed real-time notification system using WebSockets and Redis Pub/Sub."
    )
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.read()


class TestUploadEndpoint:
    """Tests for POST /api/v1/upload-and-evaluate."""

    def test_upload_txt_file(self, client):
        """Verify plain text resume upload works with standard pipeline."""
        resume_bytes = SAMPLE_RESUME.encode("utf-8")
        response = client.post(
            "/api/v1/upload-and-evaluate",
            files={"resume_file": ("resume.txt", resume_bytes, "text/plain")},
            data={
                "jd_text": SAMPLE_JOB_DESCRIPTION,
                "target_role": "AI Engineer",
                "pipeline_type": "standard",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["target_role"] == "AI Engineer"
        assert data["match_results"] is not None
        assert data["rewrites"] is not None

    def test_upload_pdf_file(self, client):
        """Verify PDF resume upload is parsed and evaluated."""
        pdf_bytes = _make_test_pdf()
        response = client.post(
            "/api/v1/upload-and-evaluate",
            files={"resume_file": ("resume.pdf", pdf_bytes, "application/pdf")},
            data={
                "jd_text": SAMPLE_JOB_DESCRIPTION,
                "target_role": "AI Engineer",
                "pipeline_type": "standard",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["match_results"] is not None

    def test_upload_docx_file(self, client):
        """Verify DOCX resume upload is parsed and evaluated."""
        docx_bytes = _make_test_docx()
        response = client.post(
            "/api/v1/upload-and-evaluate",
            files={"resume_file": ("resume.docx", docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            data={
                "jd_text": SAMPLE_JOB_DESCRIPTION,
                "target_role": "Full Stack Developer",
                "pipeline_type": "standard",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_upload_unsupported_file_type(self, client):
        """Verify unsupported file types are rejected with 400."""
        response = client.post(
            "/api/v1/upload-and-evaluate",
            files={"resume_file": ("image.png", b"fake image data", "image/png")},
            data={
                "jd_text": SAMPLE_JOB_DESCRIPTION,
                "target_role": "AI Engineer",
            },
        )
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]

    def test_upload_rag_pipeline(self, client):
        """Verify file upload with RAG pipeline mode returns rag_enhanced=True."""
        resume_bytes = SAMPLE_RESUME.encode("utf-8")
        response = client.post(
            "/api/v1/upload-and-evaluate",
            files={"resume_file": ("resume.txt", resume_bytes, "text/plain")},
            data={
                "jd_text": SAMPLE_JOB_DESCRIPTION,
                "target_role": "AI Engineer",
                "pipeline_type": "rag",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["rag_enhanced"] is True


class TestSampleDataEndpoint:
    """Tests for GET /api/v1/sample-data."""

    def test_sample_data_returns_fixtures(self, client):
        """Verify sample data endpoint returns resume and JD text."""
        response = client.get("/api/v1/sample-data")
        assert response.status_code == 200
        data = response.json()
        assert "resume_text" in data
        assert "jd_text" in data
        assert "target_role" in data
        assert len(data["resume_text"]) > 100
        assert len(data["jd_text"]) > 100
