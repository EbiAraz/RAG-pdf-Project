import re

from pypdf import PdfReader


def _clean_text(text):
    text = text.replace('\x00', ' ')
    text = re.sub(r'-\s*\n\s*', '', text)
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def load_pdf(path):
    reader = PdfReader(path)

    if getattr(reader, 'is_encrypted', False):
        try:
            reader.decrypt('')
        except Exception as exc:
            raise ValueError('PDF is encrypted and cannot be read.') from exc

    pages = []
    for page in reader.pages:
        page_text = page.extract_text() or ''
        cleaned = _clean_text(page_text)
        if cleaned:
            pages.append(cleaned)

    text = '\n\n'.join(pages)
    if not text.strip():
        raise ValueError(
            'No extractable text found in the PDF. '
            'Scanned image-only PDFs are not supported without OCR.'
        )

    return text
