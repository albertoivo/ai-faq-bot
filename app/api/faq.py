from fastapi import APIRouter, Depends, HTTPException, status
from openai import OpenAI
from pydantic import BaseModel

from app.config.logging import setup_logging
from app.schemas.schemas import FAQ, FAQRequest, FAQResponse
from app.services.embedding_service import EmbeddingService

router = APIRouter(prefix="/api/v1/faq", tags=["FAQ"])


client = OpenAI()

logger = setup_logging()


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
    logger.info(f"Received FAQ search request: question='{request.question}' | enhance_with_llm={request.enhance_with_llm}")
    match = service.find_best_match(request.question, enhance_with_llm=request.enhance_with_llm)

    if not match:
        logger.warning(f"No relevant FAQ found for question: '{request.question}'")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No relevant FAQ found for your question. Please try rephrasing it.",
        )

    question, answer = match
    logger.info(f"FAQ match found for question: '{question}'")
    faq_item = FAQ(question=question, answer=answer)
    return FAQResponse(faq=faq_item)


@router.post(
    "/regenerate-embeddings",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regenerate FAQ embeddings",
)
def regenerate_embeddings(service: EmbeddingService = Depends(get_embedding_service)):
    logger.info("Received request to regenerate embeddings for all supported languages.")
    supported_languages = ["en", "pt"]  # Define supported languages here
    for lang in supported_languages:
        try:
            if service.embeddings_path and service.embeddings_path.exists():
                service.embeddings_path.unlink()
            lang_service = EmbeddingService(language=lang)
            lang_service._get_or_generate_embeddings()
            logger.info(f"Successfully regenerated embeddings for language '{lang}'")
        except Exception as e:
            logger.error(f"Could not regenerate embeddings for language '{lang}': {e}")
    return {"message": "Embedding regeneration process started for all languages."}
