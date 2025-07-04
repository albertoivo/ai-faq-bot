import os
from typing import List

from openai import OpenAI

# Configure the OpenAI client
# The API key is loaded from environment variables.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embeddings(
    texts: List[str], model: str = "text-embedding-ada-002"
) -> List[List[float]]:
    """
    Generates embeddings for a list of texts using the specified OpenAI model.

    Args:
        texts (List[str]): A list of strings to embed.
        model (str, optional): The OpenAI model to use for embeddings.
                               Defaults to "text-embedding-ada-002".

    Returns:
        List[List[float]]: A list of embeddings, where each embedding is a list of floats.

    Raises:
        Exception: If the API call fails.
    """
    try:
        # Replace newlines to avoid issues with the API
        texts = [text.replace("\n", " ") for text in texts]
        response = client.embeddings.create(input=texts, model=model)
        return [embedding.embedding for embedding in response.data]
    except Exception as e:
        # Handle API errors (e.g., invalid key, rate limits)
        print(f"An error occurred while generating embeddings: {e}")
        raise


def detect_language(text: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Detects the language of a given text using the OpenAI ChatCompletion API.

    Args:
        text (str): The text to analyze.
        model (str, optional): The model to use for detection.
                               Defaults to "gpt-3.5-turbo".

    Returns:
        str: The detected two-letter language code (e.g., "en", "pt").

    Raises:
        Exception: If the API call fails or the response is not as expected.
    """
    try:
        prompt = (
            f"Identify the language of the following text. "
            f"Respond with only the two-letter ISO 639-1 language code (e.g., 'en' for English, 'pt' for Portuguese). "
            f"Text: '{text}'"
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a language detection expert."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=5,
            temperature=0,
        )
        language_code = response.choices[0].message.content.strip().lower()

        # Basic validation to ensure it's a two-letter code
        if len(language_code) == 2 and language_code.isalpha():
            return language_code
        else:
            # Fallback or error
            print(
                f"Warning: Could not determine a valid language code. Response: '{language_code}'"
            )
            return "en"  # Default to English as a fallback

    except Exception as e:
        print(f"An error occurred during language detection: {e}")
        raise


def generate_friendly_answer(
    user_question: str, faq_answer: str, model: str = "gpt-3.5-turbo"
) -> str:
    """
    Generates a more friendly and helpful answer based on the FAQ content and user's question.

    Args:
        user_question (str): The original question from the user.
        faq_answer (str): The raw answer from the FAQ database.
        model (str, optional): The model to use for generating the response.
                               Defaults to "gpt-3.5-turbo".

    Returns:
        str: A more friendly and contextual answer.

    Raises:
        Exception: If the API call fails.
    """
    try:
        system_prompt = """You are a helpful and friendly AI assistant for the AI FAQ Bot project. 
        Your task is to take a user's question and a corresponding FAQ answer, then create a more 
        personalized, friendly, and comprehensive response. 

        Guidelines:
        - Be conversational and warm in tone
        - Address the user directly when appropriate
        - Add helpful context or tips when relevant
        - If the FAQ answer seems technical, explain it in simpler terms
        - Feel free to add encouraging words or next steps
        - Keep the core information from the FAQ answer intact
        - Don't make up information not present in the FAQ answer"""

        user_prompt = f"""
        User's question: "{user_question}"
        
        FAQ answer: "{faq_answer}"
        
        Please provide a friendly, helpful response that addresses the user's question using the FAQ information."""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=300,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"An error occurred while generating friendly answer: {e}")
        # Return the original FAQ answer as fallback
        return faq_answer
