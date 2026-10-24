from typing import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    history: list[dict]
    namespace: str
    document_ids: list[str]
    document_mode: bool
    plan: list[str]
    retrieval_query: str
    context: str
    sources: list[dict]
    results: list[dict]
    errors: list[str]
    step: int
    answer: str
