def chunk_text(text, chunk_size, overlap=0):
    if not text or not str(text).strip():
        raise ValueError('PDF contains no extractable text.')

    words = str(text).split()
    if not words:
        raise ValueError('PDF contains no extractable text.')

    if chunk_size <= 0:
        raise ValueError('chunk_size must be greater than 0.')

    overlap = max(0, min(int(overlap), chunk_size - 1))
    step = chunk_size - overlap
    chunks = []

    for start in range(0, len(words), step):
        piece = words[start:start + chunk_size]
        if not piece:
            break
        chunks.append(' '.join(piece))
        if start + chunk_size >= len(words):
            break

    if len(chunks) >= 2 and len(chunks[-1].split()) < max(20, overlap // 2):
        chunks[-2] = chunks[-2] + ' ' + chunks[-1]
        chunks.pop()

    return chunks
