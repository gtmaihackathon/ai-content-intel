import trafilatura, pdfplumber, os, tempfile

def extract_text_from_url(url):
    downloaded = trafilatura.fetch_url(url)
    if not downloaded: return None, "fetch failed"
    text = trafilatura.extract(downloaded)
    return text, None

def extract_text_from_pdf(file_path):
    texts = []
    with pdfplumber.open(file_path) as pdf:
        for p in pdf.pages:
            texts.append(p.extract_text() or "")
    return "\n".join(texts), None
