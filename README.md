# GenAI Content Transformation Platform

A CDS208 prototype that transforms uploaded or pasted content into summaries, study notes, reports, Q&A sets, simplified text and MCQ quizzes using a locally hosted Ollama model.

## Features
- PDF, DOCX and TXT text extraction
- Ollama-powered generation
- Prompt templates and adjustable tone/detail
- Automated multi-output workflow
- SQLite transformation history
- Usage analytics and CSV export for Power BI
- Streamlit interface

## Requirements
- Python 3.10+
- Ollama installed and running
- A model pulled locally (default: `llama3.2`)

## Setup (Windows PowerShell)
```powershell
git clone https://github.com/YOUR-USERNAME/genai-content-transformation.git
cd genai-content-transformation
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
ollama pull llama3.2
ollama serve
```
Open a second terminal in the project folder and run:
```powershell
streamlit run app.py
```
If Ollama is already running as a background service, do not start a second `ollama serve` process.

## Team workflow
Create one feature branch per member. Commit only your own work, push the branch and open a pull request. The team leader reviews and merges pull requests into `main`.

## Power BI
Open `Analytics` in the app and download `genai_analytics.csv`. In Power BI Desktop select **Get data → Text/CSV**, load the file and create visuals for task counts, source word counts and activity by date.

## Limitations
The prototype sends document text to the local Ollama service. It does not verify factual accuracy. Review all generated content before relying on it. Text extraction from scanned/image-only PDFs requires OCR, which is not included in this starter version.
