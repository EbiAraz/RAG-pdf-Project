import faiss


def create_index(vectors):
    if vectors is None or getattr(vectors, 'size', 0) == 0 or len(vectors.shape) != 2:
        raise ValueError(
            'No valid text found in PDF. '
            'Ensure the PDF contains extractable text content.'
        )

    dimension = vectors.shape[1]
    # Embeddings are L2-normalized, so inner product == cosine similarity.
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)
    return index
