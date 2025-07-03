from fastapi import FastAPI, APIRouter

router = APIRouter(prefix="/api/v1/faq", tags=["FAQ"])

# route for getting a FAQ and returning it in a JSON format
@router.get("/ask", summary="Get FAQ")
def get_faq():
    return {
        "faq": [
            {
                "question": "What is AI FAQ Bot?",
                "answer": "AI FAQ Bot is a FastAPI application that provides an API for managing FAQs.",
            },
            {
                "question": "How do I use the API?",
                "answer": "You can use the API by sending requests to the endpoints defined in the documentation.",
            },
        ]
    }
