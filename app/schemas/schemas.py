from pydantic import BaseModel
from typing import List

class FAQ(BaseModel):
    question: str
    answer: str

class FAQRequest(BaseModel):
    question: str

class FAQResponse(BaseModel):
    faqs: List[FAQ]
