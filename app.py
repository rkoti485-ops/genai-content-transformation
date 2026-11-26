import streamlit as st
from pathlib import Path

from modules.text_extract import extract_text
from modules.ai_engine import transform_text, check_ollama
from modules.quiz_generator import generate_quiz
from modules.workflows import run_full_workflow
from modules.database import init_db, save_record, get_history
from modules.analytics import get_analytics

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GenAI Content Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- APP SETUP ----------------
init_db()

def load_css():
    css_file = Path("assets/styles.css")
    if css_file.exists():
        st.markdown(f"<style>{css_file.read_text(encoding='utf-8')}</style>",
                    unsafe_allow_html=True)

load_css()

if "model" not in st.session_state:
    st.session_state.model = "llama3.2"
if "last_result" not in st.session_state:
    st.session_state.last_result = ""
if "workflow_results" not in st.session_state:
    st.session_state.workflow_results = {}
if "source_text" not in st.session_state:
    st.session_state.source_text = ""
if "source_name" not in st.session_state:
    st.session_state.source_name = "Pasted text"


# ---------------- REUSABLE UI HELPERS ----------------
def page_header(eyebrow, title, subtitle):
    st.markdown(f'<div class="eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="page-subtitle">{subtitle}</p>', unsafe_allow_html=True)

def read_source():
    st.markdown("### 1. Add your content")
    uploaded = st.file_uploader(
        "Upload a document",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, Word DOCX and plain text TXT."
    )
    pasted = st.text_area(
        "Or paste text directly",
        height=190,
        placeholder="Paste your study material, article, notes or other content here..."
    )

    source = ""
    source_name = "Pasted text"

    if uploaded is not None:
        try:
            source = extract_text(uploaded)
            source_name = uploaded.name
            if source.strip():
                st.success(f"Successfully read {uploaded.name} • {len(source.split())} words")
            else:
                st.warning("No readable text was found. If this is a scanned PDF, OCR is required.")
        except Exception as error:
            st.error(f"Could not read this file: {error}")
    elif pasted.strip():
        source = pasted.strip()

    if source:
        st.session_state.source_text = source
        st.session_state.source_name = source_name

    return source, source_name

def save_and_show(result, source, source_name, task, model):
    st.session_state.last_result = result
    st.session_state.last_task = task
    save_record(source_name, task, len(source.split()), result, model)

