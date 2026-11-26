import streamlit as st
from modules.ai_engine import transform_text, check_ollama
from modules.quiz_generator import generate_quiz
from modules.workflows import run_full_workflow
from modules.exporter import make_download
from modules.database import init_db, save_record, get_history
from modules.analytics import get_analytics
from modules.text_extract import extract_text
from pathlib import Path

st.set_page_config(page_title="GenAI Content Studio", page_icon="✨", layout="wide")
init_db()

def load_css():
    css_path = Path("assets/styles.css")
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
load_css()

st.sidebar.title("✨ GenAI Studio")
page = st.sidebar.radio("Navigate", ["Home", "Transform Content", "AI Workflow", "History", "Analytics", "About"])
st.sidebar.caption("CDS208 • Emerging Tools and Applications")
model = st.sidebar.text_input("Ollama model", value="llama3.2")
if st.sidebar.button("Check AI connection"):
    ok, msg = check_ollama(model)
    (st.sidebar.success if ok else st.sidebar.error)(msg)

def source_panel():
    uploaded = st.file_uploader("Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    pasted = st.text_area("Or paste your content here", height=180, placeholder="Paste text to transform...")
    source = ""
    filename = "Pasted text"
    if uploaded:
        try:
            source = extract_text(uploaded)
            filename = uploaded.name
            st.success(f"Extracted text from {filename} ({len(source.split())} words)")
        except Exception as exc:
            st.error(f"Could not read file: {exc}")
    elif pasted.strip():
        source = pasted.strip()
    return source, filename

if page == "Home":
    st.title("GenAI Content Transformation Platform")
    st.write("Transform documents into summaries, study notes, quizzes, reports and question-answer sets using Generative AI.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Transformation types", "6")
    c2.metric("AI engine", "Ollama")
    c3.metric("Storage", "SQLite")
    st.subheader("What can you create?")
    cols = st.columns(3)
    for col, title, desc in zip(cols * 2, ["Smart summaries", "Study notes", "MCQ quizzes", "Reports", "Q&A sets", "Automated workflow"],
                                ["Condense long documents", "Organize key concepts", "Practice with answers", "Create structured reports", "Generate revision questions", "Run several tasks together"]):
        with col:
            st.markdown(f"### {title}")
            st.write(desc)
    st.info("Start by opening **Transform Content** and uploading a PDF, DOCX or TXT file.")

elif page == "Transform Content":
    st.title("Transform your content")
    source, filename = source_panel()
    kind = st.selectbox("Choose output", ["Summary", "Study Notes", "Report", "Question & Answer", "Simplify Text", "Key Points"])
    length = st.select_slider("Output detail", options=["Short", "Medium", "Detailed"], value="Medium")
    tone = st.selectbox("Writing style", ["Clear and simple", "Academic", "Professional", "Student-friendly"])
    if st.button("✨ Generate content", type="primary", disabled=not bool(source.strip())):
        with st.spinner("Generating with Ollama..."):
            try:
                result = transform_text(source, kind, length, tone, model)
                st.session_state["last_result"] = result
                st.session_state["last_filename"] = filename
                save_record(filename, kind, len(source.split()), result, model)
            except Exception as exc:
                st.error(str(exc))
    if st.session_state.get("last_result"):
        st.subheader("Generated output")
        st.markdown(st.session_state["last_result"])
        st.download_button("Download as TXT", make_download(st.session_state["last_result"], "txt"),
                           file_name="genai_output.txt", mime="text/plain")
        st.download_button("Download as Markdown", make_download(st.session_state["last_result"], "md"),
                           file_name="genai_output.md", mime="text/markdown")

elif page == "AI Workflow":
    st.title("Automated content workflow")
    st.write("One input → multiple AI-generated learning resources.")
    source, filename = source_panel()
    if st.button("Run complete workflow", type="primary", disabled=not bool(source.strip())):
        outputs = {}
        progress = st.progress(0)
        tasks = ["Summary", "Study Notes", "Question & Answer", "Quiz"]
        for i, task in enumerate(tasks):
            with st.spinner(f"Creating {task}..."):
                if task == "Quiz":
                    outputs[task] = generate_quiz(source, 5, model)
                else:
                    outputs[task] = transform_text(source, task, "Medium", "Student-friendly", model)
            progress.progress((i + 1) / len(tasks))
            save_record(filename, f"Workflow: {task}", len(source.split()), str(outputs[task]), model)
        st.session_state["workflow_outputs"] = outputs
        st.success("Workflow completed.")
    for name, output in st.session_state.get("workflow_outputs", {}).items():
        with st.expander(name, expanded=True):
            st.markdown(output if isinstance(output, str) else str(output))
            st.download_button(f"Download {name}", make_download(str(output), "txt"),
                               file_name=f"{name.lower().replace(' ', '_')}.txt", key=f"dl_{name}")

elif page == "History":
    st.title("Transformation history")
    records = get_history()
    if not records:
        st.info("No transformations saved yet.")
    else:
        for record in records:
            with st.expander(f"{record['created_at']} • {record['source_name']} • {record['task']}"):
                st.write(f"Words in source: {record['word_count']} | Model: {record['model']}")
                st.markdown(record["output"])
                st.download_button("Download result", make_download(record["output"], "txt"),
                                   file_name="history_result.txt", key=f"hist_{record['id']}")

elif page == "Analytics":
    st.title("Usage analytics")
    data = get_analytics()
    a, b, c = st.columns(3)
    a.metric("Total generations", data["total"])
    b.metric("Total input words", data["words"])
    c.metric("Most used task", data["top_task"])
    if not data["by_task"].empty:
        st.subheader("Generations by task")
        st.bar_chart(data["by_task"].set_index("task"))
        st.subheader("Recent activity")
        st.dataframe(data["recent"], use_container_width=True)
    st.download_button("Export analytics CSV for Power BI", data["csv"],
                       file_name="genai_analytics.csv", mime="text/csv")

else:
    st.title("About this project")
    st.markdown("""
    **Project:** GenAI Platform for Automated Content Transformation

    **Problem:** Converting lengthy source material into useful learning and communication formats takes time.

    **Solution:** A local Generative AI application that transforms uploaded or pasted content into summaries, notes, quizzes, Q&A and reports.

    **Core technologies:** Python, Streamlit, Ollama, Prompt Engineering, SQLite, Pandas, Power BI and GitHub.

    **Responsible use:** Always review generated content. AI output can contain errors and should not be treated as a verified source.
    """)
