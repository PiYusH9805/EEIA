import hashlib
from rag.pdf_reader import extract_pdf_pages
from rag.chunker import create_chunks
from rag.vector_store import store_chunks, search_chunks, get_chunk_count


class RAGService:
    @staticmethod
    def upload_pdf(uploaded_file, namespace='default'):
        uploaded_file.seek(0)
        content = uploaded_file.read()
        if len(content) > 25 * 1024 * 1024:
            raise ValueError('PDF size must be at most 25 MB.')
        document_id = hashlib.sha256(content).hexdigest()
        pages = extract_pdf_pages(uploaded_file)
        chunks, metadata = [], []
        for page in pages:
            for chunk in create_chunks(page['text']):
                chunks.append(chunk)
                metadata.append({'page': page['page']})
        source = str(getattr(uploaded_file, 'name', 'document.pdf')).replace('\\', '/').split('/')[-1]
        store_chunks(chunks, namespace, document_id, source, metadata)
        return {'characters': sum(len(page['text']) for page in pages), 'chunks': len(chunks),
                'stored': get_chunk_count(namespace), 'document_id': document_id, 'source': source}

    @staticmethod
    def retrieve(query, namespace='default', document_ids=None, with_metadata=False):
        return search_chunks(query, namespace=namespace, document_ids=document_ids, with_metadata=with_metadata)

    @staticmethod
    def context(records, budget=12000):
        parts, used = [], []
        remaining = budget
        for record in records:
            meta = record['metadata']
            label = f"[S{len(used)+1}] {meta['source']}, page {meta.get('page', '?')}"
            text = record['text'][:max(0, remaining - len(label) - 4)]
            if not text:
                break
            parts.append(label + '\n' + text)
            used.append(dict(record, citation=f'S{len(used)+1}'))
            remaining -= len(parts[-1]) + 2
        return '\n\n'.join(parts), used
