"""Phase 2: Tool runner harness — demonstrates individual tool invocation.

This script validates that each modular tool can be invoked independently,
simulating how a LangGraph agent node would call them.
"""

from agentic_ai.tools import extract_skills, compute_match_score, suggest_rewrite
from agentic_ai.sample_data import SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION


def run_tool_demo():
    """Execute each Phase 2 tool individually with sample data and print results."""
    sep = "=" * 70
    sub_sep = "-" * 70

    print("\n" + sep)
    print(" PHASE 2: MODULAR AGENT TOOLS — INDIVIDUAL INVOCATION DEMO")
    print(sep)

    # ─── TOOL 1: extract_skills (resume) ───
    print(f"\n{sub_sep}")
    print(" TOOL 1: extract_skills (Resume)")
    print(sub_sep)
    resume_skills = extract_skills.invoke({
        "text": SAMPLE_RESUME,
        "source_type": "resume",
    })
    print(f"  Technical Skills ({len(resume_skills['technical_skills'])}):")
    for s in resume_skills["technical_skills"]:
        print(f"    • {s}")
    print(f"  Soft Skills ({len(resume_skills['soft_skills'])}):")
    for s in resume_skills["soft_skills"]:
        print(f"    • {s}")
    print(f"  Domain Knowledge ({len(resume_skills['domain_knowledge'])}):")
    for s in resume_skills["domain_knowledge"]:
        print(f"    • {s}")
    print(f"  Certifications & Methodologies ({len(resume_skills['certifications_and_methodologies'])}):")
    for s in resume_skills["certifications_and_methodologies"]:
        print(f"    • {s}")
    print(f"  Years of Experience: {resume_skills.get('years_of_experience', 'N/A')}")

    # ─── TOOL 1: extract_skills (JD) ───
    print(f"\n{sub_sep}")
    print(" TOOL 1: extract_skills (Job Description)")
    print(sub_sep)
    jd_skills = extract_skills.invoke({
        "text": SAMPLE_JOB_DESCRIPTION,
        "source_type": "job_description",
    })
    print(f"  Technical Skills ({len(jd_skills['technical_skills'])}):")
    for s in jd_skills["technical_skills"]:
        print(f"    • {s}")
    print(f"  Domain Knowledge ({len(jd_skills['domain_knowledge'])}):")
    for s in jd_skills["domain_knowledge"]:
        print(f"    • {s}")

    # ─── TOOL 2: compute_match_score ───
    print(f"\n{sub_sep}")
    print(" TOOL 2: compute_match_score")
    print(sub_sep)
    score_result = compute_match_score.invoke({
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "resume_text": SAMPLE_RESUME,
        "jd_text": SAMPLE_JOB_DESCRIPTION,
    })
    print(f"  Overall Match Score:    {score_result['overall_score']} / 100")
    print(f"  Skills Score:           {score_result['skills_score']} / 100")
    print(f"  Experience Score:       {score_result['experience_score']} / 100")
    print(f"  Impact Score:           {score_result['impact_score']} / 100")
    print(f"  Matched Skills ({len(score_result['matched_skills'])}):")
    for s in score_result["matched_skills"]:
        print(f"    [+] {s}")
    print(f"  Missing Critical ({len(score_result['missing_critical'])}):")
    for s in score_result["missing_critical"]:
        print(f"    [-] {s}")
    print(f"  Rationale: {score_result['scoring_rationale']}")

    # ─── TOOL 3: suggest_rewrite ───
    print(f"\n{sub_sep}")
    print(" TOOL 3: suggest_rewrite")
    print(sub_sep)
    sample_bullets = [
        "Developed an automated resume parsing service using LangChain and OpenAI API to speed up recruiter workflows.",
        "Built and maintained RESTful APIs using FastAPI and PostgreSQL handling 50k daily active requests.",
        "Integrated FAISS vector database for semantic search over 20,000 product catalog entries.",
    ]
    rewrite_result = suggest_rewrite.invoke({
        "bullet_points": sample_bullets,
        "target_role": "Senior AI / Full Stack Engineer",
        "missing_skills": score_result.get("missing_critical", []),
    })
    for idx, bullet in enumerate(rewrite_result["rewritten_bullets"], 1):
        print(f"\n  #{idx}. Original:")
        print(f'     "{bullet["original"]}"')
        print(f"     Rewritten:")
        print(f'     "{bullet["rewritten"]}"')
        print(f"     Reasoning: {bullet['reasoning']}")
        if bullet.get("skills_addressed"):
            print(f"     Skills Addressed: {', '.join(bullet['skills_addressed'])}")
    print(f"\n  Strategic Summary: {rewrite_result['strategic_summary']}")

    print(f"\n{sep}")
    print(" Phase 2 Tool Invocation Demo Complete.")
    print(sep + "\n")


if __name__ == "__main__":
    run_tool_demo()
