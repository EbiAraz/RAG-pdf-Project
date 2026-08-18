from configs.settings import CHUNK_OVERLAP, CHUNK_SIZE
from ingestion.chunker import chunk_text
from ingestion.pdf_loader import load_pdf
from retrieval.embedder import embed
from retrieval.vector_store import create_index


def build(pdf_path):
    text = load_pdf(pdf_path)
    chunks = chunk_text(text, CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    vectors = embed(chunks)
    index = create_index(vectors)
    return index, chunks
