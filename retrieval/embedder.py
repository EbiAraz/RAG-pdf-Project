from sentence_transformers import SentenceTransformer
from configs.settings import EMBED_MODEL
import numpy as np

_model = None

def _get_model():
    global _model
    if _model is None:
        print(f'Loading embedding model: {EMBED_MODEL}...')
        _model = SentenceTransformer(EMBED_MODEL)
    return _model

def embed(texts):
    
    model = _get_model()
    vectors = model.encode(texts)

    return np.array(vectors).astype('float32')