import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from app.main import chat, upload_document
from app.services.memory_service import MemoryService
from app.services.planner_service import PlannerService
from rag.chunker import create_chunks
from rag.vector_store import search_chunks, store_chunks


class FakeCollection:
    def __init__(self):
        self.items = {}

    def upsert(self, ids, documents, metadatas):
        self.items.update({i: (d, m) for i, d, m in zip(ids, documents, metadatas)})

    def get(self, where, include):
        filters = where.get('$and', [where])
        def matches(metadata):
            return all(all(metadata[k] in v['$in'] if isinstance(v, dict) else metadata[k] == v
                           for k, v in clause.items()) for clause in filters)
        rows = [(i, d, m) for i, (d, m) in self.items.items() if matches(m)]
        return {'ids': [r[0] for r in rows], 'documents': [r[1] for r in rows], 'metadatas': [r[2] for r in rows]}

    def query(self, query_texts, n_results, where, include):
        data = self.get(where, [])
        return {'ids': [data['ids'][:n_results]], 'distances': [[.3] * min(n_results, len(data['ids']))]}


class RegressionTests(unittest.TestCase):
    def test_chunker_bounds_and_overlap(self):
        with self.assertRaises(ValueError):
            create_chunks('text', 5, 5)
        chunks = create_chunks('a' * 2500)
        self.assertEqual(len(chunks), 3)
        self.assertTrue(all(len(chunk) <= 1200 for chunk in chunks))
        self.assertEqual(create_chunks(''), [])

    def test_memory_isolation_and_clear(self):
        a, b = MemoryService(), MemoryService()
        for i in range(30):
            a.add_message('user', str(i))
            a.add_message('assistant', str(i))
        self.assertLessEqual(len(a.get_history()), 20)
        self.assertEqual(b.get_history(), [])
        a.clear()
        self.assertEqual(a.get_history(), [])

    def test_routing_boundaries(self):
        self.assertIsNone(PlannerService.detect_agent('digital latest contest'))
        self.assertEqual(PlannerService.detect_agents('github actions deployment'), ['devops'])
        self.assertIn('security', PlannerService.detect_agents('Explain auth.py and review security'))

    def test_index_idempotence_and_isolation(self):
        collection = FakeCollection()
        with patch('rag.vector_store.get_collection', return_value=collection):
            store_chunks(['authentication login'], 'alice', 'one', 'a.pdf', [{'page': 1}])
            store_chunks(['authentication login'], 'alice', 'one', 'a.pdf', [{'page': 1}])
            store_chunks(['secret other tenant'], 'bob', 'two', 'b.pdf', [{'page': 2}])
            self.assertEqual(len(collection.items), 2)
            hits = search_chunks('authentication', namespace='alice', document_ids=['one'], with_metadata=True)
            self.assertEqual(len(hits), 1)
            self.assertEqual(hits[0]['metadata']['source'], 'a.pdf')
            self.assertEqual(search_chunks('authentication', namespace='charlie'), [])

    def test_upload_metadata(self):
        file = io.BytesIO(b'fake pdf'); file.name = 'guide.pdf'
        with patch('app.services.rag_service.extract_pdf_pages', return_value=[{'page': 3, 'text': 'Architecture evidence'}]), patch('app.services.rag_service.store_chunks') as store, patch('app.services.rag_service.get_chunk_count', return_value=1):
            result = upload_document(file, 'alice')
            self.assertEqual(result['source'], 'guide.pdf')
            self.assertEqual(store.call_args.args[1], 'alice')
            self.assertEqual(store.call_args.args[4], [{'page': 3}])

    def test_multistep_graph_shares_results(self):
        with patch('app.services.repository_service.RepositoryService.get_source_context', return_value='def login(): pass'), patch('app.router.router.AgentRouter.execute', side_effect=['code finding', 'security finding']) as execute, patch('app.services.llm_service.LLMService.chat', return_value='Combined report'):
            result = chat('Explain auth.py and assess security', return_details=True)
            self.assertEqual(result['plan'], ['code', 'security'])
            self.assertEqual(result['answer'], 'Combined report')
            self.assertIn('code finding', execute.call_args_list[1].args[1])

    def test_partial_agent_failure_preserves_success(self):
        with patch('app.services.repository_service.RepositoryService.get_source_context', return_value='source'), patch('app.router.router.AgentRouter.execute', side_effect=['code finding', RuntimeError('Model unavailable')]), patch('app.services.llm_service.LLMService.chat', return_value='Partial report'):
            result = chat('Explain auth.py and assess security', return_details=True)
            self.assertEqual(result['results'][0]['answer'], 'code finding')
            self.assertEqual(result['errors'], ['security'])
            self.assertTrue(result['results'][1]['failed'])

    def test_document_query_rewrite_and_sources(self):
        evidence = [{'text': 'Login uses OAuth.', 'metadata': {'source': 'a.pdf', 'page': 2}, 'score': 1}]
        with patch('app.services.llm_service.LLMService.chat', side_effect=['How does OAuth login work?', 'Login uses OAuth [S1].']), patch('app.services.rag_service.RAGService.retrieve', return_value=evidence) as retrieve:
            result = chat('How does it work?', history=[{'role': 'user', 'content': 'Explain login'}], namespace='alice', document_ids=['one'], document_mode=True, return_details=True)
            self.assertEqual(retrieve.call_args.args[:3], ('How does OAuth login work?', 'alice', ['one']))
            self.assertEqual(result['sources'][0]['citation'], 'S1')

    def test_no_evidence_abstains_without_generation(self):
        with patch('app.services.rag_service.RAGService.retrieve', return_value=[]), patch('app.services.llm_service.LLMService.chat') as llm:
            result = chat('Explain PDF', namespace='alice', document_ids=['one'], document_mode=True)
            self.assertIn('not provide enough', result)
            llm.assert_not_called()

    def test_file_boundary(self):
        from app.tools.file_reader import FileReader
        with tempfile.TemporaryDirectory() as directory:
            reader = FileReader(directory)
            with self.assertRaises(ValueError): reader.read('../outside.py')
            with self.assertRaises(ValueError): reader.read('.env')

    def test_streamlit_reply_survives_rerun_and_clear(self):
        from streamlit.testing.v1 import AppTest
        with patch('app.main.chat', return_value={'answer': 'Hello **there**\n\n```python\nx = 1\n```', 'plan': ['general'], 'sources': []}):
            app = AppTest.from_file('frontend/streamlit_app.py').run()
            self.assertFalse(app.exception)
            app.chat_input[0].set_value('hello').run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.chat_message), 2)
            self.assertIn('Hello **there**', app.session_state['messages'][-1]['content'])
            app.run()
            self.assertEqual(len(app.chat_message), 2)
            app.button[0].click().run()
            self.assertEqual(app.session_state['messages'], [])
            self.assertEqual(app.session_state['memory'].get_history(), [])

    def test_streamlit_failure_visible(self):
        from streamlit.testing.v1 import AppTest
        with patch('app.main.chat', side_effect=RuntimeError('Connection unavailable')):
            app = AppTest.from_file('frontend/streamlit_app.py').run()
            app.chat_input[0].set_value('hello').run()
            self.assertFalse(app.exception)
            self.assertIn('Connection unavailable', app.session_state['messages'][-1]['content'])
            self.assertEqual(app.session_state['memory'].get_history(), [])


if __name__ == '__main__':
    unittest.main()
