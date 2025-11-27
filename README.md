# AI Content Intelligence Engine

Streamlit-based content intelligence platform:
- Ingest URLs, PDFs, DOCX, or paste text
- Classify content by persona, funnel stage, topic, and intent
- Identify gaps in persona × funnel stage coverage
- Generate quarterly content plan (LLM)
- Persona Agent (Slack / RAG chat)
- FAISS vector search for semantic retrieval

## Run locally

```bash
git clone <repo>
cd ai-content-intel
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
streamlit run app/app.py
