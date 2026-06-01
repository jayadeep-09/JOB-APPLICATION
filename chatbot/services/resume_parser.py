import io
import pdfplumber
import docx

def extract_text_from_pdf(file_obj):
    text = ""
    try:
        with pdfplumber.open(file_obj) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error parsing PDF: {e}")
    return text

def extract_text_from_docx(file_obj):
    text = ""
    try:
        doc = docx.Document(file_obj)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
    return text

def parse_resume(file_obj, filename):
    text = ""
    if filename.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_obj)
    elif filename.lower().endswith('.docx'):
        text = extract_text_from_docx(file_obj)
    
    # Basic cleaning
    text = " ".join(text.split())
    return text
