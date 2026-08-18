import re

from configs.settings import TOP_K
from generation.llm import generate
from generation.prompt_builder import snippet
from retrieval.embedder import embed
from retrieval.retriever import retrieve

_STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'of', 'to', 'in', 'on', 'for', 'with',
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'do', 'does', 'did',
    'who', 'what', 'where', 'when', 'why', 'how', 'which', 'whom',
    'this', 'that', 'these', 'those', 'it', 'its', 'as', 'at', 'by', 'from',
}


def _tokens(text):
    return set(re.findall(r'\w+', str(text).lower()))


def _content_tokens(text):
    return {token for token in _tokens(text) if token not in _STOPWORDS and len(token) > 1}


def _rerank(question, ids, scores, chunks):
    question_tokens = _content_tokens(question)
    ranked = []
    for idx, score in zip(ids, scores):
        if idx < 0 or idx >= len(chunks):
            continue
        overlap = len(question_tokens & _content_tokens(chunks[idx])) / max(1, len(question_tokens))
        ranked.append((0.7 * score + 0.3 * overlap, idx))
    ranked.sort(reverse=True, key=lambda item: item[0])
    return [idx for _, idx in ranked[:TOP_K]]


def _sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', ' '.join(str(text).split()))
    return [part.strip() for part in parts if part.strip()]


def extractive_answer(question, context):
    sentences = _sentences(context)
    if not sentences:
        return snippet(context, limit=400)

    question_tokens = _content_tokens(question)
    best_sentence = sentences[0]
    best_score = -1.0
    for sentence in sentences:
        overlap = len(question_tokens & _content_tokens(sentence))
        score = overlap / max(1, len(question_tokens))
        if score > best_score:
            best_score = score
            best_sentence = sentence
    return best_sentence


def _is_weak_answer(answer, question, context):
    cleaned = (answer or '').strip()
    if len(cleaned) < 2:
        return True
    if cleaned.lower() == question.strip().lower():
        return True

    lowered = cleaned.lower()
    unknown = any(marker in lowered for marker in ('i do not know', "i don't know", 'not in the context'))
    if unknown:
        return True

    answer_tokens = _content_tokens(cleaned)
    context_tokens = _tokens(context)
    if not answer_tokens:
        return True
    grounded = len(answer_tokens & context_tokens) / len(answer_tokens)
    return grounded < 0.25


def rag_answer(question, index, chunks):
    question = (question or '').strip()
    if not question:
        return 'Please enter a question.', ''

    query_vector = embed([question])
    ids, scores = retrieve(index, query_vector)
    selected = _rerank(question, ids, scores, chunks)

    if not selected:
        return 'No relevant text was found in the loaded PDF.', ''

    context_parts = []
    source_lines = []
    for rank, chunk_id in enumerate(selected, start=1):
        chunk = chunks[chunk_id]
        context_parts.append(chunk)
        source_lines.append(f'[{rank}] {snippet(chunk)}')

    context = '\n\n'.join(context_parts)
    answer = generate(question, context)
    top_score = scores[0] if scores else 0.0
    if _is_weak_answer(answer, question, context):
        if top_score >= 0.12:
            answer = extractive_answer(question, context)
        else:
            answer = 'I do not know based on the loaded PDF.'

    return answer, '\n\n'.join(source_lines)
