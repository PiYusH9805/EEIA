def create_chunks(text, chunk_size=500, overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += (
            chunk_size - overlap
        )

    return chunks
    st.subheader("First Chunk")

    st.write(chunks[0])

    if len(chunks) > 1:
        st.subheader("Second Chunk")
        st.write(chunks[1])