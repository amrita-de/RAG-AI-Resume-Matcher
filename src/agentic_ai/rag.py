"""Phase 4: RAG Engine — FAISS vector indexing and semantic retrieval.

Provides two independent retrieval pipelines:
1. JD Retrieval: Given a resume, find the most relevant job descriptions from an indexed corpus.
2. Best Practices Retrieval: Given a bullet point and target role, find curated XYZ formula
   examples to ground the LLM's rewrite suggestions in real, high-quality patterns.

Embedding Model:
    Uses HuggingFace 'all-MiniLM-L6-v2' — a free, local model requiring no API key.
    This ensures offline CI/CD compatibility and zero embedding costs.

Architecture:
    ┌──────────────┐    ┌───────────────────┐    ┌─────────────────┐
    │ rag_data.py  │──▶ │ build_*_index()   │──▶ │ FAISS VectorDB  │
    │ (corpus)     │    │ (embed + index)   │    │ (in-memory)     │
    └──────────────┘    └───────────────────┘    └────────┬────────┘
                                                          │
                        ┌───────────────────┐             │
                        │ retrieve_*()      │◀────────────┘
                        │ (query → top-k)   │
                        └───────────────────┘
"""

import os
import logging
from typing import Optional

from agentic_ai.rag_data import SAMPLE_JD_CORPUS, BEST_PRACTICES_CORPUS

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────
# Module-level caches for singleton indices
# ─────────────────────────────────────────────────────────
_jd_vectorstore = None
_bp_vectorstore = None


# ─────────────────────────────────────────────────────────
# Embedding Model Factory
# ─────────────────────────────────────────────────────────

def get_embeddings():
    """Return a HuggingFace embedding model for local, free embedding generation.

    Uses 'all-MiniLM-L6-v2' — a lightweight 384-dimensional model optimized for
    semantic similarity. Runs entirely locally with no API key required.

    Returns:
        HuggingFaceEmbeddings instance, or None if sentence-transformers is not installed.
    """
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    except ImportError:
        logger.warning(
            "sentence-transformers or langchain-huggingface not installed. "
            "RAG features will use mock fallbacks."
        )
        return None


# ═══════════════════════════════════════════════════════
# JD CORPUS INDEXING & RETRIEVAL
# ═══════════════════════════════════════════════════════

def build_jd_index(jd_corpus: list[dict] | None = None):
    """Embed and index a corpus of job descriptions into a FAISS vector store.

    Args:
        jd_corpus: List of JD dicts with 'title', 'company', 'domain', 'text' keys.
                   Defaults to SAMPLE_JD_CORPUS if not provided.

    Returns:
        FAISS vector store instance, or None if embeddings are unavailable.
    """
    global _jd_vectorstore

    if _jd_vectorstore is not None:
        return _jd_vectorstore

    if jd_corpus is None:
        jd_corpus = SAMPLE_JD_CORPUS

    embeddings = get_embeddings()
    if embeddings is None:
        logger.warning("Skipping JD index build — no embedding model available.")
        return None

    try:
        from langchain_community.vectorstores import FAISS
        from langchain_core.documents import Document

        documents = [
            Document(
                page_content=jd["text"],
                metadata={
                    "title": jd["title"],
                    "company": jd["company"],
                    "domain": jd.get("domain", "General"),
                },
            )
            for jd in jd_corpus
        ]

        _jd_vectorstore = FAISS.from_documents(documents, embeddings)
        logger.info(f"Built JD FAISS index with {len(documents)} documents.")
        return _jd_vectorstore

    except Exception as e:
        logger.error(f"Failed to build JD index: {e}")
        return None


def retrieve_similar_jds(resume_text: str, k: int = 3) -> list[dict]:
    """Given resume text, retrieve the top-k most semantically similar job descriptions.

    Args:
        resume_text: Raw text of the candidate's resume.
        k: Number of similar JDs to retrieve (default: 3).

    Returns:
        List of dicts with 'title', 'company', 'domain', 'text', and 'similarity_score'.
        Falls back to mock data if the index is unavailable.
    """
    index = build_jd_index()

    if index is None:
        return _mock_retrieve_similar_jds(k)

    try:
        results = index.similarity_search_with_score(resume_text, k=k)
        return [
            {
                "title": doc.metadata.get("title", "Unknown"),
                "company": doc.metadata.get("company", "Unknown"),
                "domain": doc.metadata.get("domain", "General"),
                "text": doc.page_content,
                "similarity_score": round(float(score), 4),
            }
            for doc, score in results
        ]
    except Exception as e:
        logger.error(f"JD retrieval failed: {e}")
        return _mock_retrieve_similar_jds(k)


