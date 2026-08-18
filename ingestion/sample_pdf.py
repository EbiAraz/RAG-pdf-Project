"""Create a small sample PDF with known facts for default testing."""

from pathlib import Path


SAMPLE_LINES = [
    'Northwind Analytics Company Profile',
    '',
    'Northwind Analytics is a software company founded in 2018.',
    'The company headquarters is in Berlin, Germany.',
    'The chief executive officer is Maria Chen.',
    'The company has 120 employees.',
    '',
    'Main Product',
    'The flagship product is Atlas Query Engine, a tool for searching',
    'private document collections. Atlas Query Engine was released in 2021.',
    'Customers use it to ask questions about PDF files and internal reports.',
    '',
    'How Atlas Works',
    'Atlas splits documents into overlapping text chunks, converts those',
    'chunks into embeddings, and stores them in a vector index. When a user',
    'asks a question, Atlas retrieves the most relevant chunks and a language',
    'model writes an answer using only that retrieved context.',
    '',
    'Support Policy',
    'Customer support is available Monday to Friday from 09:00 to 18:00',
    'Central European Time. The support email is support@northwind.example.',
    'The annual subscription price for Atlas Query Engine is 2400 euros.',
]


def _escape_pdf_text(text):
    return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


def create_sample_pdf(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    commands = ['BT', '/F1 12 Tf', '72 740 Td']
    for index, line in enumerate(SAMPLE_LINES):
        safe = _escape_pdf_text(line)
        if index == 0:
            commands.append(f'({safe}) Tj')
        else:
            commands.append(f'0 -18 Td ({safe}) Tj')
    commands.append('ET')
    stream = '\n'.join(commands).encode('latin-1', errors='replace')

    objects = [
        b'1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n',
        b'2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n',
        (
            b'3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] '
            b'/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n'
        ),
        (
            f'4 0 obj << /Length {len(stream)} >> stream\n'.encode('ascii')
            + stream
            + b'\nendstream\nendobj\n'
        ),
        b'5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n',
    ]

    header = b'%PDF-1.4\n'
    body = b''
    offsets = []
    for obj in objects:
        offsets.append(len(header) + len(body))
        body += obj

    xref_pos = len(header) + len(body)
    xref = [b'xref\n', f'0 {len(objects) + 1}\n'.encode('ascii'), b'0000000000 65535 f \n']
    for offset in offsets:
        xref.append(f'{offset:010d} 00000 n \n'.encode('ascii'))

    trailer = (
        f'trailer << /Size {len(objects) + 1} /Root 1 0 R >>\n'
        f'startxref\n{xref_pos}\n%%EOF\n'
    ).encode('ascii')

    path.write_bytes(header + body + b''.join(xref) + trailer)
    return str(path)
