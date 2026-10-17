"""Generate a comprehensive, 5-page interview-optimized PDF architecture guide.

Each page is dedicated and self-contained:
- Page 1: System Overview & Phase 1 (Static Parsing Layer & Structured Evaluation)
- Page 2: Phase 2 (Deconstruction into Modular Agent Tools & Fallback Architecture)
- Page 3: Phase 3 (LangGraph Workflow Orchestration, State Management & Execution Graph)
- Page 4: Phase 4 (RAG Pipeline, Production FastAPI REST API & Human-in-the-Loop Gate)
- Page 5: Phases 1-4 Technical Interview Defense & 10 High-Frequency Architecture Q&As
"""

import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak,
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_decorations(num_pages)
            super().showPage()
        super().save()

    def _draw_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        # Top running header on pages 2+
        if self._pageNumber > 1:
            self.drawString(44, 11 * inch - 30,
                            "Agentic AI Resume Matcher | Architecture & Technical Interview Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(44, 11 * inch - 34, 8.5 * inch - 44, 11 * inch - 34)

        # Bottom footer on all pages
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 44, 28, page_text)
        self.drawString(44, 28, "Technical Interview Architecture Blueprint | Production Guide")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(44, 38, 8.5 * inch - 44, 38)
        self.restoreState()


def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=44,
        rightMargin=44,
        topMargin=42,
        bottomMargin=44,
    )
    styles = getSampleStyleSheet()

    # Palette
    C_PRIMARY = colors.HexColor("#0F172A")
    C_SECONDARY = colors.HexColor("#1E3A8A")
    C_ACCENT = colors.HexColor("#2563EB")
    C_TEXT = colors.HexColor("#1E293B")
    C_MUTED = colors.HexColor("#475569")
    C_GREEN = colors.HexColor("#065F46")
    C_ORANGE = colors.HexColor("#92400E")
    C_PHASE2 = colors.HexColor("#7C3AED")
    C_PHASE3 = colors.HexColor("#059669")
    C_PHASE4 = colors.HexColor("#DC2626")

    # Typography styles
    s_title = ParagraphStyle(
        "T", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=18, leading=22, textColor=C_PRIMARY, spaceAfter=3
    )
    s_sub = ParagraphStyle(
        "S", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=10, leading=14, textColor=C_ACCENT, spaceAfter=4
    )
    s_meta = ParagraphStyle(
        "M", parent=styles["Normal"], fontName="Helvetica-Oblique",
        fontSize=8, leading=11, textColor=C_MUTED
    )
    s_h1 = ParagraphStyle(
        "H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=11, leading=15, textColor=C_SECONDARY, spaceBefore=8, spaceAfter=4, keepWithNext=True
    )
    s_h2 = ParagraphStyle(
        "H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=9.5, leading=13, textColor=C_ACCENT, spaceBefore=6, spaceAfter=3, keepWithNext=True
    )
    s_body = ParagraphStyle(
        "B", parent=styles["Normal"], fontName="Helvetica",
        fontSize=8, leading=11.5, textColor=C_TEXT, spaceAfter=4
    )
    s_th = ParagraphStyle(
        "TH", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=7.5, leading=10, textColor=colors.white
    )
    s_tc = ParagraphStyle(
        "TC", parent=styles["Normal"], fontName="Helvetica",
        fontSize=7.5, leading=10, textColor=C_TEXT
    )
    s_tcb = ParagraphStyle("TCB", parent=s_tc, fontName="Helvetica-Bold")
    s_arr = ParagraphStyle(
        "ARR", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=10, leading=10, textColor=colors.HexColor("#475569"), alignment=1
    )
    s_qq = ParagraphStyle(
        "QQ", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=8, leading=11, textColor=C_SECONDARY, spaceBefore=4, spaceAfter=1, keepWithNext=True
    )
    s_qa = ParagraphStyle(
        "QA", parent=s_body, fontSize=7.5, leading=10.5, leftIndent=8, spaceAfter=4
    )
    s_call = ParagraphStyle(
        "CL", parent=s_body, fontSize=7.5, leading=10.5, textColor=C_GREEN, spaceAfter=0
    )

    story = []

    def make_table(data, widths, header_color=C_SECONDARY):
        t = Table(data, colWidths=widths)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), header_color),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ("PADDING", (0, 0), (-1, -1), 3),
        ]))
        return t

    def callout(text, bg="#ECFDF5", border="#10B981", style=s_call):
        t = Table([[Paragraph(text, style)]], colWidths=[524])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor(border)),
            ("PADDING", (0, 0), (-1, -1), 4),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        return t

    def phase_banner(phase_num, phase_title, bg_color):
        tag_style = ParagraphStyle(
            "PB", parent=styles["Normal"], fontName="Helvetica-Bold",
            fontSize=10, leading=13, textColor=colors.white
        )
        t = Table([[Paragraph(f"PHASE {phase_num}: {phase_title}", tag_style)]], colWidths=[524])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg_color)),
            ("PADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        return t

    # ═══════════════════════════════════════════════════════════════
    # PAGE 1: TITLE & PHASE 1
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("Agentic AI Resume & JD Matcher", s_title))
    story.append(Paragraph("End-to-End System Architecture & Technical Interview Guide (Phases 1-4)", s_sub))
    story.append(Paragraph(
        "<b>Core Architecture:</b> Deterministic Parsing &middot; Modular LangChain Tools &middot; "
        "LangGraph StateGraph &middot; FAISS Vector RAG &middot; FastAPI REST API &middot; Human-in-the-Loop (HITL)",
        s_meta
    ))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_ACCENT, spaceAfter=6))

    story.append(phase_banner(1, "STATIC PARSING LAYER & STRUCTURED EVALUATION", "#1E3A8A"))
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. System Architecture & Phase 1 Scope", s_h1))
    story.append(Paragraph(
        "The <b>Agentic AI Resume Matcher</b> ingests candidate resumes, extracts structured technical profiles, "
        "scores candidate fit against Target Job Descriptions, isolates critical skill gaps, and rewrites bullet points "
        "using Google's XYZ formula (<i>Accomplished [X] as measured by [Y] by doing [Z]</i>). "
        "<b>Phase 1</b> builds the deterministic bedrock: multi-column document extraction and Pydantic "
        "structured schemas that guarantee zero runtime schema failures.",
        s_body
    ))
    story.append(callout(
        "<b>Phase 1 Thesis:</b> Nondeterminism compounds disastrously in agent workflows. If multi-column PDF extraction "
        "scrambles text, downstream agents hallucinate. By enforcing strict bounding-box text extraction and "
        "type-safe Pydantic output constraints at Phase 1, we guarantee pristine data feeds before introducing agent loops."
    ))
    story.append(Spacer(1, 5))

    story.append(Paragraph("1.1 Phase 1 File, Library & Function Specifications", s_h2))
    story.append(make_table([
        [Paragraph("File Name", s_th), Paragraph("Functions / Classes", s_th),
         Paragraph("Libraries Used", s_th), Paragraph("Purpose / Implementation Details", s_th)],
        [Paragraph("<code>parsers.py</code>", s_tcb),
         Paragraph("• <code>extract_text_from_pdf()</code><br/>"
                   "• <code>extract_text_from_docx()</code><br/>"
                   "• <code>parse_document()</code>", s_tc),
         Paragraph("• <code>pdfplumber</code><br/>"
                   "• <code>python-docx</code><br/>"
                   "• <code>io.BytesIO</code>", s_tc),
         Paragraph("Extracts clean text preserving spatial layout and multi-column bounding boxes; rejects corrupt binaries.", s_tc)],
        [Paragraph("<code>schemas.py</code>", s_tcb),
         Paragraph("• <code>BulletOptimization</code><br/>"
                   "• <code>SkillGapReport</code><br/>"
                   "• <code>ScoringRubric</code><br/>"
                   "• <code>ResumeEvaluation</code>", s_tc),
         Paragraph("• <code>pydantic</code> (<code>BaseModel</code>, <code>Field</code>)<br/>"
                   "• <code>typing</code> (<code>List</code>, <code>Optional</code>)", s_tc),
         Paragraph("Defines validated domain models with numeric constraints (<code>ge=0, le=100</code>) for match scores.", s_tc)],
        [Paragraph("<code>evaluator.py</code>", s_tcb),
         Paragraph("• <code>evaluate_resume()</code><br/>"
                   "• <code>mock_evaluate_resume()</code><br/>"
                   "• <code>_get_llm()</code>", s_tc),
         Paragraph("• <code>langchain_core.prompts</code><br/>"
                   "• <code>langchain_openai</code><br/>"
                   "• <code>langchain_google_genai</code>", s_tc),
         Paragraph("Monolithic baseline evaluation engine calling LLMs with <code>.with_structured_output()</code> and offline mock fallback.", s_tc)],
        [Paragraph("<code>sample_data.py</code>", s_tcb),
         Paragraph("• <code>SAMPLE_RESUME</code><br/>"
                   "• <code>SAMPLE_JOB_DESCRIPTION</code>", s_tc),
         Paragraph("• Standard Python", s_tc),
         Paragraph("Curated benchmark resume and JD strings for offline testing and baseline verification.", s_tc)],
    ], [85, 140, 125, 174], C_SECONDARY))
    story.append(Spacer(1, 5))

    story.append(Paragraph("1.2 Key Engineering Highlights & Trade-offs", s_h2))
    story.append(Paragraph(
        "• <b>Spatial Layout vs OCR:</b> Used <code>pdfplumber</code> bounding-box extraction over Tesseract OCR to eliminate "
        "heavy C-dependencies while preserving multi-column reading order.<br/>"
        "• <b>Grammar-Constrained Decoding:</b> Instead of asking for JSON in prompt strings, Pydantic models compile into JSON "
        "Schema enforced via API token logits, eliminating malformed JSON parsing exceptions.",
        s_body
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # PAGE 2: PHASE 2
    # ═══════════════════════════════════════════════════════════════
    story.append(phase_banner(2, "DECONSTRUCTION INTO MODULAR AGENT TOOLS", "#7C3AED"))
    story.append(Spacer(1, 5))

    story.append(Paragraph("2. Phase 2 Architecture: Modular Tool Contracts", s_h1))
    story.append(Paragraph(
        "Phase 1 relied on a monolithic prompt that performed extraction, scoring, and bullet rewriting in one shot. "
        "<b>Phase 2 decomposes this monolith into three isolated, independently testable LangChain tools</b> "
        "decorated with <code>@tool</code>, each backed by dedicated Pydantic input and output schemas.",
        s_body
    ))
    story.append(callout(
        "<b>Key Design Principle:</b> Tools are NOT autonomous agents; they are deterministic, single-responsibility workers. "
        "By enforcing strict typing via <code>tool_schemas.py</code>, we isolate LLM reasoning boundaries and enable "
        "independent unit testing, granular LangSmith observability traces, and fine-grained caching.",
        "#F5F3FF", "#8B5CF6",
        ParagraphStyle("P2Call", parent=s_body, fontSize=7.5, leading=10.5, textColor=colors.HexColor("#5B21B6"))
    ))
    story.append(Spacer(1, 5))

    story.append(Paragraph("2.1 Phase 2 File, Library & Function Specifications", s_h2))
    story.append(make_table([
        [Paragraph("File Name", s_th), Paragraph("Functions / Classes", s_th),
         Paragraph("Libraries Used", s_th), Paragraph("Purpose / Implementation Details", s_th)],
        [Paragraph("<code>tool_schemas.py</code>", s_tcb),
         Paragraph("• <code>ExtractSkillsInput</code> / <code>ExtractedSkills</code><br/>"
                   "• <code>MatchScoreInput</code> / <code>MatchScoreOutput</code><br/>"
                   "• <code>RewriteInput</code> / <code>RewriteOutput</code>", s_tc),
         Paragraph("• <code>pydantic</code> (<code>BaseModel</code>, <code>Field</code>)<br/>"
                   "• <code>typing</code> (<code>List</code>, <code>Optional</code>)", s_tc),
         Paragraph("Defines fine-grained input/output Pydantic contracts that bind each tool to deterministic I/O schemas.", s_tc)],
        [Paragraph("<code>tools.py</code>", s_tcb),
         Paragraph("• <code>extract_skills()</code><br/>"
                   "• <code>compute_match_score()</code><br/>"
                   "• <code>suggest_rewrite()</code><br/>"
                   "• <code>_mock_*()</code> fallbacks", s_tc),
         Paragraph("• <code>langchain_core.tools</code> (<code>@tool</code>)<br/>"
                   "• <code>langchain_core.prompts</code><br/>"
                   "• <code>langchain_openai</code> / <code>google_genai</code>", s_tc),
         Paragraph("Decorated LangChain tools executing skill extraction, semantic scoring, and XYZ bullet optimization with mock fallbacks.", s_tc)],
        [Paragraph("<code>tool_runner.py</code>", s_tcb),
         Paragraph("• <code>run_tool_demo()</code>", s_tc),
         Paragraph("• LangChain Tool Invocation API (<code>.invoke()</code>)", s_tc),
         Paragraph("Standalone verification runner that invokes Phase 2 tools in isolation to validate contract adherence.", s_tc)],
    ], [85, 140, 125, 174], C_PHASE2))
    story.append(Spacer(1, 5))

    story.append(Paragraph("2.2 Tool Execution Flow & Zero-Cost CI/CD Mock Fallbacks", s_h2))
    story.append(Paragraph(
        "1. <b><code>extract_skills</code></b>: Analyzes raw text to extract categorized technical skills, soft skills, and years of experience.<br/>"
        "2. <b><code>compute_match_score</code></b>: Compares candidate skills against JD requirements to generate aligned skills, missing skills, and a weighted 0-100 score.<br/>"
        "3. <b><code>suggest_rewrite</code></b>: Rewrites raw resume bullets using the XYZ formula with grounded metrics and action verbs.<br/>"
        "• <b>Deterministic Mock Routing:</b> Every tool inspects runtime environment variables for valid LLM API keys. "
        "If keys are missing, execution automatically routes to typed <code>_mock_*</code> helpers. "
        "This allows 100% of our test suite to execute instantly in offline CI/CD without incurring API tokens or rate limits.",
        s_body
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # PAGE 3: PHASE 3
    # ═══════════════════════════════════════════════════════════════
    story.append(phase_banner(3, "LANGGRAPH WORKFLOW ORCHESTRATION & STATE MACHINE", "#059669"))
    story.append(Spacer(1, 5))

    story.append(Paragraph("3. Phase 3 Architecture: LangGraph State Machine", s_h1))
    story.append(Paragraph(
        "Phase 2 gave us isolated tools, but orchestrating them requires managing state across dependent steps. "
        "<b>Phase 3 unifies tools into a directed cyclical state graph using LangGraph.</b> "
        "LangGraph manages immutable state transitions, checkpointing, and parallel branch execution.",
        s_body
    ))
    story.append(callout(
        "<b>Why LangGraph over LangChain Chains:</b> Standard chains are strictly linear (A &gt; B &gt; C) with no "
        "checkpointing or branching. LangGraph provides a compiled state machine with cycles, branching, and persistent checkpoints. "
        "This allows parallel extraction of resume and JD text, state rollback, and async pause/resume capability.",
        "#ECFDF5", "#10B981",
        ParagraphStyle("P3Call", parent=s_body, fontSize=7.5, leading=10.5, textColor=C_GREEN)
    ))
    story.append(Spacer(1, 4))

    # Phase 3 Workflow Diagram
    p3_diag = [
        [
            Paragraph("<b>START</b><br/>Input Texts", s_tc),
            Paragraph("<b>&gt;</b>", s_arr),
            Paragraph("<b>extract_resume</b><br/><b>extract_jd</b><br/><i>(Parallel Nodes)</i>", s_tcb),
            Paragraph("<b>&gt;</b>", s_arr),
            Paragraph("<b>compute_score</b><br/><i>(Sync Barrier)</i>", s_tcb),
            Paragraph("<b>&gt;</b>", s_arr),
            Paragraph("<b>optimize_bullets</b><br/><i>(XYZ Rewriting)</i>", s_tcb),
            Paragraph("<b>&gt;</b>", s_arr),
            Paragraph("<b>aggregate_report</b><br/><b>END</b>", s_tcb),
        ]
    ]
    t_p3 = Table(p3_diag, colWidths=[65, 14, 100, 14, 90, 14, 100, 14, 113])
    t_p3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#D1FAE5")),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#A7F3D0")),
        ("BACKGROUND", (4, 0), (4, 0), colors.HexColor("#6EE7B7")),
        ("BACKGROUND", (6, 0), (6, 0), colors.HexColor("#34D399")),
        ("BACKGROUND", (8, 0), (8, 0), colors.HexColor("#10B981")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 3),
        ("PADDING", (1, 0), (1, 0), 0),
        ("PADDING", (3, 0), (3, 0), 0),
        ("PADDING", (5, 0), (5, 0), 0),
        ("PADDING", (7, 0), (7, 0), 0),
    ]))
    story.append(t_p3)
    story.append(Spacer(1, 5))

    story.append(Paragraph("3.1 Phase 3 File, Library & Function Specifications", s_h2))
    story.append(make_table([
        [Paragraph("File Name", s_th), Paragraph("Functions / Classes", s_th),
         Paragraph("Libraries Used", s_th), Paragraph("Purpose / Implementation Details", s_th)],
        [Paragraph("<code>graph.py</code>", s_tcb),
         Paragraph("• <code>AgentState</code> (TypedDict)<br/>"
                   "• <code>extract_resume_node()</code><br/>"
                   "• <code>extract_jd_node()</code><br/>"
                   "• <code>compute_score_node()</code><br/>"
                   "• <code>optimize_bullets_node()</code><br/>"
                   "• <code>aggregate_report_node()</code><br/>"
                   "• <code>compile_workflow()</code>", s_tc),
         Paragraph("• <code>langgraph.graph</code> (<code>StateGraph</code>, <code>START</code>, <code>END</code>)<br/>"
                   "• <code>typing</code> (<code>TypedDict</code>, <code>Annotated</code>)", s_tc),
         Paragraph("Builds and compiles the asynchronous state graph orchestrating parallel extraction, scoring, and bullet optimization.", s_tc)],
        [Paragraph("<code>graph_runner.py</code>", s_tcb),
         Paragraph("• <code>run_graph_demo()</code>", s_tc),
         Paragraph("• LangGraph Compiled Graph API (<code>.invoke()</code>)<br/>"
                   "• <code>json</code>", s_tc),
         Paragraph("Executes the compiled workflow graph end-to-end and outputs formatted JSON evaluation reports.", s_tc)],
        [Paragraph("<code>main.py</code>", s_tcb),
         Paragraph("• <code>main()</code>", s_tc),
         Paragraph("• <code>argparse</code><br/>"
                   "• <code>sys</code>", s_tc),
         Paragraph("Unified CLI entry point with subcommands to execute Phase 1, Phase 2, or Phase 3 pipelines.", s_tc)],
    ], [85, 140, 125, 174], C_PHASE3))
    story.append(Spacer(1, 5))

    story.append(Paragraph("3.2 State Management & Graph Reducer Mechanics", s_h2))
    story.append(Paragraph(
        "• <b><code>AgentState</code> TypedDict:</b> Defines explicit channels for <code>resume_text</code>, <code>jd_text</code>, "
        "<code>extracted_skills</code>, <code>match_score</code>, <code>bullet_optimizations</code>, and <code>final_report</code>.<br/>"
        "• <b>Parallel Branching:</b> Both <code>extract_resume_node</code> and <code>extract_jd_node</code> branch concurrently from <code>START</code>, "
        "halving LLM extraction latency before meeting at the <code>compute_score_node</code> synchronization barrier.<br/>"
        "• <b>Immutability:</b> Each node returns partial state dictionaries that LangGraph merges into the central state.",
        s_body
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # PAGE 4: PHASE 4
    # ═══════════════════════════════════════════════════════════════
    story.append(phase_banner(4, "RAG-ENHANCED PIPELINE, REST API & HUMAN-IN-THE-LOOP", "#DC2626"))
    story.append(Spacer(1, 5))

    story.append(Paragraph("4. Phase 4 Architecture: Production Delivery & Supervision", s_h1))
    story.append(Paragraph(
        "<b>Phase 4 transitions the system into a production-grade enterprise platform</b> with three pillars: "
        "(1) <b>FAISS Vector RAG</b> to ground bullet rewrites in real XYZ examples and match JDs from an indexed corpus, "
        "(2) <b>FastAPI REST API</b> exposing the entire pipeline as versioned HTTP endpoints, and "
        "(3) <b>Human-in-the-Loop (HITL)</b> approval gates using LangGraph state checkpointing.",
        s_body
    ))
    story.append(callout(
        "<b>Phase 4 Thesis:</b> Autonomous LLMs hallucinate metrics when rewriting resumes. RAG solves this by grounding "
        "rewrites in curated XYZ best practices. High-stakes resume edits require human oversight before delivery; "
        "LangGraph's <code>interrupt()</code> pattern allows reviewers to inspect, edit, or approve rewrites before state finalization.",
        "#FEE2E2", "#DC2626",
        ParagraphStyle("P4Call", parent=s_body, fontSize=7.5, leading=10.5, textColor=colors.HexColor("#991B1B"))
    ))
    story.append(Spacer(1, 4))

    # Phase 4 Workflow Diagram
    p4_diag = [
        [
            Paragraph("<b>START</b><br/>Input Texts", s_tc),
            Paragraph("<b>&gt;</b>", s_arr),
            Paragraph("<b>Parallel Extract</b><br/>Resume + JD", s_tcb),
            Paragraph("<b>&gt;</b>", s_arr),
            Paragraph("<b>retrieve_context</b><br/><i>(FAISS RAG)</i>", s_tcb),
            Paragraph("<b>&gt;</b>", s_arr),
            Paragraph("<b>compute_score</b><br/><b>optimize_bullets</b>", s_tcb),
            Paragraph("<b>&gt;</b>", s_arr),
            Paragraph("<b>[HITL Review]</b><br/><b>aggregate &gt; END</b>", s_tcb),
        ]
    ]
    t_p4 = Table(p4_diag, colWidths=[65, 14, 95, 14, 105, 14, 105, 14, 113])
    t_p4.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#FEE2E2")),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#FECACA")),
        ("BACKGROUND", (4, 0), (4, 0), colors.HexColor("#FCA5A5")),
        ("BACKGROUND", (6, 0), (6, 0), colors.HexColor("#F87171")),
        ("BACKGROUND", (8, 0), (8, 0), colors.HexColor("#EF4444")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 3),
        ("PADDING", (1, 0), (1, 0), 0),
        ("PADDING", (3, 0), (3, 0), 0),
        ("PADDING", (5, 0), (5, 0), 0),
        ("PADDING", (7, 0), (7, 0), 0),
    ]))
    story.append(t_p4)
    story.append(Spacer(1, 5))

    story.append(Paragraph("4.1 Phase 4 File, Library & Function Specifications", s_h2))
    story.append(make_table([
        [Paragraph("File Name", s_th), Paragraph("Functions / Classes", s_th),
         Paragraph("Libraries Used", s_th), Paragraph("Purpose / Implementation Details", s_th)],
        [Paragraph("<code>rag.py</code>", s_tcb),
         Paragraph("• <code>build_jd_index()</code><br/>"
                   "• <code>retrieve_similar_jds()</code><br/>"
                   "• <code>build_best_practices_index()</code><br/>"
                   "• <code>retrieve_rewrite_context()</code>", s_tc),
         Paragraph("• <code>faiss-cpu</code><br/>"
                   "• <code>langchain_huggingface</code><br/>"
                   "• <code>sentence-transformers</code>", s_tc),
         Paragraph("Builds FAISS vector indices with local <code>all-MiniLM-L6-v2</code> embeddings; retrieves top-k semantic matches.", s_tc)],
        [Paragraph("<code>rag_data.py</code>", s_tcb),
         Paragraph("• <code>SAMPLE_JD_CORPUS</code><br/>"
                   "• <code>BEST_PRACTICES_CORPUS</code>", s_tc),
         Paragraph("• Standard Python", s_tc),
         Paragraph("Curated corpora: 5 complete domain JDs and 15 XYZ-formula resume bullet exemplars across AI, Full-Stack, and DevOps.", s_tc)],
        [Paragraph("<code>api.py</code>", s_tcb),
         Paragraph("• FastAPI Application<br/>"
                   "• <code>MemorySaver</code> checkpointer<br/>"
                   "• HITL thread session manager", s_tc),
         Paragraph("• <code>fastapi</code><br/>"
                   "• <code>uvicorn</code><br/>"
                   "• LangGraph Checkpointing", s_tc),
         Paragraph("Async REST API exposing evaluation, RAG retrieval, and stateful human approval gates with Swagger docs.", s_tc)],
        [Paragraph("<code>api_schemas.py</code>", s_tcb),
         Paragraph("• <code>EvaluateRequest</code> / <code>Response</code><br/>"
                   "• <code>RAGEvaluateRequest</code><br/>"
                   "• <code>HITLReviewRequest</code>", s_tc),
         Paragraph("• <code>pydantic</code> (BaseModel, Field)", s_tc),
         Paragraph("Type-safe HTTP request/response payloads with validation and error schemas.", s_tc)],
    ], [85, 140, 125, 174], colors.HexColor("#DC2626")))
    story.append(Spacer(1, 5))

    story.append(Paragraph("4.2 Production REST Endpoints & HITL State Persistence", s_h2))
    story.append(make_table([
        [Paragraph("HTTP Endpoint", s_th), Paragraph("Method", s_th),
         Paragraph("Workflow / Purpose", s_th), Paragraph("State & Checkpoint Handling", s_th)],
        [Paragraph("<code>/api/v1/evaluate</code>", s_tcb), Paragraph("POST", s_tc),
         Paragraph("Executes standard LangGraph workflow end-to-end.", s_tc),
         Paragraph("Stateless execution returning final aggregated evaluation report.", s_tc)],
        [Paragraph("<code>/api/v1/evaluate/rag</code>", s_tcb), Paragraph("POST", s_tc),
         Paragraph("Auto-retrieves top JD match from FAISS & grounds rewrites.", s_tc),
         Paragraph("Embeds candidate resume, fetches nearest JD, and injects XYZ examples.", s_tc)],
        [Paragraph("<code>/api/v1/evaluate/hitl</code>", s_tcb), Paragraph("POST", s_tc),
         Paragraph("Runs graph until <code>human_review_node</code> and pauses.", s_tc),
         Paragraph("Persists thread state in <code>MemorySaver</code>; returns pending rewrites.", s_tc)],
        [Paragraph("<code>/api/v1/evaluate/hitl/{id}/review</code>", s_tcb), Paragraph("POST", s_tc),
         Paragraph("Resumes graph with approved or edited rewrites.", s_tc),
         Paragraph("Invokes <code>Command(resume=...)</code> to resume thread and finalize report.", s_tc)],
    ], [140, 45, 175, 164], colors.HexColor("#991B1B")))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # PAGE 5: INTERVIEW DEFENSE
    # ═══════════════════════════════════════════════════════════════
    story.append(phase_banner("1-4", "TECHNICAL INTERVIEW DEFENSE &amp; SYSTEM DESIGN Q&amp;A", "#0F172A"))
    story.append(Spacer(1, 5))

    story.append(Paragraph("5. Architectural Interview Q&amp;A Defense Cheat Sheet", s_h1))

    qa_pairs = [
        ("Q1: Why build a dedicated parsing layer instead of feeding PDFs directly to LLMs?",
         "<b>Answer:</b> Layout nondeterminism compounds. Multi-column PDFs scramble text streams when parsed naively. "
         "By guaranteeing bounding-box parsing via <code>pdfplumber</code> in Phase 1, we eliminate garbage-in/garbage-out cascades before agents run."),

        ("Q2: Why Pydantic Structured Outputs instead of prompting for raw JSON?",
         "<b>Answer:</b> Unconstrained text generation is brittle (markdown fences, truncated braces). "
         "Using <code>.with_structured_output()</code> compiles Pydantic schemas into JSON Schema constraints sent directly to API token logits, guaranteeing 100% schema conformity."),

        ("Q3: Why decompose monolithic processing into separate Tools in Phase 2?",
         "<b>Answer:</b> 1. <b>Testability:</b> Every tool has isolated unit tests. 2. <b>Selectivity:</b> Agents conditionally execute "
         "expensive rewrite steps only if match scores fall below thresholds. 3. <b>Observability:</b> Each tool produces discrete traces in LangSmith."),

        ("Q4: Why use LangGraph for orchestration instead of linear LangChain chains or plain Python?",
         "<b>Answer:</b> Standard chains are strictly linear DAGs without cyclic loops or state persistence. LangGraph treats workflows "
         "as state machines with cycles, branching, parallel node execution, and first-class state checkpointing required for human approvals."),

        ("Q5: How does your test suite handle LLM costs during automated CI/CD runs?",
         "<b>Answer:</b> Every tool checks for valid API keys; when absent, execution transparently routes to deterministic <code>_mock_*</code> helpers. "
         "This allows our full test suite to verify graph propagation and contracts locally and instantly with zero token expenses."),

        ("Q6: Why incorporate RAG instead of relying purely on LLM parametric memory?",
         "<b>Answer:</b> Parametric LLM knowledge hallucinates metrics and uses cliché phrasing. RAG grounds rewrites in real-world, "
         "curated XYZ best practices. It also enables automatic JD matching from indexed corporate job pools without manual user copy-pasting."),

        ("Q7: Why use FAISS with local HuggingFace embeddings instead of OpenAI embeddings?",
         "<b>Answer:</b> Zero marginal cost, offline resilience, and zero latency. Local <code>all-MiniLM-L6-v2</code> models generate 384-dimensional "
         "embeddings locally without external network round-trips, rate limit throttling, or per-token fees."),

        ("Q8: Why enforce Human-in-the-Loop instead of letting agents fully automate rewrites?",
         "<b>Answer:</b> Resume rewriting is high-stakes: a hallucinated percentage or unverified claim can disqualify a candidate. "
         "HITL introduces a safety approval gate where human recruiters inspect and modify suggestions before delivery."),

        ("Q9: How does your FastAPI architecture maintain stateful HITL flows over stateless HTTP?",
         "<b>Answer:</b> LangGraph's <code>MemorySaver</code> checkpointer serializes graph state keyed by <code>thread_id</code>. "
         "The client's first request pauses at the interrupt point; a subsequent review POST calls <code>Command(resume=...)</code>, resuming the exact graph state."),

        ("Q10: How would you scale this architecture horizontally for multi-tenant production?",
         "<b>Answer:</b> Replace <code>MemorySaver</code> with PostgreSQL or Redis checkpointers (<code>PostgresSaver</code>), offload vector storage "
         "to pgvector or Pinecone, and distribute graph nodes via Celery/Temporal workers with FastAPI as the API gateway."),
    ]

    for q, a in qa_pairs:
        story.append(Paragraph(q, s_qq))
        story.append(Paragraph(a, s_qa))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[PDF Generator] Successfully compiled: {output_path}")


if __name__ == "__main__":
    # Primary comprehensive guide for the entire system
    build_pdf("Agentic_AI_Architecture_and_Interview_Guide.pdf")

    # Target files ensuring all phase references resolve to the updated master guide
    build_pdf("Phase_1_Architecture_and_Implementation_Guide.pdf")
    build_pdf("Phase_3_Architecture_and_Implementation_Guide.pdf")
    build_pdf("Phase_4_Architecture_and_Implementation_Guide.pdf")
