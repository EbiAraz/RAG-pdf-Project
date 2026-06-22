def chunk_text(text, chunk_size):
    # Handle empty text
    if not text or not text.strip():
        raise ValueError('PDF contains no extractable text.')
    
    words = text.split()
    
    if not words:
        raise ValueError('PDF contains no extractable text.')

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks