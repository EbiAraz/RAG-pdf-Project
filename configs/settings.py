import os
from pathlib import Path


def _load_dotenv(path='.env'):
    env_path = Path(path)
    if not env_path.is_file():
        return
    for raw_line in env_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()
os.environ.setdefault('HF_HUB_DISABLE_SYMLINKS_WARNING', '1')
os.environ.setdefault('HF_HUB_DISABLE_EXPERIMENTAL_WARNING', '1')

EMBED_MODEL = os.getenv('EMBED_MODEL', 'paraphrase-multilingual-MiniLM-L12-v2')
GEN_MODEL = os.getenv('GEN_MODEL', 'google/flan-t5-small')

# Smaller overlapping chunks keep facts intact and fit T5's 512-token limit.
CHUNK_SIZE = 140
CHUNK_OVERLAP = 40

# Retrieve extra candidates, then keep the best after lexical rerank.
CANDIDATE_K = 8
TOP_K = 4

MAX_INPUT_TOKENS = 512
MAX_NEW_TOKENS = 128
NUM_BEAMS = 2
