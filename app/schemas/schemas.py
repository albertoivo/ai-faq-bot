from typing import List

from pydantic import BaseModel


class FAQ(BaseModel):
    question: str
    answer: str


class FAQRequest(BaseModel):
    question: str


class FAQResponse(BaseModel):
    faqs: List[FAQ]
