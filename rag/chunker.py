def create_chunks(text, chunk_size=1200, overlap=200):
    """Bounded overlapping chunks, preferring paragraph/sentence boundaries."""
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError('Require chunk_size > 0 and 0 <= overlap < chunk_size.')
    chunks, start = [], 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            for separator in ('\n\n', '. ', '\n', ' '):
                boundary = text.rfind(separator, start + chunk_size // 2, end)
                if boundary != -1:
                    end = boundary + len(separator)
                    break
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(start + 1, end - overlap)
    return chunks
