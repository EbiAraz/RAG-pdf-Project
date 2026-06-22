from ingestion.pdf_loader import load_pdf
from ingestion.chunker import chunk_text
from retrieval.embedder import embed
from retrieval.vector_store import create_index
from configs.settings import CHUNK_SIZE

def build(pdf_path):

    text = load_pdf(pdf_path)

    chunks = chunk_text(text,CHUNK_SIZE)

    vectors = embed(chunks)

    index = create_index(vectors)

    return index , chunks