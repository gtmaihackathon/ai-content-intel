import streamlit as st
import pandas as pd
import os
from app.ingestion import extract_text_from_url, extract_text_from_pdf
from app.embedding import get_embedding
from app.vector_db import FAISSIndex
from app.classifier import classify_asset
from app.analysis import coverage_matrix, find_gaps

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="AI Content Intelligence Engine", layout="wide")
st.title("AI Content Intelligence Engine")
st.sidebar.title("Navigation")

# -------------------------
# GLOBALS
# -------------------------
faiss_index = None
assets_df = pd.DataFrame(columns=['asset_id','title','source','url','text','word_count','created_at',
                                  'persona','funnel_stage','topic','intent','summary'])

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
tabs = ["Ingest", "Assets", "Coverage & Gaps", "Persona Agent", "Export"]
choice = st.sidebar.radio("Go to", tabs)

# -------------------------
# INGEST TAB
# -------------------------
if choice == "Ingest":
    st.header("Ingest Content Assets")
    file_type = st.radio("Select content type", ["CSV", "PDF", "URL"])
    
    if file_type == "CSV":
        csv_file = st.file_uploader("Upload CSV", type=["csv"])
        if csv_file:
            new_assets = pd.read_csv(csv_file)
            assets_df = pd.concat([assets_df, new_assets], ignore_index=True)
            st.success(f"Loaded {len(new_assets)} assets from CSV")
    
    elif file_type == "PDF":
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
        if pdf_file:
            text, err = extract_text_from_pdf(pdf_file)
            if err:
                st.error(f"Error: {err}")
            else:
                new_asset = {
                    'asset_id': f"pdf_{len(assets_df)+1}",
                    'title': pdf_file.name,
                    'source':'pdf',
                    'url':'',
                    'text': text,
                    'word_count': len(text.split()),
                    'created_at':''
                }
                assets_df = pd.concat([assets_df, pd.DataFrame([new_asset])], ignore_index=True)
                st.success(f"PDF ingested: {pdf_file.name}")
    
    elif file_type == "URL":
        url = st.text_input("Enter URL")
        if st.button("Ingest URL"):
            text, err = extract_text_from_url(url)
            if err:
                st.error(f"Error fetching URL: {err}")
            else:
                new_asset = {
                    'asset_id': f"url_{len(assets_df)+1}",
                    'title': url,
                    'source':'url',
                    'url': url,
                    'text': text,
                    'word_count': len(text.split()),
                    'created_at':''
                }
                assets_df = pd.concat([assets_df, pd.DataFrame([new_asset])], ignore_index=True)
                st.success(f"URL ingested: {url}")

# -------------------------
# ASSETS TAB
# -------------------------
elif choice == "Assets":
    st.header("Classify Assets")
    if assets_df.empty:
        st.info("No assets loaded. Please ingest first.")
    else:
        for idx, row in assets_df.iterrows():
            st.subheader(row['title'])
            if st.button(f"Classify {row['asset_id']}"):
                try:
                    result = classify_asset(row['title'], row['text'])
                    for k,v in result.items():
                        assets_df.at[idx,k] = v
                    st.success("Classification complete")
                    st.json(result)
                except Exception as e:
                    st.error(f"Classification failed: {e}")

# -------------------------
# COVERAGE & GAPS TAB
# -------------------------
elif choice == "Coverage & Gaps":
    st.header("Persona × Funnel Stage Coverage")
    if 'persona' not in assets_df.columns or assets_df.empty:
        st.info("No classified assets yet. Please classify assets first.")
    else:
        pivot = coverage_matrix(assets_df)
        st.dataframe(pivot)
        gaps = find_gaps(pivot)
        st.subheader("Content Gaps")
        st.write(gaps if gaps else "No gaps detected!")

# -------------------------
# PERSONA AGENT TAB
# -------------------------
elif choice == "Persona Agent":
    st.header("Persona Agent (Ask Questions)")
    question = st.text_area("Ask a persona-related question")
    if st.button("Ask"):
        if question.strip() == "":
            st.warning("Please enter a question")
        else:
            # Placeholder: integrate with FAISS + LLM retrieval
            st.write("Querying persona agent...")
            st.info("This is a placeholder response. Integrate your FAISS + LLM RAG here.")

# -------------------------
# EXPORT TAB
# -------------------------
elif choice == "Export":
    st.header("Generate Content Plan / Export")
    if st.button("Generate Content Plan"):
        if assets_df.empty:
            st.warning("No assets to generate plan from")
        else:
            # Placeholder: integrate with LLM to generate content plan
            st.write("Generating content plan...")
            st.info("This is a placeholder. Integrate with your LLM content plan prompt here.")

