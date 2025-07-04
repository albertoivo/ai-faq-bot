from typing import List

from pydantic import BaseModel


class FAQ(BaseModel):
    question: str
    answer: str


class FAQRequest(BaseModel):
    question: str
    enhance_with_llm: bool = True


class FAQResponse(BaseModel):
    faqs: List[FAQ]