def _mock_retrieve_similar_jds(k: int = 3) -> list[dict]:
    """Deterministic fallback for JD retrieval when embeddings are unavailable."""
    mock_results = []
    for jd in SAMPLE_JD_CORPUS[:k]:
        mock_results.append({
            "title": jd["title"],
            "company": jd["company"],
            "domain": jd.get("domain", "General"),
            "text": jd["text"],
            "similarity_score": 0.85,
        })
    return mock_results


# ═══════════════════════════════════════════════════════
# BEST PRACTICES INDEXING & RETRIEVAL
# ═══════════════════════════════════════════════════════

def build_best_practices_index():
    """Embed and index curated resume bullet best practices into a FAISS vector store.

    The index enables retrieval of high-quality XYZ formula examples relevant to
    a specific bullet point and target role, grounding the LLM's rewrite suggestions.

    Returns:
        FAISS vector store instance, or None if embeddings are unavailable.
    """
    global _bp_vectorstore

    if _bp_vectorstore is not None:
        return _bp_vectorstore

    embeddings = get_embeddings()
    if embeddings is None:
        logger.warning("Skipping best practices index build — no embedding model available.")
        return None

    try:
        from langchain_community.vectorstores import FAISS
        from langchain_core.documents import Document

        documents = [
            Document(
                page_content=bp["bullet"],
                metadata={
                    "domain": bp["domain"],
                    "role_type": bp["role_type"],
                    "why_effective": bp["why_effective"],
                },
            )
            for bp in BEST_PRACTICES_CORPUS
        ]

        _bp_vectorstore = FAISS.from_documents(documents, embeddings)
        logger.info(f"Built best practices FAISS index with {len(documents)} documents.")
        return _bp_vectorstore

    except Exception as e:
        logger.error(f"Failed to build best practices index: {e}")
        return None


def retrieve_rewrite_context(
    bullet: str,
    target_role: str,
    k: int = 3,
) -> dict:
    """Retrieve relevant best practice examples for grounding bullet rewrites.

    Combines the bullet text and target role into a retrieval query, then fetches
    the most relevant curated XYZ formula examples from the best practices index.

    Args:
        bullet: The original bullet point text to find similar examples for.
        target_role: The title of the target role being applied for.
        k: Number of examples to retrieve (default: 3).

    Returns:
        Dict with 'examples' (list of relevant bullet examples with metadata)
        and 'target_role'.
    """
    index = build_best_practices_index()

    query = f"Role: {target_role}. Bullet: {bullet}"

    if index is None:
        return _mock_retrieve_rewrite_context(target_role, k)

    try:
        results = index.similarity_search_with_score(query, k=k)
        examples = [
            {
                "reference_bullet": doc.page_content,
                "domain": doc.metadata.get("domain", "General"),
                "role_type": doc.metadata.get("role_type", "Engineer"),
                "why_effective": doc.metadata.get("why_effective", ""),
                "similarity_score": round(float(score), 4),
            }
            for doc, score in results
        ]
        return {
            "target_role": target_role,
            "examples": examples,
        }

    except Exception as e:
        logger.error(f"Best practices retrieval failed: {e}")
        return _mock_retrieve_rewrite_context(target_role, k)


def _mock_retrieve_rewrite_context(target_role: str, k: int = 3) -> dict:
    """Deterministic fallback for best practices retrieval."""
    mock_examples = []
    for bp in BEST_PRACTICES_CORPUS[:k]:
        mock_examples.append({
            "reference_bullet": bp["bullet"],
            "domain": bp["domain"],
            "role_type": bp["role_type"],
            "why_effective": bp["why_effective"],
            "similarity_score": 0.80,
        })
    return {
        "target_role": target_role,
        "examples": mock_examples,
    }


# ═══════════════════════════════════════════════════════
# INDEX MANAGEMENT
# ═══════════════════════════════════════════════════════

def reset_indices():
    """Clear cached FAISS indices. Useful for testing or re-indexing with new data."""
    global _jd_vectorstore, _bp_vectorstore
    _jd_vectorstore = None
    _bp_vectorstore = None
    logger.info("RAG indices cleared.")
