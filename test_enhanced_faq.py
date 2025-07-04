#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced FAQ Bot with LLM integration.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.embedding_service import EmbeddingService

def test_enhanced_faq():
    """Test the enhanced FAQ functionality."""
    service = EmbeddingService()
    
    # Test questions in different languages
    test_questions = [
        "What is this bot?",  # English
        "Como executo esta aplicação?",  # Portuguese  
        "How do I contribute?",  # English
        "Onde ficam os dados?",  # Portuguese
    ]
    
    print("=== Testing Enhanced FAQ Bot ===\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"Test {i}: {question}")
        print("-" * 50)
        
        # Test with LLM enhancement
        print("🤖 Enhanced Answer:")
        result = service.find_best_match(question, enhance_with_llm=True)
        if result:
            matched_question, enhanced_answer = result
            print(f"Matched FAQ: {matched_question}")
            print(f"Answer: {enhanced_answer}")
        else:
            print("No relevant FAQ found.")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_enhanced_faq()
