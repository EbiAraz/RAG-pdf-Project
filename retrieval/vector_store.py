import faiss
import numpy as np

def create_index(vectors):
    # Handle empty vectors
    if vectors.size == 0 or len(vectors.shape) == 1:
        raise ValueError(
            'No valid text found in PDF. '
            'Ensure the PDF contains extractable text content.'
        )
    
    dimension = vectors.shape[1]
    
    index = faiss.IndexFlatL2(dimension)

    index.add(vectors)

    return index