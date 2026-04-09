import io
from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    """Extracts text from a PDF file-like object."""
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_txt(file):
    """Extracts text from a TXT file-like object."""
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        return f"Error reading TXT: {str(e)}"

def process_file(uploaded_file):
    """Dispatches processing based on file type."""
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    else:
        return "Unsupported file type."
