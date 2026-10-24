def chat(question, history=None, namespace='default', document_ids=None, document_mode=False, return_details=False):
    if not isinstance(question, str) or not question.strip():
        raise ValueError('Please enter a question.')
    if len(question) > 16000:
        raise ValueError('Please keep the question below 16,000 characters.')
    from app.graph.workflow import graph
    result = graph.invoke({'question': question.strip(), 'history': history or [],
        'namespace': namespace, 'document_ids': document_ids or [], 'document_mode': document_mode},
        config={'recursion_limit': 20})
    return result if return_details else result['answer']


def upload_document(uploaded_file, namespace='default'):
    from app.services.rag_service import RAGService
    return RAGService.upload_pdf(uploaded_file, namespace)
