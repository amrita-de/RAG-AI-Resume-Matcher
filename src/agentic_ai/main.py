"""Agentic AI Resume & Job Description Matcher - CLI Entrypoint.

Supports all phases:
  Phase 1: python -m agentic_ai.main                    (default — baseline evaluation)
  Phase 2: python -m agentic_ai.main --phase2            (tool demo)
  Phase 3: python -m agentic_ai.main --phase3            (LangGraph pipeline)
  Phase 4: python -m agentic_ai.main --phase4-api        (FastAPI server)
           python -m agentic_ai.main --phase4-rag        (RAG-enhanced pipeline demo)
           python -m agentic_ai.main --phase4-hitl       (HITL CLI demo)
"""

import sys
import argparse
from agentic_ai.sample_data import SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION
from agentic_ai.evaluator import evaluate_resume
from agentic_ai.parsers import parse_document


def print_evaluation_report(evaluation, provider_name: str) -> None:
    """Print beautifully formatted evaluation report to stdout."""
    sep = "=" * 70
    sub_sep = "-" * 70

    print("\n" + sep)
    print(f" AGENTIC AI RESUME EVALUATION REPORT  (Provider: {provider_name.upper()})")
    print(sep)
    print(f" Candidate:    {evaluation.candidate_name}")
    print(f" Target Role:  {evaluation.target_role}")
    print(f" Match Score:  {evaluation.overall_match_score} / 100")
    print(sub_sep)
    print(" SCORING RUBRIC BREAKDOWN:")
    print(f"   * Skills Coverage Score:     {evaluation.scoring_rubric.skills_score} / 100")
    print(f"   * Experience Relevance:      {evaluation.scoring_rubric.experience_score} / 100")
    print(f"   * Quantified Impact Score:   {evaluation.scoring_rubric.quantified_impact_score} / 100")
    print(f"   * Assessment Summary:        {evaluation.scoring_rubric.rubric_summary}")
    print(sub_sep)
    print(" SKILLS GAP ANALYSIS:")
    print(f"   [+] Matched Skills ({len(evaluation.skills_alignment.matched_skills)}):")
    for s in evaluation.skills_alignment.matched_skills:
        print(f"       - {s}")

    print(f"\n   [!] Missing Critical Skills ({len(evaluation.skills_alignment.missing_critical_skills)}):")
    for s in evaluation.skills_alignment.missing_critical_skills:
        print(f"       - {s}")

    print(f"\n   [?] Missing Preferred / Nice-to-Have ({len(evaluation.skills_alignment.missing_nice_to_have)}):")
    for s in evaluation.skills_alignment.missing_nice_to_have:
        print(f"       - {s}")

    print(sub_sep)
    print(" BULLET POINT OPTIMIZATIONS (Google XYZ Formula):")
    for idx, b in enumerate(evaluation.bullet_rewrites, 1):
        print(f"\n  #{idx}. Original:")
        print(f'     "{b.original}"')
        print(f"     Rewritten:")
        print(f'     "{b.improved}"')
        print(f"     Reasoning: {b.explanation}")
        if b.metrics_highlighted:
            print(f"     Metric Added: {b.metrics_highlighted}")

    print(sub_sep)
    print(" STRATEGIC RECRUITER VERDICT:")
    print(f"   {evaluation.strategic_advice}")
    print(sep + "\n")


def run_phase4_rag_demo():
    """Execute the Phase 4 RAG-enhanced pipeline demo."""
    from agentic_ai.graph import rag_app
    from agentic_ai.rag import retrieve_similar_jds

    sep = "=" * 70
    sub_sep = "-" * 70

    print("\n" + sep)
    print(" PHASE 4: RAG-ENHANCED PIPELINE DEMO")
    print(sep)

    # Step 1: Retrieve similar JDs
    print("\n[RAG] Retrieving similar JDs from FAISS index...")
    similar_jds = retrieve_similar_jds(SAMPLE_RESUME, k=3)
    for i, jd in enumerate(similar_jds, 1):
        print(f"  [{i}] {jd['title']} @ {jd['company']} (score: {jd['similarity_score']})")

    # Step 2: Run RAG-enhanced pipeline
    print(f"\n[RAG] Running RAG-enhanced LangGraph pipeline...")
    inputs = {
        "resume_text": SAMPLE_RESUME,
        "jd_text": SAMPLE_JOB_DESCRIPTION,
        "target_role": "Senior AI / Full Stack Engineer",
    }

    result = rag_app.invoke(inputs)
    report = result.get("final_report", {})
    match = report.get("match_results", {})
    rewrites = report.get("rewrites", {})

    print(f"\n{sub_sep}")
    print(" RAG-ENHANCED EVALUATION COMPLETE")
    print(sub_sep)

    print(f"  RAG Enhanced:        {report.get('rag_enhanced', False)}")
    print(f"  Target Role:         {report.get('target_role')}")
    print(f"  Overall Match Score: {match.get('overall_score')} / 100")
    print(f"  Skills Score:        {match.get('skills_score')} / 100")

    print(f"\n  Bullet Rewrites ({len(rewrites.get('rewritten_bullets', []))}):")
    for idx, bullet in enumerate(rewrites.get("rewritten_bullets", []), 1):
        print(f"\n  #{idx}. Original:  \"{bullet.get('original')}\"")
        print(f"     Rewritten: \"{bullet.get('rewritten')}\"")

    print(f"\n  Strategic Summary:")
    print(f"    {rewrites.get('strategic_summary')}")

    print(f"\n{sep}")
    print(" Phase 4 RAG Demo Complete.")
    print(sep + "\n")


