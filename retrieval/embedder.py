import numpy as np
from sentence_transformers import SentenceTransformer

from configs.settings import EMBED_MODEL

_model = None


def _get_model():
    global _model
    if _model is None:
        print(f'Loading embedding model: {EMBED_MODEL}...')
        try:
            _model = SentenceTransformer(EMBED_MODEL, local_files_only=True)
        except Exception:
            _model = SentenceTransformer(EMBED_MODEL)
    return _model


def embed(texts):
    if not texts:
        raise ValueError('No text available to embed.')

    model = _get_model()
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
        batch_size=32,
        convert_to_numpy=True,
    )
    return np.ascontiguousarray(vectors, dtype='float32')
