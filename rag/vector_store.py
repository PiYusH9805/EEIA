"""Persistent, namespace-filtered semantic + BM25 retrieval with rank fusion."""
import hashlib
import math
import os
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def get_collection():
    import chromadb
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
    embedding = SentenceTransformerEmbeddingFunction(model_name=os.getenv('EEIA_EMBEDDING_MODEL', 'all-MiniLM-L6-v2'))
    client = chromadb.PersistentClient(path=os.getenv('EEIA_CHROMA_PATH', str(Path(__file__).resolve().parents[1] / 'chroma_db')))
    return client.get_or_create_collection(name='eeia_documents_v2', embedding_function=embedding,
        metadata={'hnsw:space': 'cosine'})


def scope(namespace, document_ids=None):
    filters = [{'namespace': namespace}]
    if document_ids:
        filters.append({'document_id': {'$in': list(document_ids)}})
    return filters[0] if len(filters) == 1 else {'$and': filters}


def store_chunks(chunks, namespace='default', document_id=None, source='document.pdf', metadatas=None):
    if not chunks:
        raise ValueError('No text chunks to store.')
    document_id = document_id or hashlib.sha256(''.join(chunks).encode()).hexdigest()
    metadata = [dict((metadatas or [{}] * len(chunks))[i], namespace=namespace,
                     document_id=document_id, source=source, chunk=i) for i in range(len(chunks))]
    ids = [hashlib.sha256(f'{namespace}:{document_id}:{i}'.encode()).hexdigest() for i in range(len(chunks))]
    collection = get_collection()
    for start in range(0, len(chunks), 128):
        collection.upsert(ids=ids[start:start+128], documents=chunks[start:start+128], metadatas=metadata[start:start+128])
    return document_id


def get_chunk_count(namespace='default', document_ids=None):
    return len(get_collection().get(where=scope(namespace, document_ids), include=[])['ids'])


def delete_documents(namespace):
    get_collection().delete(where={'namespace': namespace})


def tokens(text):
    return re.findall(r'\w+', text.lower())


def bm25_scores(query, documents):
    terms = [Counter(tokens(doc)) for doc in documents]
    lengths = [sum(doc.values()) for doc in terms]
    average = sum(lengths) / max(len(lengths), 1) or 1
    scores = [0.0] * len(documents)
    stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'of', 'in', 'on', 'to', 'for', 'and', 'or', 'what', 'how', 'does', 'do', 'it', 'this', 'that', 'with', 'please'}
    for word in set(tokens(query)) - stopwords:
        frequency = sum(word in doc for doc in terms)
        inverse = math.log(1 + (len(terms) - frequency + .5) / (frequency + .5))
        for i, doc in enumerate(terms):
            tf = doc[word]
            scores[i] += inverse * tf * 2.5 / (tf + 1.5 * (.25 + .75 * lengths[i] / average))
    return scores


def search_chunks(query, n_results=5, namespace='default', document_ids=None, with_metadata=False):
    if not query.strip() or n_results < 1:
        return []
    collection = get_collection()
    where = scope(namespace, document_ids)
    corpus = collection.get(where=where, include=['documents', 'metadatas'])
    if not corpus['ids']:
        return []
    documents = corpus['documents']
    lexical = bm25_scores(query, documents)
    semantic = collection.query(query_texts=[query], n_results=min(max(n_results * 4, 20), len(documents)),
                                where=where, include=['distances'])
    index = {identifier: i for i, identifier in enumerate(corpus['ids'])}
    scores, distances = {}, {}
    for rank, (identifier, distance) in enumerate(zip(semantic['ids'][0], semantic['distances'][0])):
        i = index[identifier]
        distances[i] = distance
        # Cosine distance gate rejects clearly unrelated semantic matches.
        if distance <= float(os.getenv('EEIA_MAX_DISTANCE', '0.85')):
            scores[i] = scores.get(i, 0) + 1 / (60 + rank + 1)
    for rank, i in enumerate(sorted(range(len(documents)), key=lambda i: lexical[i], reverse=True)):
        if lexical[i] > 0:
            scores[i] = scores.get(i, 0) + 1 / (60 + rank + 1)
    selected, seen = [], []
    for i in sorted(scores, key=scores.get, reverse=True):
        words = set(tokens(documents[i]))
        if any(len(words & old) / max(len(words | old), 1) > .85 for old in seen):
            continue
        seen.append(words)
        selected.append({'text': documents[i], 'metadata': corpus['metadatas'][i],
                         'score': scores[i], 'distance': distances.get(i), 'id': corpus['ids'][i]})
        if len(selected) >= n_results:
            break
    return selected if with_metadata else [item['text'] for item in selected]
