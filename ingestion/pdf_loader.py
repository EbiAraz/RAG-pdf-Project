from pypdf import PdfReader

def load_pdf(path):

    reader = PdfReader(path)

    text = ""
    for page in reader.pages:
        text += (page.extract_text() or '') + "\n"
    
    return text