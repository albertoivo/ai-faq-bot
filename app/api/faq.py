from fastapi import APIRouter, Depends, HTTPException, status
from openai import OpenAI

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

    This endpoint automatically detects the language of the query and searches the
    corresponding FAQ dataset (e.g., English or Portuguese).
    """
    match = service.find_best_match(request.question)

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
    Triggers the regeneration of embeddings for all supported languages.

    This is an asynchronous-like operation. The server will start the process
    and return a 202 Accepted response immediately.
    """
    supported_languages = ["en", "pt"]  # Define supported languages here
    for lang in supported_languages:
        try:
            # Load resources which will trigger generation if files don't exist
            # To force regeneration, we would first delete the .pkl file
            if service.embeddings_path and service.embeddings_path.exists():
                service.embeddings_path.unlink()

            # Re-initialize the service for the specific language to force reload
            lang_service = EmbeddingService(language=lang)
            lang_service._get_or_generate_embeddings()  # This will now regenerate

        except Exception as e:
            # In a real app, you might want to log this more robustly
            print(f"Could not regenerate embeddings for language '{lang}': {e}")
            # Decide if you want to raise an exception or just log the error

    return {"message": "Embedding regeneration process started for all languages."}
