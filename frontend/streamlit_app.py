import hashlib
import sys
from pathlib import Path
from uuid import uuid4

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.main import chat, upload_document
from app.services.memory_service import MemoryService

st.set_page_config(page_title='EEIA', page_icon='🤖', layout='wide')
st.title('🤖 Enterprise Engineering Intelligence Agent')
st.caption('Ask about your repository or uploaded engineering documents.')

st.session_state.setdefault('messages', [])
st.session_state.setdefault('namespace', uuid4().hex)
st.session_state.setdefault('memory', MemoryService())
st.session_state.setdefault('documents', {})

if st.button('Clear Chat'):
    st.session_state.messages = []
    st.session_state.memory.clear()
    st.rerun()

st.sidebar.header('Engineering documents')
if st.sidebar.button('Delete session documents'):
    try:
        if st.session_state.documents:
            from rag.vector_store import delete_documents
            delete_documents(st.session_state.namespace)
        st.session_state.documents = {}
        st.session_state.namespace = uuid4().hex
        st.session_state.messages = []
        st.session_state.memory.clear()
        st.session_state['upload_version'] = st.session_state.get('upload_version', 0) + 1
        st.rerun()
    except Exception as exc:
        st.sidebar.error(f'Could not delete documents: {exc}')
uploaded_files = st.sidebar.file_uploader('Upload PDFs', type=['pdf'], accept_multiple_files=True, key=f"pdf_upload_{st.session_state.get('upload_version', 0)}")
for uploaded_file in uploaded_files or []:
    digest = hashlib.sha256(uploaded_file.getvalue()).hexdigest()
    if digest not in st.session_state.documents:
        try:
            with st.spinner(f'Indexing {uploaded_file.name}...'):
                stats = upload_document(uploaded_file, st.session_state.namespace)
            st.session_state.documents[digest] = stats
        except Exception as exc:
            st.sidebar.error(f'Could not index {uploaded_file.name}: {exc}')

active_ids = [hashlib.sha256(file.getvalue()).hexdigest() for file in uploaded_files or []
              if hashlib.sha256(file.getvalue()).hexdigest() in st.session_state.documents]
if active_ids:
    st.sidebar.success(f'{len(active_ids)} document(s) ready')
    for identifier in active_ids:
        stats = st.session_state.documents[identifier]
        st.sidebar.caption(f"{stats['source']}: {stats['chunks']} chunks")
mode = st.sidebar.radio('Answer using', ['Uploaded documents', 'Repository / general'],
                        index=0 if active_ids else 1)

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        if message.get('sources'):
            with st.expander('Retrieved evidence'):
                for source in message['sources']:
                    meta = source['metadata']
                    st.caption(f"[{source['citation']}] {meta['source']} · page {meta.get('page', '?')}")
                    st.text(source['text'])
        if message.get('plan'):
            st.caption('Agents: ' + ' → '.join(message['plan']))

if prompt := st.chat_input('Ask anything...'):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    result = {}
    with st.chat_message('assistant'):
        try:
            if mode == 'Uploaded documents' and not active_ids:
                raise ValueError('Upload a PDF first, or select Repository / general.')
            with st.spinner('Analyzing your question...'):
                result = chat(prompt, history=st.session_state.memory.get_history(),
                              namespace=st.session_state.namespace, document_ids=active_ids,
                              document_mode=mode == 'Uploaded documents', return_details=True)
            answer = result['answer']
            st.session_state.memory.add_message('user', prompt)
            st.session_state.memory.add_message('assistant', answer)
        except Exception as exc:
            answer = f'Unable to answer: {exc}'
        st.markdown(answer)
        if result.get('sources'):
            with st.expander('Retrieved evidence'):
                for source in result['sources']:
                    meta = source['metadata']
                    st.caption(f"[{source['citation']}] {meta['source']} · page {meta.get('page', '?')}")
                    st.text(source['text'])
        if result.get('errors'):
            st.warning('Partial result: these agents failed: ' + ', '.join(result['errors']))
        if result.get('plan'):
            st.caption('Agents: ' + ' → '.join(result['plan']))
    st.session_state.messages.append({'role': 'assistant', 'content': answer,
        'sources': result.get('sources', []), 'plan': result.get('plan', [])})

if st.session_state.messages:
    transcript = '\n\n'.join(f"## {message['role'].title()}\n\n{message['content']}" for message in st.session_state.messages)
    st.download_button('Download conversation / report', transcript, file_name='eeia-report.md', mime='text/markdown')
