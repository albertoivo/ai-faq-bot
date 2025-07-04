from typing import List

from pydantic import BaseModel


class FAQ(BaseModel):
    question: str
    answer: str


class FAQRequest(BaseModel):
    question: str
    faq_url: str  # NOVA: URL do FAQ JSON do cliente
    enhance_with_llm: bool = True


class FAQResponse(BaseModel):
    faqs: List[FAQ]
