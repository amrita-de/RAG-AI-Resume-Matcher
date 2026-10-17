"""Phase 4: Curated data corpora for RAG vector store indexing.

Provides two data sets:
1. SAMPLE_JD_CORPUS — Diverse job descriptions for semantic JD retrieval
2. BEST_PRACTICES_CORPUS — Curated resume bullet examples following the XYZ formula,
   used to ground the suggest_rewrite tool in real, high-quality patterns.
"""


# ─────────────────────────────────────────────────────────
# 1. Sample JD Corpus for Vector Indexing
# ─────────────────────────────────────────────────────────

SAMPLE_JD_CORPUS = [
    {
        "title": "Senior AI / Full Stack Engineer",
        "company": "CloudScale AI",
        "domain": "AI/Full-Stack",
        "text": (
            "We are seeking an experienced Senior AI / Full Stack Engineer to architect and build our "
            "next-generation Agentic AI workflow platform. You will design autonomous agent systems, "
            "integrate retrieval-augmented generation (RAG), and create high-performance web interfaces "
            "for enterprise users.\n\n"
            "Responsibilities:\n"
            "- Architect and deploy agentic AI pipelines using LangGraph, LangChain, and modern LLM APIs.\n"
            "- Build production-grade vector search and RAG subsystems using FAISS, Qdrant, or Pinecone.\n"
            "- Design and scale asynchronous backend services in Python using FastAPI, Celery, and PostgreSQL.\n"
            "- Develop interactive frontend interfaces in React/TypeScript with real-time streaming.\n"
            "- Optimize system latency, token consumption, and model inference costs.\n\n"
            "Required: 3+ years Python, FastAPI, React/TypeScript, LangChain/LangGraph, Docker.\n"
            "Preferred: Kubernetes, RAGAS, LangSmith, prompt caching."
        ),
    },
    {
        "title": "Machine Learning Engineer",
        "company": "NeuralForge Labs",
        "domain": "ML Engineering",
        "text": (
            "Join our ML platform team to design, train, and deploy production machine learning models "
            "at scale. You will work on end-to-end ML pipelines from data ingestion to model serving.\n\n"
            "Responsibilities:\n"
            "- Build and optimize ML training pipelines using PyTorch, TensorFlow, and Hugging Face Transformers.\n"
            "- Design feature engineering pipelines with Spark, Airflow, and dbt.\n"
            "- Deploy models via TorchServe, Triton Inference Server, or custom FastAPI endpoints.\n"
            "- Implement A/B testing frameworks and model monitoring dashboards.\n"
            "- Optimize model inference latency and GPU utilization in Kubernetes clusters.\n\n"
            "Required: 3+ years ML engineering, Python, PyTorch, Docker, Kubernetes.\n"
            "Preferred: MLflow, Weights & Biases, distributed training, ONNX optimization."
        ),
    },
    {
        "title": "Backend Engineer (Python)",
        "company": "FinEdge Systems",
        "domain": "Backend",
        "text": (
            "We need a strong Backend Engineer to build and maintain mission-critical financial "
            "transaction processing systems handling millions of daily events.\n\n"
            "Responsibilities:\n"
            "- Design and implement high-throughput REST and gRPC APIs using FastAPI and Python.\n"
            "- Build event-driven architectures with Kafka, RabbitMQ, and Redis Streams.\n"
            "- Manage PostgreSQL databases with advanced query optimization and partitioning.\n"
            "- Implement distributed tracing, structured logging, and alerting pipelines.\n"
            "- Write comprehensive unit, integration, and load tests.\n\n"
            "Required: 4+ years Python, FastAPI/Django, PostgreSQL, Redis, Docker.\n"
            "Preferred: Kafka, Kubernetes, gRPC, financial domain experience."
        ),
    },
    {
        "title": "DevOps / Platform Engineer",
        "company": "InfraCore",
        "domain": "DevOps",
        "text": (
            "As a Platform Engineer, you will build and maintain the developer platform powering "
            "our engineering teams across 50+ microservices.\n\n"
            "Responsibilities:\n"
            "- Design and manage Kubernetes clusters on AWS EKS with Terraform and Helm.\n"
            "- Build CI/CD pipelines using GitHub Actions, ArgoCD, and Docker.\n"
            "- Implement observability stacks with Prometheus, Grafana, and OpenTelemetry.\n"
            "- Automate infrastructure provisioning, secret management, and compliance controls.\n"
            "- Optimize cloud costs and resource utilization across development and production.\n\n"
            "Required: 3+ years DevOps, Kubernetes, Terraform, AWS, Docker.\n"
            "Preferred: GitOps, service mesh (Istio), cost optimization, SRE practices."
        ),
    },
    {
        "title": "Full Stack Developer (React + Node.js)",
        "company": "Veloxa Digital",
        "domain": "Full-Stack",
        "text": (
            "Build beautiful, performant web applications for our SaaS analytics platform used by "
            "10,000+ enterprise customers.\n\n"
            "Responsibilities:\n"
            "- Develop responsive frontend applications using React, TypeScript, and Next.js.\n"
            "- Build scalable GraphQL and REST APIs using Node.js, Express, and PostgreSQL.\n"
            "- Implement real-time data streaming with WebSockets and Server-Sent Events.\n"
            "- Design and optimize database schemas for multi-tenant SaaS architecture.\n"
            "- Write end-to-end tests with Playwright and unit tests with Jest.\n\n"
            "Required: 3+ years React, TypeScript, Node.js, PostgreSQL.\n"
            "Preferred: Next.js, GraphQL, Redis, Docker, Tailwind CSS."
        ),
    },
]


