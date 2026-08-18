from pydantic import BaseModel


class DocumentationResponse(BaseModel):
    answer: str