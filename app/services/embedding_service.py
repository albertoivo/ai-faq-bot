import json
import pickle
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.services.openai_services import detect_language, get_embeddings


class EmbeddingService:
    def __init__(self, data_path: Path = Path("data")):
        self.data_path = data_path
        # Language-specific paths will be set dynamically
        self.faq_data_path = None
        self.embeddings_path = None
        self.faq_data = None
        self.embeddings = None

    def _load_resources_for_language(self, language: str):
        """Loads the FAQ data and embeddings for a specific language."""
        self.faq_data_path = self.data_path / f"faq_data_{language}.json"
        self.embeddings_path = self.data_path / f"faq_embeddings_{language}.pkl"

        self.faq_data = self._load_faq_data()
        self.embeddings = self._get_or_generate_embeddings()

    def _load_faq_data(self) -> List[Dict[str, Any]]:
        """Loads the FAQ data from the JSON file."""
        if not self.faq_data_path.exists():
            print(f"Warning: FAQ data file not found at {self.faq_data_path}")
            return []
        # Ensure correct encoding for different languages
        with open(self.faq_data_path, "r", encoding="utf-8") as f:
            return json.load(f).get("faq", [])

    def _get_or_generate_embeddings(self) -> np.ndarray | None:
        """Loads saved embeddings or generates them if they don't exist."""
        if self.embeddings_path.exists():
            with open(self.embeddings_path, "rb") as f:
                return pickle.load(f)

        if not self.faq_data:
            return None

        print(f"Generating embeddings for {self.faq_data_path.name}...")
        questions = [item["question"] for item in self.faq_data]
        embeddings = get_embeddings(questions)

        # Convert to numpy array for easier calculations
        embeddings_np = np.array(embeddings)

        with open(self.embeddings_path, "wb") as f:
            pickle.dump(embeddings_np, f)

        return embeddings_np

    def find_best_match(
        self, query: str, threshold: float = 0.8
    ) -> Tuple[str, str] | None:
        """
        Finds the best matching FAQ for a given query using semantic search.

        Args:
            query (str): The user's question.
            threshold (float): The minimum similarity score to consider a match.

        Returns:
            Tuple[str, str] | None: A tuple containing the best matching question
                                     and answer, or None if no suitable match is found.
        """
        # 1. Detect language from the query
        language = detect_language(query)
        print(f"Detected language: {language}")

        # 2. Load resources for the detected language
        self._load_resources_for_language(language)

        if not self.faq_data or self.embeddings is None:
            print("Error: FAQ data or embeddings not available.")
            return None

        # 3. Generate embedding for the user's query
        query_embedding = np.array(get_embeddings([query]))

        # 4. Calculate cosine similarity
        similarities = cosine_similarity(query_embedding, self.embeddings)

        # 5. Find the best match
        best_match_index = np.argmax(similarities)
        best_match_score = similarities[0, best_match_index]

        print(
            f"Best match found: Index={best_match_index}, Score={best_match_score:.4f}"
        )

        if best_match_score >= threshold:
            best_match_faq = self.faq_data[best_match_index]
            return best_match_faq["question"], best_match_faq["answer"]

        return None