# ─────────────────────────────────────────────────────────
# 2. Best Practices Corpus for Resume Bullet Grounding
# ─────────────────────────────────────────────────────────

BEST_PRACTICES_CORPUS = [
    # ── AI / ML Domain ──
    {
        "domain": "AI/ML",
        "role_type": "AI Engineer",
        "bullet": (
            "Architected a multi-agent RAG pipeline using LangGraph and FAISS, reducing hallucination rate "
            "by 40% and improving answer relevance scores from 0.72 to 0.91 across 15,000 enterprise queries."
        ),
        "why_effective": (
            "Demonstrates XYZ formula: accomplished (RAG pipeline), measured by (40% hallucination reduction, "
            "relevance score improvement), by doing (LangGraph + FAISS). Includes both relative and absolute metrics."
        ),
    },
    {
        "domain": "AI/ML",
        "role_type": "ML Engineer",
        "bullet": (
            "Optimized transformer model inference latency from 340ms to 85ms per request by implementing "
            "ONNX quantization and dynamic batching on Triton Inference Server, supporting 2,000 concurrent users."
        ),
        "why_effective": (
            "Strong action verb (Optimized), concrete before/after metrics (340ms → 85ms), "
            "technical depth (ONNX, dynamic batching, Triton), and scale context (2,000 concurrent users)."
        ),
    },
    {
        "domain": "AI/ML",
        "role_type": "AI Engineer",
        "bullet": (
            "Engineered a hybrid retrieval system combining BM25 keyword search with dense vector embeddings, "
            "achieving 94% top-5 recall on a 500K-document knowledge base and reducing support ticket resolution time by 35%."
        ),
        "why_effective": (
            "Combines technical implementation detail (BM25 + dense vectors) with business impact "
            "(35% faster ticket resolution) and precision metric (94% recall)."
        ),
    },
    # ── Full-Stack Domain ──
    {
        "domain": "Full-Stack",
        "role_type": "Full Stack Engineer",
        "bullet": (
            "Pioneered migration of 12 legacy React class components to Next.js 14 Server Components, "
            "reducing initial page load time by 60% (3.2s → 1.3s) and improving Core Web Vitals LCP score to 'Good'."
        ),
        "why_effective": (
            "Quantifies scope (12 components), measures impact (60% load time reduction with exact ms), "
            "and references industry-standard metrics (Core Web Vitals LCP)."
        ),
    },
    {
        "domain": "Full-Stack",
        "role_type": "Full Stack Engineer",
        "bullet": (
            "Designed and deployed a real-time collaborative editing feature using WebSockets and Redis Pub/Sub, "
            "supporting 500+ simultaneous editors with sub-50ms synchronization latency."
        ),
        "why_effective": (
            "Shows system design capability (WebSockets + Redis Pub/Sub), scale (500+ editors), "
            "and performance SLA (sub-50ms latency)."
        ),
    },
    # ── Backend Domain ──
    {
        "domain": "Backend",
        "role_type": "Backend Engineer",
        "bullet": (
            "Engineered asynchronous FastAPI microservices processing 120K daily financial transactions "
            "with sub-80ms P99 latency and 99.97% uptime over a 6-month production window."
        ),
        "why_effective": (
            "Combines throughput (120K daily), latency SLA (P99 < 80ms), reliability (99.97% uptime), "
            "and timeframe (6 months) — all verifiable claims."
        ),
    },
    {
        "domain": "Backend",
        "role_type": "Backend Engineer",
        "bullet": (
            "Reduced PostgreSQL query execution time by 75% across 8 critical API endpoints by implementing "
            "composite indexes, query plan analysis, and connection pooling with PgBouncer."
        ),
        "why_effective": (
            "Specific scope (8 endpoints), clear metric (75% reduction), and technical depth "
            "(composite indexes, query plans, PgBouncer) showing database mastery."
        ),
    },
    {
        "domain": "Backend",
        "role_type": "Backend Engineer",
        "bullet": (
            "Architected an event-driven data pipeline using Kafka and Redis Streams, processing 5M+ "
            "daily events with exactly-once delivery semantics and automated dead-letter queue recovery."
        ),
        "why_effective": (
            "Demonstrates distributed systems expertise (Kafka, exactly-once semantics, DLQ), "
            "quantifies scale (5M+ events), and highlights reliability engineering."
        ),
    },
    # ── DevOps Domain ──
    {
        "domain": "DevOps",
        "role_type": "DevOps Engineer",
        "bullet": (
            "Automated Kubernetes cluster provisioning across 3 AWS regions using Terraform and Helm, "
            "reducing infrastructure deployment time from 4 hours to 12 minutes and eliminating manual configuration drift."
        ),
        "why_effective": (
            "Before/after metric (4 hours → 12 minutes), scope (3 regions), tools (Terraform, Helm), "
            "and business value (eliminated configuration drift)."
        ),
    },
    {
        "domain": "DevOps",
        "role_type": "Platform Engineer",
        "bullet": (
            "Built a unified CI/CD platform using GitHub Actions and ArgoCD serving 50+ microservices, "
            "reducing average deployment cycle from 45 minutes to 8 minutes with zero-downtime blue-green deploys."
        ),
        "why_effective": (
            "Scale (50+ microservices), before/after (45min → 8min), deployment strategy (blue-green), "
            "and reliability (zero-downtime)."
        ),
    },
    # ── Cross-Domain Impact Bullets ──
    {
        "domain": "General",
        "role_type": "Software Engineer",
        "bullet": (
            "Led a 4-person cross-functional team to deliver an internal developer portal 3 weeks ahead "
            "of schedule, reducing developer onboarding time from 2 weeks to 3 days across 80+ engineers."
        ),
        "why_effective": (
            "Shows leadership (4-person team), delivery excellence (3 weeks early), and measurable "
            "organizational impact (onboarding 2 weeks → 3 days for 80+ engineers)."
        ),
    },
    {
        "domain": "General",
        "role_type": "Software Engineer",
        "bullet": (
            "Implemented comprehensive observability stack using OpenTelemetry, Prometheus, and Grafana, "
            "reducing mean time to detection (MTTD) from 25 minutes to under 3 minutes for production incidents."
        ),
        "why_effective": (
            "Industry-standard metric (MTTD), dramatic improvement (25min → <3min), "
            "and specific tooling (OpenTelemetry, Prometheus, Grafana)."
        ),
    },
    {
        "domain": "AI/ML",
        "role_type": "AI Engineer",
        "bullet": (
            "Deployed a production LLM evaluation framework using RAGAS and LangSmith, continuously monitoring "
            "faithfulness, relevance, and toxicity scores across 50K+ weekly inference requests."
        ),
        "why_effective": (
            "Demonstrates LLM ops maturity (evaluation + monitoring), specific frameworks (RAGAS, LangSmith), "
            "scale (50K+ weekly), and multi-metric tracking."
        ),
    },
    {
        "domain": "Full-Stack",
        "role_type": "Full Stack Engineer",
        "bullet": (
            "Developed a server-side rendered analytics dashboard using Next.js and D3.js, reducing "
            "time-to-interactive by 55% and increasing daily active user engagement by 28% over 3 months."
        ),
        "why_effective": (
            "Technical specificity (SSR, Next.js, D3.js), performance metric (55% TTI reduction), "
            "and business outcome (28% engagement increase with timeframe)."
        ),
    },
    {
        "domain": "AI/ML",
        "role_type": "AI Engineer",
        "bullet": (
            "Reduced LLM API costs by 62% ($18K/month savings) by implementing semantic prompt caching, "
            "response streaming, and adaptive model routing between GPT-4o-mini and Claude 3 Haiku based on query complexity."
        ),
        "why_effective": (
            "Direct cost impact ($18K/month), percentage improvement (62%), and sophisticated "
            "optimization strategy (caching, streaming, adaptive routing)."
        ),
    },
]