def run_phase4_hitl_demo():
    """Execute the Phase 4 HITL pipeline demo (simulated approval in CLI)."""
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.types import Command
    from agentic_ai.graph import compile_hitl_workflow

    sep = "=" * 70
    sub_sep = "-" * 70

    print("\n" + sep)
    print(" PHASE 4: HUMAN-IN-THE-LOOP PIPELINE DEMO")
    print(sep)

    checkpointer = MemorySaver()
    hitl_app = compile_hitl_workflow(checkpointer=checkpointer)

    inputs = {
        "resume_text": SAMPLE_RESUME,
        "jd_text": SAMPLE_JOB_DESCRIPTION,
        "target_role": "Senior AI / Full Stack Engineer",
    }

    config = {"configurable": {"thread_id": "hitl-demo-1"}}

    print("\n[HITL] Running pipeline to human review gate...")
    result = hitl_app.invoke(inputs, config=config)

    # Get state at interrupt
    state = hitl_app.get_state(config)
    pending_rewrites = state.values.get("rewrites", {})

    print(f"\n{sub_sep}")
    print(" PIPELINE PAUSED — AWAITING HUMAN REVIEW")
    print(sub_sep)
    print(f"  Match Score: {state.values.get('match_results', {}).get('overall_score')} / 100")
    print(f"\n  Pending Rewrites:")
    for idx, bullet in enumerate(pending_rewrites.get("rewritten_bullets", []), 1):
        print(f"    #{idx}. \"{bullet.get('rewritten', '')}\"")

    # Simulate human approval
    print(f"\n  [HUMAN REVIEWER] Approving all rewrites...")
    human_input = {
        "approval": "approved",
        "feedback": "Rewrites look great — strong action verbs and quantified metrics.",
    }

    print(f"\n[HITL] Resuming pipeline with human approval...")
    final_result = hitl_app.invoke(
        Command(resume=human_input),
        config=config,
    )

    report = final_result.get("final_report", {})

    print(f"\n{sub_sep}")
    print(" HITL PIPELINE COMPLETE — FINAL REPORT")
    print(sub_sep)
    print(f"  Status:        {report.get('status')}")
    print(f"  Target Role:   {report.get('target_role')}")
    human_review = report.get("human_review", {})
    print(f"  Human Review:  {human_review.get('approval', 'N/A')}")
    print(f"  Feedback:      {human_review.get('feedback', 'N/A')}")

    print(f"\n{sep}")
    print(" Phase 4 HITL Demo Complete.")
    print(sep + "\n")


def main() -> None:
    """Main execution function — unified CLI entry point for all phases."""
    parser = argparse.ArgumentParser(
        description="Agentic AI Resume & JD Matcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--phase2", action="store_true", help="Run Phase 2 tool demo")
    parser.add_argument("--phase3", action="store_true", help="Run Phase 3 LangGraph demo")
    parser.add_argument("--phase4-api", action="store_true", help="Launch Phase 4 FastAPI server")
    parser.add_argument("--phase4-rag", action="store_true", help="Run Phase 4 RAG-enhanced demo")
    parser.add_argument("--phase4-hitl", action="store_true", help="Run Phase 4 HITL demo")
    args = parser.parse_args()

    if args.phase2:
        from agentic_ai.tool_runner import run_tool_demo
        run_tool_demo()
    elif args.phase3:
        from agentic_ai.graph_runner import run_graph_demo
        run_graph_demo()
    elif args.phase4_api:
        import uvicorn
        print("[Phase 4] Launching FastAPI server...")
        print("[Phase 4] Swagger docs: http://localhost:8000/docs")
        uvicorn.run("agentic_ai.api:api_app", host="0.0.0.0", port=8000, reload=True)
    elif args.phase4_rag:
        run_phase4_rag_demo()
    elif args.phase4_hitl:
        run_phase4_hitl_demo()
    else:
        # Default: Phase 1
        print("[Phase 1 Runner] Initializing Document Parser & Evaluation Pipeline...")

        print("[Phase 1 Runner] Validating document text extraction...")
        resume_text = SAMPLE_RESUME
        jd_text = SAMPLE_JOB_DESCRIPTION

        print(f"[Phase 1 Runner] Parsed Resume Length: {len(resume_text)} characters")
        print(f"[Phase 1 Runner] Parsed JD Length:     {len(jd_text)} characters")

        print("[Phase 1 Runner] Invoking Structured LLM Evaluation Chain...")
        report, provider = evaluate_resume(resume_text, jd_text)

        print_evaluation_report(report, provider)
        print("[Phase 1 Runner] Phase 1 Execution Succeeded.")


if __name__ == "__main__":
    main()
