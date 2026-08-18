import chromadb
from chromadb.utils import embedding_functions

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="pdf_docs",
    embedding_function=embedding_function
)

def store_chunks(chunks):

    try:
        collection.delete(
            ids=[
                str(i)
                for i in range(collection.count())
            ]
        )
    except:
        pass

    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        ids=ids
    )

def search_chunks(query, n_results=5):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results["documents"][0]

def get_chunk_count():

    return collection.count()