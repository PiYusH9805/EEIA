# EEIA implementation and verification

## Run

From the repository root in PowerShell:

```powershell
.\myenv\Scripts\python.exe -m streamlit run app.py
```

The existing `frontend/streamlit_app.py` entry point also works. The root `app.py` now opens the same UI instead of blocking on terminal input.

Install requirements in a fresh environment if needed. The existing `myenv` contains the tested dependencies. Requirements now include the formerly missing OpenAI SDK and sentence-transformers.

Configure `.env` with AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT. An endpoint ending in `/openai/v1/` uses the OpenAI-compatible client; a resource endpoint uses AzureOpenAI and AZURE_OPENAI_API_VERSION (default 2024-10-21). Client initialization is lazy, with 60-second request timeout and one retry. Set EEIA_SEND_TEMPERATURE=true only for a deployment supporting temperature.

## Preserved architecture

Streamlit -> app/main.py -> LangGraph planner -> retrieval -> specialized agent loop -> report -> Streamlit.

Existing agent, service, graph and rag directories remain in place. The planner validates agent names, supports up to five ordered agents and falls back to general conversation if the planner JSON is malformed. Retrieved evidence and earlier findings are shared through graph state. Multi-agent answers are synthesized into an engineering report; single-agent answers are returned directly. Research uses internal evidence and model knowledge, with no claim of live web research.

## Implemented RAG and memory

- Page-aware extraction and paragraph/sentence-aware overlapping chunking.
- Lazy all-MiniLM-L6-v2 embeddings; persistent Chroma collection `eeia_documents_v2`.
- Content-hash document IDs and idempotent upserts, with multiple documents and session namespace filters.
- Semantic candidate search + BM25 lexical retrieval, reciprocal rank fusion, a cosine-distance relevance gate and duplicate suppression.
- Conversation-based standalone query rewriting; original-query retry when a rewrite retrieves no evidence.
- Bounded context construction and source/page metadata, source labels and visible retrieved excerpts.
- Insufficient-evidence response without model generation when no chunks survive retrieval.
- Session-owned bounded memory (20 messages / 16,000 characters); clear chat clears model memory too.
- Markdown report/conversation download and explicit session-document deletion.
- Project source snippets with line numbers; excluded environments and secret-file/path containment checks.

Select **Uploaded documents** for PDF-only questions, even when they mention security or architecture. Select **Repository / general** for code analysis; selected documents can supplement that analysis. Removing a PDF from the uploader removes it from active retrieval. Delete session documents removes that session's indexed documents and conversation.

Existing `pdf_docs` data is untouched. Re-upload PDFs into the new metadata-aware collection. A browser session owns its namespace; there is no authenticated account or cross-session restore. Conversation memory is temporary. Persisted document records can outlive a closed tab; use Delete session documents before closing if they should be removed.

## Verification

```powershell
.\myenv\Scripts\python.exe -m unittest discover -s tests -p test_regressions.py -v
```

Regression coverage: rendering successful and failed chat replies, rerun persistence, clear-chat memory reset, routing boundaries, multi-agent shared state/report generation, conversational query rewriting, source metadata, no-evidence abstention, duplicate-safe indexing, session isolation, chunk boundaries and file-access containment.

A real local ingestion smoke check extracted 39,657 characters from the supplied 21-page architecture guide and indexed 49 chunks in an isolated temporary database. A live Azure greeting and an end-to-end PDF answer with five source references completed successfully. All 12 offline regression tests passed. These checks do not imply all possible questions or all model-generated findings are correct.

## Limits and next evaluation work

Retrieval relevance uses heuristics; no calibrated answer-accuracy claim is made. Lexical rank fusion is not a trained cross-encoder reranker. This implementation does not include OCR, external web search, persistent user profiles, GraphRAG, fine-tuning, autonomous code execution, patch application or deployment. Tests suggested by agents are suggestions until actually executed. Large-corpus BM25 currently reads the selected document corpus in memory; an indexed lexical backend is appropriate before scaling beyond local project use. PDFs are capped at 25 MB; context uses character budgets rather than exact model-token counting. Source evidence selection is bounded and may omit deeper dependencies.

Additional techniques should be added against a concrete evaluation set and provider configuration, rather than labelled as all advanced RAG being complete.

API references checked during implementation: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_conditional_edges and https://docs.trychroma.com/reference/python

## Community Cloud dependency troubleshooting

Use repository PiYusH9805/EEIA, branch main, entry point app.py, and select Python 3.13 in Advanced settings to match the locally tested interpreter. Paste Azure credentials as root-level TOML secrets; never commit .env.

The October 24 deployment log used Python 3.14.9. The former full-environment requirements pinned grpcio-status==1.71.2 while google-api-core[grpc]==2.31.0 required grpcio-status>=1.75.1 on Python 3.14. The application uses Azure OpenAI, not the unused Google/Gemini packages that introduced that conflict. requirements.txt now declares only the eight direct application dependencies and lets the resolver choose compatible transitive dependencies.

Changing requirements triggers dependency installation in Community Cloud. Python-version changes require deleting and redeploying the Cloud app; save its secrets/settings privately first. This does not require deleting the GitHub repository. A passing local test suite does not confirm that a fresh Linux cloud build has completed.
