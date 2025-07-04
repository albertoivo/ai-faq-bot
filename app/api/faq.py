from fastapi import APIRouter, Depends, HTTPException, status
from openai import OpenAI
from pydantic import BaseModel

from app.schemas.schemas import FAQ, FAQRequest, FAQResponse
from app.services.embedding_service import EmbeddingService

router = APIRouter(prefix="/api/v1/faq", tags=["FAQ"])


client = OpenAI()


# Dependency to get a singleton instance of the service
def get_embedding_service():
    return EmbeddingService()


@router.post(
    "/search",
    response_model=FAQResponse,
    summary="Search for a FAQ using semantic search",
)
def search_faq(
    request: FAQRequest, service: EmbeddingService = Depends(get_embedding_service)
):
    """
    Performs semantic search to find the most relevant FAQ for a given question.
    
    The FAQ data is loaded from the provided URL and the system automatically
    detects the language of the query and performs semantic search.
    """
    match = service.find_best_match(
        query=request.question,
        faq_url=request.faq_url,  # NOVO: URL do FAQ
        enhance_with_llm=request.enhance_with_llm
    )

    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No relevant FAQ found for your question. Please try rephrasing it.",
        )

    question, answer = match
    faq_item = FAQ(question=question, answer=answer)
    return FAQResponse(faqs=[faq_item])


@router.post(
    "/regenerate-embeddings",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regenerate FAQ embeddings",
)
def regenerate_embeddings(service: EmbeddingService = Depends(get_embedding_service)):
    """
    Clears the embedding cache to force regeneration on next search.
    """
    import os
    cache_files = list(service.data_path.glob("faq_*_embeddings.pkl"))
    
    for cache_file in cache_files:
        try:
            cache_file.unlink()
            print(f"Deleted cache file: {cache_file}")
        except Exception as e:
            print(f"Error deleting cache file {cache_file}: {e}")
    
    return {"message": f"Cleared {len(cache_files)} embedding cache files."}
