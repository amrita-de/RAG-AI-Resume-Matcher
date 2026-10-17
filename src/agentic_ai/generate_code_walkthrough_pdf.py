"""Generate a comprehensive, beginner-friendly Codebase Walkthrough PDF.

Each page is dedicated and self-contained:
- Page 1: Big Picture Architecture & Beginner Agentic AI Primer
- Page 2: Document Ingestion Layer (parsers.py)
- Page 3: Phase 1 Schemas & Baseline Evaluator (schemas.py, evaluator.py, sample_data.py)
- Page 4: Phase 2 Modular Agent Tools (tool_schemas.py, tools.py, tool_runner.py)
- Page 5: Phase 3 LangGraph Workflow & State Machine (graph.py, graph_runner.py)
- Page 6: Phase 4 FAISS Vector RAG Pipeline (rag_data.py, rag.py)
- Page 7: Phase 4 Production REST API & Human-in-the-Loop (api_schemas.py, api.py)
- Page 8: CLI Orchestrator, Packaging & Beginner Mastery Checklist (main.py, __init__.py, pyproject.toml)
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
            self.drawString(40, 11 * inch - 28,
                            "Agentic AI Resume Matcher | Beginner Codebase Walkthrough & Learning Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(40, 11 * inch - 32, 8.5 * inch - 40, 11 * inch - 32)

        # Bottom footer on all pages
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 40, 24, page_text)
        self.drawString(40, 24, "Complete Code Walkthrough | File-by-File Beginner's Guide")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 34, 8.5 * inch - 40, 34)
        self.restoreState()


def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=38,
        bottomMargin=40,
    )
    styles = getSampleStyleSheet()

    # Color Palette
    C_PRIMARY = colors.HexColor("#0F172A")
    C_SECONDARY = colors.HexColor("#1E3A8A")
    C_ACCENT = colors.HexColor("#2563EB")
    C_TEXT = colors.HexColor("#1E293B")
    C_MUTED = colors.HexColor("#475569")
    C_GREEN = colors.HexColor("#065F46")
    C_ORANGE = colors.HexColor("#92400E")
    C_PURPLE = colors.HexColor("#7C3AED")
    C_EMERALD = colors.HexColor("#059669")
    C_CRIMSON = colors.HexColor("#DC2626")

    # Typography Styles
    s_title = ParagraphStyle(
        "T", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=17, leading=21, textColor=C_PRIMARY, spaceAfter=2
    )
    s_sub = ParagraphStyle(
        "S", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=9.5, leading=13, textColor=C_ACCENT, spaceAfter=3
    )
    s_meta = ParagraphStyle(
        "M", parent=styles["Normal"], fontName="Helvetica-Oblique",
        fontSize=7.5, leading=10.5, textColor=C_MUTED
    )
    s_h1 = ParagraphStyle(
        "H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=10.5, leading=14, textColor=C_SECONDARY, spaceBefore=5, spaceAfter=3, keepWithNext=True
    )
    s_h2 = ParagraphStyle(
        "H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=9, leading=12, textColor=C_ACCENT, spaceBefore=4, spaceAfter=2, keepWithNext=True
    )
    s_body = ParagraphStyle(
        "B", parent=styles["Normal"], fontName="Helvetica",
        fontSize=7.5, leading=10.5, textColor=C_TEXT, spaceAfter=3
    )
    s_th = ParagraphStyle(
        "TH", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=7, leading=9.5, textColor=colors.white
    )
    s_tc = ParagraphStyle(
        "TC", parent=styles["Normal"], fontName="Helvetica",
        fontSize=7, leading=9.5, textColor=C_TEXT
    )
    s_tcb = ParagraphStyle("TCB", parent=s_tc, fontName="Helvetica-Bold")
    s_call = ParagraphStyle(
        "CL", parent=s_body, fontSize=7, leading=9.5, textColor=C_GREEN, spaceAfter=0
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
            ("PADDING", (0, 0), (-1, -1), 2.5),
        ]))
        return t

    def callout(text, bg="#ECFDF5", border="#10B981", style=s_call):
        t = Table([[Paragraph(text, style)]], colWidths=[532])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor(border)),
            ("PADDING", (0, 0), (-1, -1), 3.5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        return t

    def section_banner(title, subtitle, bg_color):
        t_text = Paragraph(
            f"<b>{title}</b> &middot; <font size='7.5'>{subtitle}</font>",
            ParagraphStyle("SB", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=colors.white)
        )
        t = Table([[t_text]], colWidths=[532])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg_color)),
            ("PADDING", (0, 0), (-1, -1), 4),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        return t

    # ═══════════════════════════════════════════════════════════════
    # PAGE 1: BIG PICTURE & BEGINNER PRIMER
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("Agentic AI Resume &amp; JD Matcher", s_title))
    story.append(Paragraph("Complete Beginner's Codebase Walkthrough: File-by-File Explanation", s_sub))
    story.append(Paragraph(
        "<b>Audience:</b> Beginners to AI Engineering, LangChain, LangGraph, RAG, and FastAPI &middot; "
        "<b>Goal:</b> Demystify every import, function, data structure, and design pattern in simple English.",
        s_meta
    ))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_ACCENT, spaceAfter=5))

    story.append(section_banner("MODULE 0", "THE BIG PICTURE &amp; CORE CONCEPTS PRIMER", "#0F172A"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. What Does This Project Do in Plain English?", s_h1))
    story.append(Paragraph(
        "Imagine applying for a job: you have a resume in PDF or Word, and the company has a Job Description (JD). "
        "Normally, a human recruiter reads both, finds matching skills, spots missing requirements, and decides if you get an interview. "
        "<b>This project automates that entire process using an Autonomous AI Agent</b>. It parses your resume, extracts skills, calculates "
        "a mathematical match score, and rewrites weak resume bullet points into high-impact Google XYZ achievements.",
        s_body
    ))

    story.append(callout(
        "<b>Real-World Analogy:</b> Think of this system as an automated factory with 4 departments: "
        "(1) <b>parsers.py</b> is the delivery dock unboxing PDFs; (2) <b>tools.py</b> are specialized robots measuring skills and rewriting text; "
        "(3) <b>graph.py</b> is the smart conveyor belt routing data between robots; (4) <b>rag.py</b> is the corporate reference library "
        "providing real-world examples, and (5) <b>api.py</b> is the customer counter where external apps submit jobs."
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Essential Concepts Every Beginner Must Know", s_h1))
    story.append(make_table([
        [Paragraph("Term / Concept", s_th), Paragraph("What It Means", s_th), Paragraph("Why We Use It in This Project", s_th)],
        [Paragraph("<b>LLM</b> (Large Language Model)", s_tc),
         Paragraph("An AI model (like GPT-4o or Gemini 1.5) trained on text that generates human-like responses.", s_tc),
         Paragraph("Acts as the reasoning engine for skill extraction and bullet point rewriting.", s_tc)],
        [Paragraph("<b>Structured Output</b>", s_tc),
         Paragraph("Forcing the LLM to reply in strict JSON adhering to a schema, not conversational text.", s_tc),
         Paragraph("Guarantees the AI never gives broken JSON or markdown fences that crash your code.", s_tc)],
        [Paragraph("<b>LangChain Tool</b> (<code>@tool</code>)", s_tc),
         Paragraph("A regular Python function wrapped so an AI agent can inspect its inputs, outputs, and purpose.", s_tc),
         Paragraph("Turns monolithic code into modular, individually testable functions (e.g., extract_skills).", s_tc)],
        [Paragraph("<b>LangGraph StateGraph</b>", s_tc),
         Paragraph("A state machine where functions are 'nodes' and data is passed via a central typed state dict.", s_tc),
         Paragraph("Enables parallel tasks (extracting resume and JD at the same time) and pause/resume flows.", s_tc)],
        [Paragraph("<b>RAG</b> (Retrieval-Augmented Gen)", s_tc),
         Paragraph("Searching an indexed database of knowledge and giving relevant excerpts to the LLM as reference.", s_tc),
         Paragraph("Grounds resume rewrites in real XYZ formula best practices so the AI doesn't hallucinate.", s_tc)],
        [Paragraph("<b>Vector Embedding</b>", s_tc),
         Paragraph("A mathematical list of numbers (coordinates) representing the semantic meaning of text.", s_tc),
         Paragraph("Allows FAISS to calculate how similar a resume bullet is to high-scoring industry examples.", s_tc)],
        [Paragraph("<b>Human-in-the-Loop</b> (HITL)", s_tc),
         Paragraph("Pausing an AI workflow at a critical decision point so a human can inspect and approve.", s_tc),
         Paragraph("Prevents hallucinated or exaggerated resume bullet edits from being finalized without review.", s_tc)],
        [Paragraph("<b>FastAPI &amp; REST API</b>", s_tc),
         Paragraph("A high-performance Python framework that turns functions into web URLs (HTTP endpoints).", s_tc),
         Paragraph("Allows web frontends, mobile apps, and third-party tools to submit resumes and get JSON reports.", s_tc)],
    ], [110, 200, 222], C_SECONDARY))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. Complete Project Architecture &amp; File Map", s_h1))
    story.append(Paragraph(
        "• <b>Phase 1 (Bedrock):</b> <code>parsers.py</code> &rarr; <code>schemas.py</code> &rarr; <code>evaluator.py</code> &rarr; <code>sample_data.py</code><br/>"
        "• <b>Phase 2 (Modular Tools):</b> <code>tool_schemas.py</code> &rarr; <code>tools.py</code> &rarr; <code>tool_runner.py</code><br/>"
        "• <b>Phase 3 (Workflow Graph):</b> <code>graph.py</code> &rarr; <code>graph_runner.py</code><br/>"
        "• <b>Phase 4 (RAG &amp; Production):</b> <code>rag_data.py</code> &rarr; <code>rag.py</code> &rarr; <code>api_schemas.py</code> &rarr; <code>api.py</code><br/>"
        "• <b>Entry Point &amp; Config:</b> <code>main.py</code>, <code>__init__.py</code>, <code>pyproject.toml</code>",
        s_body
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # PAGE 2: PARSERS.PY
    # ═══════════════════════════════════════════════════════════════
    story.append(section_banner("MODULE 1: DOCUMENT INGESTION", "parsers.py &middot; Clean Text Extraction", "#1E3A8A"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Purpose &amp; Real-World Problem Solved", s_h1))
    story.append(Paragraph(
        "<b>Why this file exists:</b> Before an AI can evaluate a resume, it must read the document. However, resumes are submitted "
        "in various formats (.pdf, .docx, .txt). PDFs in particular are tricky: multi-column resumes (left column: contact info/skills, "
        "right column: work experience) often get scrambled by standard text extractors (which read left-to-right across columns, mixing lines). "
        "<code>parsers.py</code> acts as the universal ingestion gateway that cleans, unifies, and extracts text accurately.",
        s_body
    ))
    story.append(callout(
        "<b>Beginner Gotcha Solved:</b> Naive PDF parsers merge columns horizontally, turning 'Senior Python Engineer' and 'Skills: Guitar' into "
        "'Senior Python Skills: Guitar Engineer'. <code>pdfplumber</code> extracts text using <b>spatial bounding boxes</b> with <code>layout=True</code>, "
        "preserving the natural reading order so the AI never sees jumbled text."
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Libraries &amp; Imports Breakdown", s_h1))
    story.append(make_table([
        [Paragraph("Import Statement", s_th), Paragraph("Library / Module", s_th), Paragraph("Why We Use It (Beginner Explanation)", s_th)],
        [Paragraph("<code>from pathlib import Path</code>", s_tc),
         Paragraph("Standard Library (<code>pathlib</code>)", s_tc),
         Paragraph("Modern object-oriented file path handling (e.g., checking file extension <code>.suffix</code> across Windows and Linux).", s_tc)],
        [Paragraph("<code>from typing import Union, BinaryIO</code>", s_tc),
         Paragraph("Standard Library (<code>typing</code>)", s_tc),
         Paragraph("Type hints that allow functions to accept either a string file path, a <code>Path</code> object, raw <code>bytes</code>, or an open file stream.", s_tc)],
        [Paragraph("<code>import io</code>", s_tc),
         Paragraph("Standard Library (<code>io</code>)", s_tc),
         Paragraph("Provides <code>io.BytesIO</code> to convert in-memory raw binary bytes into a virtual file without saving it to disk first.", s_tc)],
        [Paragraph("<code>import re</code>", s_tc),
         Paragraph("Standard Library (<code>re</code>)", s_tc),
         Paragraph("Regular expressions module used to collapse multiple tabs, spaces, and repeated blank lines into clean paragraph breaks.", s_tc)],
        [Paragraph("<code>import pdfplumber</code>", s_tc),
         Paragraph("Third-Party (<code>pdfplumber</code>)", s_tc),
         Paragraph("Advanced PDF parsing engine that inspects character coordinates, fonts, and bounding boxes to extract multi-column text.", s_tc)],
        [Paragraph("<code>import docx</code>", s_tc),
         Paragraph("Third-Party (<code>python-docx</code>)", s_tc),
         Paragraph("Microsoft Word (.docx) parser used to read both regular body paragraphs and embedded skill/experience table cells.", s_tc)],
    ], [140, 110, 282], C_SECONDARY))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. Function-by-Function Code Walkthrough", s_h1))
    story.append(make_table([
        [Paragraph("Function Name &amp; Signature", s_th), Paragraph("Inputs &amp; Outputs", s_th), Paragraph("Step-by-Step Logic &amp; Internal Mechanics", s_th)],
        [Paragraph("<code>clean_extracted_text(text: str) -&gt; str</code>", s_tcb),
         Paragraph("<b>In:</b> Raw text with messy spacing<br/><b>Out:</b> Clean normalized string", s_tc),
         Paragraph("1. Splits text into lines.<br/>2. Replaces consecutive tabs/spaces with single spaces using regex <code>re.sub(r'[ \\t]+', ' ')</code>.<br/>3. Replaces 3+ consecutive newlines with clean double newlines (paragraphs).", s_tc)],
        [Paragraph("<code>extract_text_from_pdf(file_source) -&gt; str</code>", s_tcb),
         Paragraph("<b>In:</b> Path, bytes, or file stream<br/><b>Out:</b> Clean extracted text", s_tc),
         Paragraph("1. Checks input type: wraps raw bytes in <code>io.BytesIO</code> or opens file path in binary mode ('rb').<br/>2. Loops through all pages using <code>pdfplumber.open()</code>.<br/>3. Calls <code>page.extract_text(layout=True)</code> for spatial alignment.<br/>4. Falls back to standard extraction if layout mode returns empty.<br/>5. Cleans and joins text chunks.", s_tc)],
        [Paragraph("<code>extract_text_from_docx(file_source) -&gt; str</code>", s_tcb),
         Paragraph("<b>In:</b> Path, bytes, or file stream<br/><b>Out:</b> Paragraphs + tables text", s_tc),
         Paragraph("1. Loads document via <code>docx.Document()</code>.<br/>2. Extracts all non-empty paragraphs.<br/>3. Loops through all embedded tables and table rows (resumes frequently put skills in tables).<br/>4. Deduplicates adjacent merged cells and joins text with clean pipe separators (<code>|</code>).", s_tc)],
        [Paragraph("<code>parse_document(file_source, filename) -&gt; str</code>", s_tcb),
         Paragraph("<b>In:</b> Any file format<br/><b>Out:</b> Universal plain text", s_tc),
         Paragraph("1. Inspects file extension (<code>.pdf</code>, <code>.docx</code>, <code>.txt</code>, <code>.md</code>).<br/>2. Automatically dispatches to <code>extract_text_from_pdf</code> or <code>extract_text_from_docx</code>.<br/>3. For text files, safely decodes UTF-8 with <code>errors='ignore'</code>.<br/>4. Raises descriptive <code>ValueError</code> for unsupported files.", s_tc)],
    ], [140, 110, 282], C_SECONDARY))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # PAGE 3: SCHEMAS.PY, EVALUATOR.PY, SAMPLE_DATA.PY
    # ═══════════════════════════════════════════════════════════════
    story.append(section_banner("MODULE 2: PHASE 1 BASELINE &amp; SCHEMAS", "schemas.py &middot; evaluator.py &middot; sample_data.py", "#1E3A8A"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. schemas.py &mdash; Type-Safe Domain Models", s_h1))
    story.append(Paragraph(
        "<b>Why this file exists:</b> If you prompt an LLM to 'give me JSON', it might return missing fields, markdown blocks (<code>```json</code>), "
        "or scores out of range (like 150/100). <code>schemas.py</code> uses <b>Pydantic</b> to define strict contracts that the LLM must follow.",
        s_body
    ))
    story.append(make_table([
        [Paragraph("Model Name", s_th), Paragraph("Fields &amp; Types", s_th), Paragraph("Validation Rules &amp; Purpose", s_th)],
        [Paragraph("<code>BulletOptimization</code>", s_tcb),
         Paragraph("• <code>original_bullet: str</code><br/>• <code>optimized_bullet: str</code><br/>• <code>explanation: str</code>", s_tc),
         Paragraph("Captures a before-and-after rewrite of a resume bullet point along with the reasoning behind the improvement.", s_tc)],
        [Paragraph("<code>SkillGapReport</code>", s_tcb),
         Paragraph("• <code>matched_skills: List[str]</code><br/>• <code>missing_skills: List[str]</code><br/>• <code>reasoning: str</code>", s_tc),
         Paragraph("Isolates which skills from the JD the candidate already possesses versus critical gaps they must address.", s_tc)],
        [Paragraph("<code>ScoringRubric</code>", s_tcb),
         Paragraph("• <code>relevance_score: int</code><br/>• <code>impact_score: int</code><br/>• <code>clarity_score: int</code><br/>• <code>overall_score: int</code>", s_tc),
         Paragraph("Uses Pydantic's <code>Field(ge=0, le=100)</code> constraint. <b>ge=0</b> means greater-than-or-equal-to 0; <b>le=100</b> means less-than-or-equal-to 100. Impossible values are rejected.", s_tc)],
        [Paragraph("<code>ResumeEvaluation</code>", s_tcb),
         Paragraph("• <code>rubric: ScoringRubric</code><br/>• <code>skill_gap: SkillGapReport</code><br/>• <code>bullet_optimizations: List</code><br/>• <code>summary_recommendation: str</code>", s_tc),
         Paragraph("The master container model nesting all sub-reports into a single, complete candidate evaluation dossier.", s_tc)],
    ], [110, 150, 272], C_SECONDARY))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. evaluator.py &mdash; Monolithic Baseline Evaluation Engine", s_h1))
    story.append(Paragraph(
        "<b>Why this file exists:</b> Serves as our Phase 1 baseline. It connects to OpenAI, Gemini, or Groq, feeds in the resume and JD, "
        "and uses <code>.with_structured_output(ResumeEvaluation)</code> to guarantee a 100% valid response conforming to our schema.",
        s_body
    ))
    story.append(make_table([
        [Paragraph("Function / Logic", s_th), Paragraph("Key Libraries Used", s_th), Paragraph("How It Works (Step-by-Step)", s_th)],
        [Paragraph("<code>_get_llm()</code>", s_tcb),
         Paragraph("<code>os</code>, <code>dotenv</code>, <code>langchain_openai</code>, <code>langchain_google_genai</code>, <code>langchain_groq</code>", s_tc),
         Paragraph("1. Loads environment variables via <code>load_dotenv()</code>.<br/>2. Cascades through available API keys: checks OpenAI &rarr; Gemini &rarr; Groq.<br/>3. Instantiates the model with low temperature (0.1) for deterministic output.<br/>4. Returns <code>None</code> if no keys exist, triggering mock fallback.", s_tc)],
        [Paragraph("<code>mock_evaluate_resume(...)</code>", s_tcb),
         Paragraph("<code>schemas.ResumeEvaluation</code>", s_tc),
         Paragraph("Returns a realistic, fully typed <code>ResumeEvaluation</code> object instantly without making external API calls. Crucial for zero-cost automated tests.", s_tc)],
        [Paragraph("<code>evaluate_resume(resume, jd)</code>", s_tcb),
         Paragraph("<code>ChatPromptTemplate</code>, <code>.with_structured_output</code>", s_tc),
         Paragraph("1. Obtains LLM via <code>_get_llm()</code> (routes to mock if None).<br/>2. Compiles system and user prompts.<br/>3. Binds Pydantic schema using <code>llm.with_structured_output(ResumeEvaluation)</code>.<br/>4. Invokes chain and returns validated object.", s_tc)],
    ], [110, 150, 272], C_SECONDARY))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. sample_data.py &mdash; Benchmark Data Strings", s_h1))
    story.append(Paragraph(
        "<b>Why this file exists:</b> Contains curated strings <code>SAMPLE_RESUME</code> (a full-stack developer profile with Python, FastAPI, React) "
        "and <code>SAMPLE_JOB_DESCRIPTION</code> (Senior AI/Python Engineer role). Having consistent benchmark data allows all tests and demos "
        "to run reproducibly without depending on external file uploads.",
        s_body
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # PAGE 4: TOOL_SCHEMAS.PY, TOOLS.PY, TOOL_RUNNER.PY
    # ═══════════════════════════════════════════════════════════════
    story.append(section_banner("MODULE 3: MODULAR AGENT TOOLS", "tool_schemas.py &middot; tools.py &middot; tool_runner.py", "#7C3AED"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Architectural Motivation: Why Decompose into Tools?", s_h1))
    story.append(Paragraph(
        "In Phase 1, a single monolithic prompt asked the LLM to extract skills, compute scores, and rewrite bullets all at once. "
        "This caused 3 major problems: (1) if one part failed, the whole call failed; (2) you couldn't unit-test scoring separately from extraction; "
        "and (3) you couldn't execute steps in parallel. <b>Phase 2 breaks the monolith into three specialized LangChain Tools.</b>",
        s_body
    ))
    story.append(callout(
        "<b>What is a LangChain @tool?</b> When you decorate a Python function with <code>@tool</code>, LangChain inspects the function's name, "
        "its type hints, and its docstring. It converts this information into a JSON Schema specification that an AI agent reads to know "
        "<b>when</b> and <b>how</b> to call your function autonomously.",
        "#F5F3FF", "#8B5CF6",
        ParagraphStyle("P2C", parent=s_body, fontSize=7, leading=9.5, textColor=colors.HexColor("#5B21B6"))
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. tool_schemas.py &mdash; Granular Input/Output Contracts", s_h1))
    story.append(make_table([
        [Paragraph("Schema Class", s_th), Paragraph("Fields &amp; Types", s_th), Paragraph("Purpose / Contract Responsibility", s_th)],
        [Paragraph("<code>ExtractSkillsInput</code>", s_tcb),
         Paragraph("• <code>text: str</code><br/>• <code>source_type: str</code> ('resume'|'jd')", s_tc),
         Paragraph("Validates raw text input before running skill extraction.", s_tc)],
        [Paragraph("<code>ExtractedSkills</code>", s_tcb),
         Paragraph("• <code>technical_skills: List[str]</code><br/>• <code>soft_skills: List[str]</code><br/>• <code>years_of_experience: float</code>", s_tc),
         Paragraph("Strict output schema returned by the extraction tool.", s_tc)],
        [Paragraph("<code>MatchScoreInput</code>", s_tcb),
         Paragraph("• <code>resume_skills: ExtractedSkills</code><br/>• <code>jd_skills: ExtractedSkills</code>", s_tc),
         Paragraph("Requires pre-extracted skills from both sources before computing alignment.", s_tc)],
        [Paragraph("<code>MatchScoreOutput</code>", s_tcb),
         Paragraph("• <code>matched_skills: List[str]</code><br/>• <code>missing_skills: List[str]</code><br/>• <code>match_score: int</code><br/>• <code>rationale: str</code>", s_tc),
         Paragraph("Quantified match result with 0-100 score and explanation.", s_tc)],
        [Paragraph("<code>RewriteInput</code>", s_tcb),
         Paragraph("• <code>bullets: List[str]</code><br/>• <code>target_role: str</code><br/>• <code>rag_context: Optional[dict]</code>", s_tc),
         Paragraph("Inputs for bullet optimization; includes optional Phase 4 RAG reference context.", s_tc)],
        [Paragraph("<code>RewriteOutput</code>", s_tcb),
         Paragraph("• <code>rewritten_bullets: List[RewrittenBullet]</code><br/>• <code>overall_improvement: str</code>", s_tc),
         Paragraph("List of optimized bullets following Google XYZ formula.", s_tc)],
    ], [110, 160, 262], C_PURPLE))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. tools.py &mdash; The Three Agent Tools", s_h1))
    story.append(make_table([
        [Paragraph("Tool Name &amp; Decorator", s_th), Paragraph("Arguments &amp; Returns", s_th), Paragraph("Internal Execution &amp; Mock Fallback", s_th)],
        [Paragraph("<code>@tool(args_schema=...)<br/>extract_skills</code>", s_tcb),
         Paragraph("<b>In:</b> text, source_type<br/><b>Out:</b> dict (ExtractedSkills)", s_tc),
         Paragraph("1. Checks API keys via <code>_get_llm()</code>.<br/>2. If keys missing, calls <code>_mock_extract_skills()</code> returning typed data.<br/>3. If keys present, prompts LLM with recruitment instructions and <code>.with_structured_output(ExtractedSkills)</code>.<br/>4. Normalizes skill casing (lowercase, stripped).", s_tc)],
        [Paragraph("<code>@tool(args_schema=...)<br/>compute_match_score</code>", s_tcb),
         Paragraph("<b>In:</b> resume_skills, jd_skills<br/><b>Out:</b> dict (MatchScoreOutput)", s_tc),
         Paragraph("1. Compares technical and soft skills between resume and JD.<br/>2. Uses mathematical set operations (intersections &amp; differences) for deterministic matching.<br/>3. Computes weighted alignment score (60% technical, 20% soft skills, 20% experience).<br/>4. Generates concise rationale explaining the score.", s_tc)],
        [Paragraph("<code>@tool(args_schema=...)<br/>suggest_rewrite</code>", s_tcb),
         Paragraph("<b>In:</b> bullets, target_role, rag_context<br/><b>Out:</b> dict (RewriteOutput)", s_tc),
         Paragraph("1. Takes unpolished resume bullets.<br/>2. Injects Phase 4 RAG best practice examples if provided in <code>rag_context</code>.<br/>3. Prompts LLM to rewrite each bullet into Google XYZ format (<i>Accomplished [X] by doing [Z] as measured by [Y]</i>).<br/>4. Returns structured improvements and action verbs.", s_tc)],
    ], [110, 140, 282], C_PURPLE))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4. tool_runner.py &mdash; Isolated Verification Runner", s_h1))
    story.append(Paragraph(
        "<b>Why this file exists:</b> Demonstrates how to invoke tools independently without launching an agent. "
        "Calls <code>extract_skills.invoke({...})</code> and <code>compute_match_score.invoke({...})</code> using sample data "
        "and prints formatted JSON to verify that inputs and outputs conform strictly to schema contracts.",
        s_body
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # PAGE 5: GRAPH.PY, GRAPH_RUNNER.PY
    # ═══════════════════════════════════════════════════════════════
    story.append(section_banner("MODULE 4: WORKFLOW ORCHESTRATION", "graph.py &middot; graph_runner.py &middot; LangGraph State Machine", "#059669"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Why LangGraph? State Machines vs Linear Chains", s_h1))
    story.append(Paragraph(
        "Standard LangChain chains execute linearly (A &rarr; B &rarr; C). If step B needs both resume skills and JD skills, a linear chain "
        "must run them one after another. <b>LangGraph introduces a directed cyclical state machine.</b> It allows parallel nodes, "
        "central state tracking via TypedDict, and persistent checkpointing so workflows can pause and wait for human review.",
        s_body
    ))
    story.append(callout(
        "<b>The Central State Pattern:</b> Think of <code>AgentState</code> as a shared Google Doc that every worker node reads from and writes to. "
        "When a node finishes, it doesn't pass data directly to the next worker; instead, it returns a partial dictionary that LangGraph "
        "merges into the central state. Every downstream node automatically sees the updated document.",
        "#ECFDF5", "#10B981",
        ParagraphStyle("P3C", parent=s_body, fontSize=7, leading=9.5, textColor=C_GREEN)
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. graph.py &mdash; AgentState Schema Breakdown", s_h1))
    story.append(make_table([
        [Paragraph("State Key", s_th), Paragraph("Type", s_th), Paragraph("Lifecycle &amp; Which Node Populates It", s_th)],
        [Paragraph("<code>resume_text</code>, <code>jd_text</code>", s_tcb), Paragraph("<code>str</code>", s_tc), Paragraph("Supplied at entry point by the user/caller upon invoking the graph.", s_tc)],
        [Paragraph("<code>target_role</code>", s_tcb), Paragraph("<code>str</code>", s_tc), Paragraph("Optional role name (e.g. 'Senior AI Engineer') to focus bullet rewrites.", s_tc)],
        [Paragraph("<code>resume_skills</code>", s_tcb), Paragraph("<code>Optional[dict]</code>", s_tc), Paragraph("Populated concurrently by <code>extract_resume_node</code>.", s_tc)],
        [Paragraph("<code>jd_skills</code>", s_tcb), Paragraph("<code>Optional[dict]</code>", s_tc), Paragraph("Populated concurrently by <code>extract_jd_node</code>.", s_tc)],
        [Paragraph("<code>match_results</code>", s_tcb), Paragraph("<code>Optional[dict]</code>", s_tc), Paragraph("Populated by <code>compute_score_node</code> once both extractions complete.", s_tc)],
        [Paragraph("<code>rewrites</code>", s_tcb), Paragraph("<code>Optional[dict]</code>", s_tc), Paragraph("Populated by <code>optimize_bullets_node</code> using XYZ formula.", s_tc)],
        [Paragraph("<code>final_report</code>", s_tcb), Paragraph("<code>Optional[dict]</code>", s_tc), Paragraph("Assembled by <code>aggregate_report_node</code>; contains full evaluation summary.", s_tc)],
        [Paragraph("<code>rag_context</code>", s_tcb), Paragraph("<code>Optional[dict]</code>", s_tc), Paragraph("Phase 4: Populated by <code>retrieve_context_node</code> with retrieved best practices.", s_tc)],
        [Paragraph("<code>human_approval</code>, <code>reviewed_rewrites</code>", s_tcb), Paragraph("<code>Optional[str/dict]</code>", s_tc), Paragraph("Phase 4: Set by human reviewer during HITL pause/resume flow.", s_tc)],
    ], [110, 110, 312], C_EMERALD))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. Graph Node Functions &amp; Workflow Compilers", s_h1))
    story.append(make_table([
        [Paragraph("Node / Compiler Function", s_th), Paragraph("Inputs &amp; Outputs", s_th), Paragraph("What It Does (Step-by-Step Mechanics)", s_th)],
        [Paragraph("<code>extract_resume_node</code>", s_tcb),
         Paragraph("<b>In:</b> state['resume_text']<br/><b>Out:</b> {'resume_skills': ...}", s_tc),
         Paragraph("Calls <code>extract_skills.invoke({'text': ..., 'source_type': 'resume'})</code> and writes to state.", s_tc)],
        [Paragraph("<code>extract_jd_node</code>", s_tcb),
         Paragraph("<b>In:</b> state['jd_text']<br/><b>Out:</b> {'jd_skills': ...}", s_tc),
         Paragraph("Calls <code>extract_skills.invoke({'text': ..., 'source_type': 'jd'})</code> concurrently with resume extraction.", s_tc)],
        [Paragraph("<code>compute_score_node</code>", s_tcb),
         Paragraph("<b>In:</b> resume_skills, jd_skills<br/><b>Out:</b> {'match_results': ...}", s_tc),
         Paragraph("Acts as synchronization barrier: waits for both parallel extractions to finish, then calls <code>compute_match_score</code>.", s_tc)],
        [Paragraph("<code>optimize_bullets_node</code>", s_tcb),
         Paragraph("<b>In:</b> resume_text, rag_context<br/><b>Out:</b> {'rewrites': ...}", s_tc),
         Paragraph("Extracts action bullets from resume, injects RAG context if present, and invokes <code>suggest_rewrite</code>.", s_tc)],
        [Paragraph("<code>aggregate_report_node</code>", s_tcb),
         Paragraph("<b>In:</b> All state fields<br/><b>Out:</b> {'final_report': ...}", s_tc),
         Paragraph("Consolidates scores, skill gaps, approved rewrites, and metadata into the final deliverable dictionary.", s_tc)],
        [Paragraph("<code>compile_workflow()</code>", s_tcb),
         Paragraph("<b>Returns:</b> Compiled Graph", s_tc),
         Paragraph("Builds original Phase 3 DAG: START &rarr; [extract_resume &amp; extract_jd] &rarr; compute_score &rarr; optimize_bullets &rarr; aggregate &rarr; END.", s_tc)],
        [Paragraph("<code>compile_rag_workflow()</code>", s_tcb),
         Paragraph("<b>Returns:</b> Compiled Graph", s_tc),
         Paragraph("Phase 4 variant: inserts <code>retrieve_context_node</code> between extraction and scoring to ground rewrites.", s_tc)],
        [Paragraph("<code>compile_hitl_workflow(checkpointer)</code>", s_tcb),
         Paragraph("<b>Returns:</b> Compiled Graph", s_tc),
         Paragraph("Phase 4 HITL variant: inserts <code>human_review_node</code> with <code>interrupt()</code> to pause for human approval.", s_tc)],
    ], [130, 120, 282], C_EMERALD))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4. graph_runner.py &mdash; Workflow Execution Engine", s_h1))
    story.append(Paragraph(
        "<b>Why this file exists:</b> Compiles the graph using <code>compile_workflow()</code>, loads sample texts, builds the initial "
        "<code>AgentState</code> dictionary, and invokes the workflow via <code>app.invoke(initial_state)</code>. It demonstrates how "
        "data flows through all nodes from START to END and prints the final aggregated report.",
        s_body
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # PAGE 6: RAG_DATA.PY, RAG.PY
    # ═══════════════════════════════════════════════════════════════
    story.append(section_banner("MODULE 5: FAISS VECTOR RAG PIPELINE", "rag_data.py &middot; rag.py &middot; Semantic Retrieval", "#DC2626"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Purpose: Why RAG is Essential for Resume Agents", s_h1))
    story.append(Paragraph(
        "When an LLM rewrites resume bullets from scratch, it tends to hallucinate false statistics (e.g. 'boosted revenue by 400%') "
        "or use generic buzzwords. <b>RAG (Retrieval-Augmented Generation) solves this</b> by indexing curated, real-world examples. "
        "Before rewriting, the system retrieves the 3 most relevant high-impact XYZ formula exemplars and feeds them to the LLM as style guides.",
        s_body
    ))
    story.append(callout(
        "<b>How Vector Embeddings Work in Plain English:</b> An embedding model converts a sentence into 384 decimal numbers. "
        "Sentences with similar meanings end up close together in mathematical space. If a bullet mentions 'Docker and Kubernetes', "
        "FAISS calculates the cosine distance to all indexed examples in less than 1 millisecond and retrieves the best DevOps templates.",
        "#FEE2E2", "#DC2626",
        ParagraphStyle("P4C", parent=s_body, fontSize=7, leading=9.5, textColor=colors.HexColor("#991B1B"))
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. rag_data.py &mdash; Curated Benchmark Corpora", s_h1))
    story.append(make_table([
        [Paragraph("Corpus Constant", s_th), Paragraph("Data Structure &amp; Scope", s_th), Paragraph("Purpose / Content Details", s_th)],
        [Paragraph("<code>SAMPLE_JD_CORPUS</code>", s_tcb),
         Paragraph("List of 5 dicts<br/>(id, title, company, text)", s_tc),
         Paragraph("Diverse corporate JDs: Senior AI Engineer, Full-Stack Developer, DevOps/Cloud Architect, ML Engineer, and Backend Specialist. Used for auto-matching candidate resumes.", s_tc)],
        [Paragraph("<code>BEST_PRACTICES_CORPUS</code>", s_tcb),
         Paragraph("List of 15 dicts<br/>(id, domain, original, xyz, reason)", s_tc),
         Paragraph("Curated before-and-after bullet rewrites following Google XYZ formula across AI/ML, Full-Stack, Backend, and DevOps. Explains <i>why</i> the rewrite is effective.", s_tc)],
    ], [110, 140, 282], C_CRIMSON))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. rag.py &mdash; FAISS Vector Indexing &amp; Retrieval Engine", s_h1))
    story.append(make_table([
        [Paragraph("Function Name", s_th), Paragraph("Libraries Used", s_th), Paragraph("What It Does (Step-by-Step Implementation)", s_th)],
        [Paragraph("<code>get_embeddings()</code>", s_tcb),
         Paragraph("<code>langchain_huggingface</code>,<br/><code>sentence-transformers</code>", s_tc),
         Paragraph("1. Loads <code>all-MiniLM-L6-v2</code> embedding model via HuggingFace.<br/>2. Configures execution on CPU (zero GPU requirement).<br/>3. Completely free and runs 100% locally with zero external API calls or rate limits.<br/>4. Returns <code>None</code> if sentence-transformers is not installed, enabling graceful fallback.", s_tc)],
        [Paragraph("<code>build_jd_index(...)</code>", s_tcb),
         Paragraph("<code>FAISS</code>, <code>Document</code>", s_tc),
         Paragraph("1. Converts raw JD corpus into LangChain <code>Document</code> objects with metadata.<br/>2. Generates 384-dimensional vector embeddings for each document.<br/>3. Builds an in-memory FAISS L2/Cosine index.<br/>4. Caches index in global <code>_jd_vectorstore</code> singleton to prevent redundant re-indexing.", s_tc)],
        [Paragraph("<code>retrieve_similar_jds(...)</code>", s_tcb),
         Paragraph("<code>FAISS.similarity_search_with_score</code>", s_tc),
         Paragraph("1. Takes raw candidate resume text.<br/>2. Embeds resume and performs nearest-neighbor vector search against FAISS index.<br/>3. Converts L2 distance to 0-100 similarity percentage score.<br/>4. Returns top-k matching JDs with titles and relevance scores.", s_tc)],
        [Paragraph("<code>build_best_practices_index()</code>", s_tcb),
         Paragraph("<code>FAISS</code>, <code>Document</code>", s_tc),
         Paragraph("1. Indexes all 15 XYZ formula best practice bullets.<br/>2. Caches index in <code>_bp_vectorstore</code> for instant repeated retrievals.", s_tc)],
        [Paragraph("<code>retrieve_rewrite_context(...)</code>", s_tcb),
         Paragraph("<code>FAISS.similarity_search</code>", s_tc),
         Paragraph("1. Takes raw bullet and target role.<br/>2. Queries FAISS store for the most semantically relevant XYZ examples in that domain.<br/>3. Returns list of reference exemplars for prompt injection.", s_tc)],
    ], [125, 135, 272], C_CRIMSON))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # PAGE 7: API_SCHEMAS.PY, API.PY
    # ═══════════════════════════════════════════════════════════════
    story.append(section_banner("MODULE 6: REST API &amp; HUMAN-IN-THE-LOOP", "api_schemas.py &middot; api.py &middot; Production Serving", "#DC2626"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Why Build a REST API? Moving from Scripts to Services", s_h1))
    story.append(Paragraph(
        "CLI scripts are great for testing, but in production, AI agents must be accessible by web apps, mobile clients, and enterprise "
        "ATS systems. <b>FastAPI exposes our entire pipeline as high-speed HTTP REST endpoints</b> with automatic Swagger documentation. "
        "It also manages stateful Human-in-the-Loop (HITL) review sessions across stateless HTTP requests.",
        s_body
    ))
    story.append(callout(
        "<b>How Human-in-the-Loop Works Over HTTP:</b> HTTP is stateless, but LangGraph HITL is stateful. When a client calls "
        "<code>/api/v1/evaluate/hitl</code>, the graph executes up to <code>human_review_node</code> and pauses using <code>interrupt()</code>. "
        "LangGraph's <code>MemorySaver</code> checkpointer saves the exact execution state keyed by a <code>thread_id</code>. "
        "Later, a reviewer submits their decision to <code>/api/v1/evaluate/hitl/{thread_id}/review</code>; the API loads the checkpoint, "
        "calls <code>Command(resume=...)</code>, and finalizes the report seamlessly.",
        "#FEE2E2", "#DC2626",
        ParagraphStyle("P4API", parent=s_body, fontSize=7, leading=9.5, textColor=colors.HexColor("#991B1B"))
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. api_schemas.py &mdash; Request &amp; Response Envelopes", s_h1))
    story.append(make_table([
        [Paragraph("Pydantic Schema", s_th), Paragraph("HTTP Method &amp; Route", s_th), Paragraph("Fields &amp; Validation Purpose", s_th)],
        [Paragraph("<code>EvaluateRequest</code>", s_tcb), Paragraph("POST <code>/api/v1/evaluate</code>", s_tc), Paragraph("Validates that <code>resume_text</code> and <code>jd_text</code> are non-empty strings before running the pipeline.", s_tc)],
        [Paragraph("<code>RAGEvaluateRequest</code>", s_tcb), Paragraph("POST <code>/api/v1/evaluate/rag</code>", s_tc), Paragraph("Requires only <code>resume_text</code> + <code>target_role</code>; JD is automatically retrieved from FAISS.", s_tc)],
        [Paragraph("<code>HITLReviewRequest</code>", s_tcb), Paragraph("POST <code>.../review</code>", s_tc), Paragraph("Accepts reviewer <code>action</code> ('approve'|'reject'|'edit'), optional <code>feedback</code>, and modified bullets.", s_tc)],
        [Paragraph("<code>HealthResponse</code>", s_tcb), Paragraph("GET <code>/health</code>", s_tc), Paragraph("Returns API status, version ('0.1.0'), active phases ('Phases 1-4'), and timestamp.", s_tc)],
    ], [110, 120, 302], colors.HexColor("#DC2626")))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. api.py &mdash; Endpoints &amp; Checkpointing Mechanics", s_h1))
    story.append(make_table([
        [Paragraph("Endpoint &amp; Method", s_th), Paragraph("Pipeline Invoked", s_th), Paragraph("Step-by-Step Server Execution Flow", s_th)],
        [Paragraph("<code>GET /health</code>", s_tcb), Paragraph("System Health", s_tc), Paragraph("Returns 200 OK with server metadata for Kubernetes/Docker health probes.", s_tc)],
        [Paragraph("<code>POST /api/v1/evaluate</code>", s_tcb), Paragraph("Standard LangGraph", s_tc), Paragraph("1. Receives resume and JD text.<br/>2. Dispatches to compiled Phase 3 state graph.<br/>3. Returns complete <code>final_report</code> containing scores, gaps, and rewrites.", s_tc)],
        [Paragraph("<code>POST /api/v1/evaluate/rag</code>", s_tcb), Paragraph("RAG State Graph", s_tc), Paragraph("1. Searches FAISS for top matching JD if not provided.<br/>2. Retrieves best practice exemplars.<br/>3. Executes RAG workflow and returns grounded evaluation.", s_tc)],
        [Paragraph("<code>POST /api/v1/evaluate/hitl</code>", s_tcb), Paragraph("HITL Workflow (Pause)", s_tc), Paragraph("1. Generates unique <code>thread_id</code> (UUID).<br/>2. Runs HITL graph until <code>human_review_node</code> interrupts.<br/>3. Returns pending rewrites and thread_id to the reviewer.", s_tc)],
        [Paragraph("<code>POST .../{id}/review</code>", s_tcb), Paragraph("HITL Workflow (Resume)", s_tc), Paragraph("1. Validates thread_id exists.<br/>2. Loads saved state from <code>MemorySaver</code>.<br/>3. Resumes execution with <code>Command(resume=...)</code>.<br/>4. Graph finishes aggregation and returns final report.", s_tc)],
        [Paragraph("<code>GET /api/v1/similar-jds</code>", s_tcb), Paragraph("FAISS Search", s_tc), Paragraph("Standalone endpoint allowing candidates to find matching corporate jobs from text.", s_tc)],
    ], [120, 110, 302], colors.HexColor("#DC2626")))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # PAGE 8: MAIN.PY, PACKAGING & MASTERY CHECKLIST
    # ═══════════════════════════════════════════════════════════════
    story.append(section_banner("MODULE 7: CLI, PACKAGING &amp; MASTERY", "main.py &middot; pyproject.toml &middot; Beginner Roadmap", "#0F172A"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. main.py &mdash; Unified Command-Line Interface", s_h1))
    story.append(Paragraph(
        "<b>Why this file exists:</b> Provides a single terminal entry point to run any phase of the project. "
        "Uses Python's standard <code>argparse</code> library to parse flags, reads files via <code>parsers.py</code>, and routes execution.",
        s_body
    ))
    story.append(make_table([
        [Paragraph("CLI Flag / Command", s_th), Paragraph("Subsystem Executed", s_th), Paragraph("What It Runs Under the Hood", s_th)],
        [Paragraph("<code>agentic-ai</code> (default)", s_tcb), Paragraph("Phase 3 LangGraph", s_tc), Paragraph("Runs the full autonomous workflow on built-in sample data and prints report.", s_tc)],
        [Paragraph("<code>--phase1</code>", s_tcb), Paragraph("Phase 1 Baseline", s_tc), Paragraph("Runs monolithic <code>evaluator.py</code> baseline engine.", s_tc)],
        [Paragraph("<code>--phase2</code>", s_tcb), Paragraph("Phase 2 Tools Demo", s_tc), Paragraph("Runs <code>tool_runner.py</code> to test tools in isolation.", s_tc)],
        [Paragraph("<code>--phase4-rag</code>", s_tcb), Paragraph("Phase 4 RAG Pipeline", s_tc), Paragraph("Builds FAISS index, retrieves similar JDs, and grounds bullet rewrites.", s_tc)],
        [Paragraph("<code>--phase4-api</code>", s_tcb), Paragraph("FastAPI Server", s_tc), Paragraph("Spawns Uvicorn server hosting REST API at <code>http://localhost:8000/docs</code>.", s_tc)],
        [Paragraph("<code>--phase4-hitl</code>", s_tcb), Paragraph("HITL Terminal Demo", s_tc), Paragraph("Simulates interactive human approval: prompts user in terminal to approve rewrites.", s_tc)],
        [Paragraph("<code>--resume FILE --jd FILE</code>", s_tcb), Paragraph("Custom File Inputs", s_tc), Paragraph("Passes custom PDF or Word files to <code>parse_document()</code> for evaluation.", s_tc)],
    ], [115, 115, 302], C_PRIMARY))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Project Configuration &amp; Packaging (pyproject.toml)", s_h1))
    story.append(Paragraph(
        "• <b><code>pyproject.toml</code>:</b> The modern standard for Python packaging (PEP 621). Defines metadata, dependencies, "
        "and registers the terminal command <code>agentic-ai = 'agentic_ai:main'</code> so you can run it anywhere.<br/>"
        "• <b><code>__init__.py</code>:</b> Marks <code>src/agentic_ai</code> as an importable Python package and exports top-level symbols "
        "like <code>evaluate_resume</code> and <code>parse_document</code>.<br/>"
        "• <b><code>uv</code> Package Manager:</b> Used to install dependencies into an isolated virtual environment (<code>.venv</code>) "
        "with sub-second speed, replacing legacy pip and poetry.",
        s_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. 10-Step Beginner Mastery Roadmap", s_h1))
    story.append(make_table([
        [Paragraph("Step", s_th), Paragraph("Learning Action", s_th), Paragraph("Key Insight Gained", s_th)],
        [Paragraph("1", s_tcb), Paragraph("Open <code>parsers.py</code>", s_tc), Paragraph("Learn how to extract text from PDFs and Word docs without jumbling multi-column layouts.", s_tc)],
        [Paragraph("2", s_tcb), Paragraph("Inspect <code>schemas.py</code>", s_tc), Paragraph("Master Pydantic bounds (<code>ge=0, le=100</code>) to force AI outputs into strict types.", s_tc)],
        [Paragraph("3", s_tcb), Paragraph("Run <code>tool_runner.py</code>", s_tc), Paragraph("Understand how LangChain's <code>@tool</code> decorator turns Python functions into agent tools.", s_tc)],
        [Paragraph("4", s_tcb), Paragraph("Trace <code>graph.py</code>", s_tc), Paragraph("See how LangGraph passes state between parallel nodes and manages synchronization.", s_tc)],
        [Paragraph("5", s_tcb), Paragraph("Examine <code>rag.py</code>", s_tc), Paragraph("Learn how FAISS vector embeddings ground AI text generation in real-world examples.", s_tc)],
        [Paragraph("6", s_tcb), Paragraph("Launch <code>api.py</code>", s_tc), Paragraph("Visit <code>http://localhost:8000/docs</code> to see interactive Swagger API documentation.", s_tc)],
        [Paragraph("7", s_tcb), Paragraph("Test HITL Pause/Resume", s_tc), Paragraph("Experience how LangGraph's <code>interrupt()</code> pauses execution for human approval.", s_tc)],
        [Paragraph("8", s_tcb), Paragraph("Review Mock Fallbacks", s_tc), Paragraph("Learn how to build production test suites that run 100% locally with zero API costs.", s_tc)],
        [Paragraph("9", s_tcb), Paragraph("Run Pytest Suite", s_tc), Paragraph("Run <code>uv run pytest tests/ -v</code> and watch 38 unit tests pass across all four phases.", s_tc)],
        [Paragraph("10", s_tcb), Paragraph("Build Your Own Agent", s_tc), Paragraph("Combine Parsers + Tools + StateGraph + RAG + FastAPI for your own domain projects!", s_tc)],
    ], [35, 155, 342], C_PRIMARY))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[Code Walkthrough PDF] Successfully compiled: {output_path}")


if __name__ == "__main__":
    output_filename = "Agentic_AI_Beginner_Codebase_Walkthrough.pdf"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    build_pdf(output_filename)
