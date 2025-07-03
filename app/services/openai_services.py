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
            print(f"Warning: Could not determine a valid language code. Response: '{language_code}'")
            return "en"  # Default to English as a fallback

    except Exception as e:
        print(f"An error occurred during language detection: {e}")
        raise