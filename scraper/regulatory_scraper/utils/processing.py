import fitz
import re 

def clean_hyphenated_words(text):
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
    return text

def extract_text_with_pymupdf(pdf_body):
    doc = fitz.open("pdf", pdf_body)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return clean_hyphenated_words(text)