def output_panel(result, filename="genai_output"):
    st.markdown("### Generated result")
    st.markdown('<div class="result-panel">', unsafe_allow_html=True)
    st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)
    st.download_button(
        "⬇ Download as TXT",
        data=result.encode("utf-8"),
        file_name=f"{filename}.txt",
        mime="text/plain",
        type="primary"
    )


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("# ✨ GenAI Studio")
    st.caption("SMART CONTENT TRANSFORMATION")
    st.markdown("---")

    selected_page = st.radio(
        "WORKSPACE",
        ["Overview", "Content Transformer", "AI Workflow", "History", "Analytics", "About"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**AI configuration**")
    st.session_state.model = st.text_input(
        "Ollama model",
        value=st.session_state.model,
        help="Must match a model installed in Ollama, e.g. llama3.2."
    )
    if st.button("Test AI connection", use_container_width=True):
        connected, message = check_ollama(st.session_state.model)
        if connected:
            st.success(message)
        else:
            st.error(message)

    st.markdown("---")
    st.caption("CDS208 • Emerging Tools and Applications")
    st.caption("Built by Team GenAI")


# ---------------- OVERVIEW ----------------
if selected_page == "Overview":
    page_header(
        "YOUR AI-POWERED WORKSPACE",
        "Turn documents into useful content.",
        "Upload or paste information and let Generative AI transform it into summaries, notes, quizzes and reports."
    )

    st.markdown("""
    <div class="hero-card">
      <div class="hero-tag">GENERATIVE AI • CONTENT AUTOMATION</div>
      <h2>One document. Many possibilities.</h2>
      <p>Save time by transforming long content into clear, structured and reusable learning resources.</p>
    </div>
    """, unsafe_allow_html=True)

    history = get_history()
    total = len(history)
    total_words = sum(int(item.get("word_count") or 0) for item in history)
    c1, c2, c3 = st.columns(3)
    c1.metric("Transformations completed", total)
    c2.metric("Source words processed", f"{total_words:,}")
    c3.metric("AI model", st.session_state.model)

    st.markdown("### Explore the workspace")
    cards = st.columns(3)
    features = [
        ("📝", "Smart summaries", "Condense long documents into key ideas."),
        ("📚", "Study notes", "Organize concepts into readable notes."),
        ("🧠", "Quiz generator", "Create multiple-choice questions."),
        ("📄", "Report writer", "Generate structured reports."),
        ("💬", "Question & answer", "Create revision questions with answers."),
        ("⚡", "Automated workflow", "Generate several resources from one input.")
    ]
    for index, feature in enumerate(features):
        with cards[index % 3]:
            st.markdown(
                f'<div class="feature-card"><div class="feature-icon">{feature[0]}</div>'
                f'<h4>{feature[1]}</h4><p>{feature[2]}</p></div>',
                unsafe_allow_html=True
            )

    st.info("Choose **Content Transformer** in the sidebar to generate your first result.")


# ---------------- CONTENT TRANSFORMER ----------------
elif selected_page == "Content Transformer":
    page_header(
        "CREATE WITH AI",
        "Content transformer",
        "Choose an output format and customize how the AI writes your content."
    )
    source, source_name = read_source()

    st.markdown("### 2. Choose transformation settings")
    left, right = st.columns(2)
    with left:
        task = st.selectbox(
            "Output format",
            ["Summary", "Study Notes", "Report", "Question & Answer", "Simplify Text", "Key Points"]
        )
        detail = st.select_slider("Level of detail", options=["Short", "Medium", "Detailed"], value="Medium")
    with right:
        tone = st.selectbox(
            "Writing style",
            ["Clear and simple", "Student-friendly", "Academic", "Professional"]
        )
        st.caption("Tip: Use 'Detailed' for revision notes and 'Short' for quick summaries.")

    if st.button("✨ Generate content", type="primary", use_container_width=True, disabled=not bool(source.strip())):
        with st.spinner(f"Generating {task.lower()} with {st.session_state.model}..."):
            try:
                result = transform_text(source, task, detail, tone, st.session_state.model)
                save_and_show(result, source, source_name, task, st.session_state.model)
                st.success("Your content has been generated.")
            except Exception as error:
                st.error(str(error))

    if st.session_state.last_result:
        output_panel(
            st.session_state.last_result,
            st.session_state.get("last_task", "genai_output").lower().replace(" ", "_")
        )


# ---------------- AUTOMATED WORKFLOW ----------------
elif selected_page == "AI Workflow":
    page_header(
        "AUTOMATE MULTIPLE TASKS",
        "AI content workflow",
        "Use one source document to create a complete learning pack in a single workflow."
    )
    source, source_name = read_source()

    st.markdown("""
    <div class="workflow-strip">
      <span>01 · Source document</span><b>→</b>
      <span>02 · AI processing</span><b>→</b>
      <span>03 · Learning pack</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚡ Run complete workflow", type="primary", use_container_width=True, disabled=not bool(source.strip())):
        try:
            with st.spinner("Running summary, notes, Q&A and quiz generation..."):
                results = run_full_workflow(source, st.session_state.model)
                st.session_state.workflow_results = results
                for task_name, result in results.items():
                    save_record(source_name, f"Workflow: {task_name}", len(source.split()), str(result), st.session_state.model)
            st.success("Workflow completed successfully.")
        except Exception as error:
            st.error(str(error))

    if st.session_state.workflow_results:
        for task_name, result in st.session_state.workflow_results.items():
            with st.expander(f"📌 {task_name}", expanded=True):
                st.markdown(result)
                st.download_button(
                    f"Download {task_name}",
                    data=result.encode("utf-8"),
                    file_name=f"{task_name.lower().replace(' ', '_')}.txt",
                    mime="text/plain",
                    key=f"workflow_download_{task_name}"
                )


# ---------------- HISTORY ----------------
elif selected_page == "History":
    page_header("YOUR SAVED WORK", "Transformation history", "Revisit and download content generated in earlier sessions.")
    records = get_history()
    if not records:
        st.info("No saved transformations yet. Generate content to build your history.")
    else:
        st.caption(f"{len(records)} recent records")
        for record in records:
            label = f"{record['created_at']}  ·  {record['task']}  ·  {record['source_name']}"
            with st.expander(label):
                st.caption(f"Input words: {record['word_count']} | Model: {record['model']}")
                st.markdown(record["output"])
                st.download_button(
                    "Download result",
                    data=record["output"].encode("utf-8"),
                    file_name=f"history_{record['id']}.txt",
                    mime="text/plain",
                    key=f"history_download_{record['id']}"
                )


# ---------------- ANALYTICS ----------------
elif selected_page == "Analytics":
    page_header("MEASURE YOUR ACTIVITY", "Usage analytics", "Understand how the platform is being used and export data for Power BI.")
    data = get_analytics()
    a, b, c = st.columns(3)
    a.metric("Total generations", data["total"])
    b.metric("Input words processed", f"{data['words']:,}")
    c.metric("Most-used task", data["top_task"])

    if not data["by_task"].empty:
        st.markdown("### Generations by task")
        st.bar_chart(data["by_task"].set_index("task"))
        st.markdown("### Recent activity")
        st.dataframe(data["recent"], use_container_width=True, hide_index=True)
    else:
        st.info("Analytics will appear after the first content transformation.")

    st.download_button(
        "⬇ Export CSV for Power BI",
        data=data["csv"].encode("utf-8"),
        file_name="genai_analytics.csv",
        mime="text/csv",
        type="primary"
    )


# ---------------- ABOUT ----------------
elif selected_page == "About":
    page_header("PROJECT INFORMATION", "About GenAI Studio", "A CDS208 prototype demonstrating Generative AI and automated content transformation.")
    st.markdown("""
    <div class="about-card">
      <h3>Project objective</h3>
      <p>To reduce the effort involved in converting long documents into useful learning and communication formats.</p>
      <h3>How it works</h3>
      <ol>
        <li>User uploads a PDF, DOCX or TXT file, or pastes text.</li>
        <li>The application extracts readable text.</li>
        <li>Prompt templates define the requested transformation.</li>
        <li>Ollama runs the selected local language model.</li>
        <li>The generated result can be viewed, downloaded and saved in history.</li>
      </ol>
      <h3>Technology stack</h3>
      <p>Python · Streamlit · Ollama · Prompt Engineering · SQLite · Pandas · Power BI · GitHub</p>
    </div>
    """, unsafe_allow_html=True)
    st.warning("AI-generated content may contain errors. Review important information before using or submitting it.")
