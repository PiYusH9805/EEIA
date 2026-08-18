from app.services.rag_service import RAGService
from app.services.llm_service import LLMService

from app.agents.documentation.prompt import (
    DOCUMENTATION_SYSTEM_PROMPT
)


class DocumentationAgent:

    def upload_document(self, uploaded_file):
        return RAGService.upload_pdf(uploaded_file)

    def ask(self, question: str):

        chunks = RAGService.retrieve(question)

        context = "\n\n".join(chunks)

        messages = [
            {
                "role": "system",
                "content": DOCUMENTATION_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Context:

{context}

Question:

{question}
"""
            }
        ]

        answer = LLMService.chat(
            messages=messages
        )

        return answer