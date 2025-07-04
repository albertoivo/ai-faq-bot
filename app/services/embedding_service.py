import json
import pickle
import requests
from pathlib import Path
from typing import Any, Dict, List, Tuple
import hashlib

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.services.openai_services import (
    detect_language,
    get_embeddings,
    generate_friendly_answer,
)


class EmbeddingService:
    def __init__(self, data_path: Path = Path("data")):
        self.data_path = data_path
        self.data_path.mkdir(exist_ok=True)
        
        # Cache paths will be set dynamically
        self.faq_data = None
        self.embeddings = None

    def _get_cache_key(self, faq_url: str, language: str) -> str:
        """Gera uma chave de cache baseada na URL e idioma"""
        url_hash = hashlib.md5(faq_url.encode()).hexdigest()[:8]
        return f"faq_{url_hash}_{language}"

    def _load_faq_from_url(self, faq_url: str) -> List[Dict[str, Any]]:
        """Carrega FAQ data de uma URL"""
        try:
            response = requests.get(faq_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Suporta diferentes formatos de JSON
            if "faq" in data:
                return data["faq"]
            elif "faqs" in data:
                return data["faqs"]
            elif isinstance(data, list):
                return data
            else:
                raise ValueError("Invalid FAQ JSON format")
                
        except Exception as e:
            print(f"Error loading FAQ from URL {faq_url}: {e}")
            raise

    def _get_or_generate_embeddings(self, faq_data: List[Dict], cache_key: str) -> np.ndarray:
        """Carrega embeddings do cache ou gera novos"""
        cache_path = self.data_path / f"{cache_key}_embeddings.pkl"
        
        if cache_path.exists():
            with open(cache_path, "rb") as f:
                return pickle.load(f)

        # Gerar novos embeddings
        print(f"Generating embeddings for {cache_key}...")
        questions = [item["question"] for item in faq_data]
        embeddings = get_embeddings(questions)
        
        # Salvar no cache
        embeddings_np = np.array(embeddings)
        with open(cache_path, "wb") as f:
            pickle.dump(embeddings_np, f)
        
        return embeddings_np

    def find_best_match(
        self, query: str, faq_url: str, threshold: float = 0.8, enhance_with_llm: bool = True
    ) -> Tuple[str, str] | None:
        """
        Encontra a melhor resposta FAQ para uma pergunta, usando dados de uma URL.

        Args:
            query (str): A pergunta do usuário
            faq_url (str): URL do arquivo JSON com os dados FAQ
            threshold (float): Score mínimo de similaridade
            enhance_with_llm (bool): Se deve melhorar a resposta com LLM

        Returns:
            Tuple[str, str] | None: (pergunta, resposta) ou None se não encontrar
        """
        # 1. Detectar idioma
        language = detect_language(query)
        print(f"Detected language: {language}")

        # 2. Carregar FAQ da URL
        try:
            faq_data = self._load_faq_from_url(faq_url)
        except Exception as e:
            print(f"Failed to load FAQ from URL: {e}")
            return None

        if not faq_data:
            print("No FAQ data found")
            return None

        # 3. Gerar/carregar embeddings
        cache_key = self._get_cache_key(faq_url, language)
        embeddings = self._get_or_generate_embeddings(faq_data, cache_key)

        # 4. Gerar embedding da pergunta
        query_embedding = np.array(get_embeddings([query]))

        # 5. Calcular similaridade
        similarities = cosine_similarity(query_embedding, embeddings)
        best_match_index = np.argmax(similarities)
        best_match_score = similarities[0, best_match_index]

        print(f"Best match: Index={best_match_index}, Score={best_match_score:.4f}")

        if best_match_score >= threshold:
            best_match_faq = faq_data[best_match_index]
            original_question = best_match_faq["question"]
            original_answer = best_match_faq["answer"]
            
            # Melhorar resposta com LLM se solicitado
            if enhance_with_llm:
                try:
                    enhanced_answer = generate_friendly_answer(query, original_answer)
                    return original_question, enhanced_answer
                except Exception as e:
                    print(f"Failed to enhance answer: {e}")
                    return original_question, original_answer
            else:
                return original_question, original_answer

        return None
