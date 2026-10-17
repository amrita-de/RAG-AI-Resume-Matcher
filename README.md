# Agentic AI Resume & Job Description Matcher

An enterprise-grade, multi-agent AI pipeline and interactive web application designed to evaluate resumes against job descriptions with high precision. Built with **LangGraph**, **FastAPI**, **FAISS Vector Search (RAG)**, and **React + Vite**, this system provides automated skill extraction, ATS scoring, Human-in-the-Loop (HITL) review gates, and Google XYZ-formula bullet point rewrites.

---

## Architecture Overview

- **Phase 1 (Baseline Structured Evaluator):** Direct LLM structured output evaluation utilizing Pydantic schemas and deterministic fallback mode.
- **Phase 2 (Specialized Tool Suite):** Modular tool functions for `extract_skills`, `compute_match_score`, and `suggest_rewrite`.
- **Phase 3 (LangGraph Orchestration):** State graph pipeline with parallel resume/JD parsing, scoring, and bullet optimization.
- **Phase 4 (Production API, RAG & HITL):**
  - **FastAPI REST API:** Full OpenAPI/Swagger interactive endpoints.
  - **FAISS RAG Engine:** Embedding-based retrieval of benchmark job descriptions and high-impact resume phrasing.
  - **Human-in-the-Loop (HITL):** State checkpointing (`MemorySaver`) with review gates to approve or modify rewritten bullets.
  - **React Dashboard:** Modern glassmorphism UI with live progress indicators, score gauges, skills gap chips, and PDF/DOCX/TXT upload.

---

## Quick Start: Running the Project

Both the backend and frontend can be run locally on your machine.

### 1. Configure Environment Variables

Copy `.env.example` to `.env` and configure your preferred LLM provider:

```bash
# Option 1: Groq (Recommended - fast inference)
GROQ_API_KEY=gsk_...
GROQ_MODEL=qwen/qwen3.8-27b

# Option 2: Google Gemini
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-1.5-flash

# Option 3: OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

*(Note: If no API keys are provided, the system seamlessly uses a deterministic mock evaluator for testing.)*

---

### 2. Running the Web Application (Recommended)

#### Start the FastAPI Backend:
```bash
uv run uvicorn agentic_ai.api:app --reload --host 127.0.0.1 --port 8000
```
- **Backend API:** `http://127.0.0.1:8000`
- **Swagger / OpenAPI Documentation:** `http://127.0.0.1:8000/docs`

#### Start the React Frontend:
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
- **Web UI:** `http://localhost:5173`

---

### 3. Running Phase CLI Demos

You can execute individual pipeline phases directly from the terminal using `uv`:

```bash
# Phase 1: Baseline Evaluation Demo
uv run python -m agentic_ai.main

# Phase 2: Modular Tool Execution Demo
uv run python -m agentic_ai.main --phase2

# Phase 3: LangGraph Pipeline Execution Demo
uv run python -m agentic_ai.main --phase3

# Phase 4: RAG-Enhanced LangGraph Pipeline Demo
uv run python -m agentic_ai.main --phase4-rag

# Phase 4: Human-in-the-Loop (HITL) Approval Demo
uv run python -m agentic_ai.main --phase4-hitl

# Phase 4: Launch FastAPI Server
uv run python -m agentic_ai.main --phase4-api
```

---

### 4. Running the Test Suite

Run all verification tests across all phases and endpoints:

```bash
uv run pytest
```
