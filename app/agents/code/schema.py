from pydantic import BaseModel


class CodeResponse(BaseModel):
    answer: str