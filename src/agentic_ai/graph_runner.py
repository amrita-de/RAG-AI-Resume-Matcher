"""Phase 3: LangGraph runner harness — demonstrates the autonomous orchestration pipeline.

This script executes the full LangGraph workflow, passing the sample resume and JD
through the nodes and printing the aggregated final report.
"""

from agentic_ai.graph import app
from agentic_ai.sample_data import SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION


def run_graph_demo():
    """Execute the Phase 3 LangGraph pipeline and print the final report."""
    sep = "=" * 70
    sub_sep = "-" * 70

    print("\n" + sep)
    print(" PHASE 3: LANGGRAPH ORCHESTRATION PIPELINE DEMO")
    print(sep)
    
    # Define initial state
    inputs = {
        "resume_text": SAMPLE_RESUME,
        "jd_text": SAMPLE_JOB_DESCRIPTION,
        "target_role": "Senior AI / Full Stack Engineer",
    }
    
    print("\n[Orchestrator] Invoking LangGraph state machine...")
    print("[Orchestrator] Nodes executing: extract_resume & extract_jd -> compute_score -> optimize_bullets -> aggregate_report")
    
    # Run the graph
    result = app.invoke(inputs)
    
    # Extract final report
    report = result.get("final_report", {})
    match = report.get("match_results", {})
    rewrites = report.get("rewrites", {})
    
    print(f"\n{sub_sep}")
    print(" GRAPH EXECUTION COMPLETE - FINAL REPORT")
    print(sub_sep)
    
    print(f"  Target Role:         {report.get('target_role')}")
    print(f"  Overall Match Score: {match.get('overall_score')} / 100")
    print(f"  Skills Score:        {match.get('skills_score')} / 100")
    print(f"  Experience Score:    {match.get('experience_score')} / 100")
    print(f"  Impact Score:        {match.get('impact_score')} / 100")
    
    print(f"\n  Matched Skills ({len(match.get('matched_skills', []))}):")
    for s in match.get("matched_skills", [])[:5]:
        print(f"    [+] {s}")
    if len(match.get("matched_skills", [])) > 5:
        print("    [+] ...and others")
        
    print(f"\n  Missing Critical Skills ({len(match.get('missing_critical', []))}):")
    for s in match.get("missing_critical", []):
        print(f"    [-] {s}")
        
    print(f"\n  Scoring Rationale:")
    print(f"    {match.get('scoring_rationale')}")
    
    print(f"\n  Bullet Rewrites ({len(rewrites.get('rewritten_bullets', []))}):")
    for idx, bullet in enumerate(rewrites.get("rewritten_bullets", []), 1):
        print(f"\n  #{idx}. Original:  \"{bullet.get('original')}\"")
        print(f"     Rewritten: \"{bullet.get('rewritten')}\"")
        print(f"     Skills:    {', '.join(bullet.get('skills_addressed', []))}")
        
    print(f"\n  Strategic Summary:")
    print(f"    {rewrites.get('strategic_summary')}")

    print(f"\n{sep}")
    print(" Phase 3 LangGraph Demo Complete.")
    print(sep + "\n")


if __name__ == "__main__":
    run_graph_demo()
