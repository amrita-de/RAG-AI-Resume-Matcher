"""Sample resume and job description fixtures for development and testing."""

SAMPLE_RESUME = """
AMRITA DE
Email: amrita.de@example.com | Phone: +91-9876543210 | Bengaluru, India
LinkedIn: linkedin.com/in/amritade | GitHub: github.com/amritade

PROFESSIONAL SUMMARY
Full Stack & AI Engineer with 3+ years of experience building responsive web applications and machine learning pipelines. Skilled in Python, React, TypeScript, FastAPI, and LangChain. Passionate about LLM agents, vector search, and scalable backend architectures.

TECHNICAL SKILLS
- Languages: Python, JavaScript, TypeScript, SQL, HTML/CSS
- Frameworks & Libraries: FastAPI, Flask, React.js, Next.js, LangChain, PyTorch, Tailwind CSS
- Databases & Vector Stores: PostgreSQL, MongoDB, Redis, FAISS, Pinecone
- Cloud & DevOps: Docker, AWS (S3, EC2), Git, GitHub Actions, Linux

WORK EXPERIENCE
Software Engineer | NexaTech Solutions (Bengaluru, India)
July 2023 – Present
- Built and maintained RESTful APIs using FastAPI and PostgreSQL handling 50k daily active requests.
- Developed an automated resume parsing service using LangChain and OpenAI API to speed up recruiter workflows.
- Improved frontend rendering performance by 30% by migrating core React dashboards to Next.js server components.
- Integrated FAISS vector database for semantic search over 20,000 product catalog entries.

Junior AI Developer | DataVerve Labs
August 2022 – June 2023
- Implemented document classification pipeline using fine-tuned BERT models in PyTorch.
- Created interactive data visualization dashboards using React and Chart.js for enterprise clients.
- Automated ETL pipelines processing 5GB of unstructured customer review data daily.

PROJECTS
Agentic RAG Knowledge Assistant
- Built an autonomous multi-agent research assistant using LangGraph and Groq API.
- Implemented hybrid search combining BM25 keyword search and dense vector retrieval with FAISS.

EDUCATION
B.Tech in Computer Science & Engineering | Visvesvaraya Technological University
2018 – 2022 | CGPA: 8.7/10
"""

SAMPLE_JOB_DESCRIPTION = """
Senior AI / Full Stack Engineer
Company: CloudScale AI
Location: Remote / Bengaluru

About the Role:
We are seeking an experienced Senior AI / Full Stack Engineer to architect and build our next-generation Agentic AI workflow platform. You will design autonomous agent systems, integrate retrieval-augmented generation (RAG), and create high-performance web interfaces for enterprise users.

Responsibilities:
- Architect and deploy agentic AI pipelines using LangGraph, LangChain, and modern LLM APIs (OpenAI, Claude, Gemini).
- Build production-grade vector search and RAG subsystems using FAISS, Qdrant, or Pinecone with real-time hybrid retrieval.
- Design and scale asynchronous backend services in Python using FastAPI, Celery, and PostgreSQL.
- Develop interactive, sleek frontend interfaces in React/TypeScript with real-time streaming (SSE / WebSockets).
- Optimize system latency, token consumption, and model inference costs in production Kubernetes/Docker environments.
- Implement CI/CD automation and automated evaluation rubrics for LLM outputs.

Required Qualifications:
- 3+ years of experience in Python, FastAPI, and modern frontend frameworks (React, TypeScript).
- Proven hands-on experience building production RAG systems, vector embeddings, and LangGraph/LangChain agents.
- Strong understanding of asynchronous programming, Redis caching, and relational databases (PostgreSQL).
- Familiarity with containerization (Docker) and cloud deployments on AWS or GCP.

Preferred / Bonus Skills:
- Experience with Kubernetes and microservices orchestration.
- Familiarity with evaluation frameworks (RAGAS, TruLens) and LLM observability (LangSmith, Phoenix).
- Experience optimizing token costs and latency through prompt caching and speculative decoding.
"""
