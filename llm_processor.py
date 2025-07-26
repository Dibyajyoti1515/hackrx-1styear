from transformers import pipeline
from typing import List, Dict, Tuple

class LLMProcessor:
    def __init__(self):
        # Use a free open-source model like facebook/bart-large-cnn or meta-llama/Llama-3.1 (requires GPU)
        self.generator = pipeline('text-generation', model='distilgpt2')  # Placeholder: Replace with Llama via Hugging Face

    def generate_answer(self, question: str, contexts: List[Dict]) -> Tuple[str, Dict]:
        context_text = "\n".join([ctx['text'] for ctx in contexts])
        prompt = f"Question: {question}\nContext: {context_text}\nAnswer concisely:"
        generated = self.generator(prompt, max_length=200, num_return_sequences=1)[0]['generated_text']
        answer = generated.split("Answer concisely:")[-1].strip()
        
        rationale = self._generate_rationale(question, contexts, answer)
        return answer, rationale

    def _generate_rationale(self, question: str, contexts: List[Dict], answer: str) -> Dict:
        """Generate comprehensive decision rationale"""
        rationale = {
            "reasoning_steps": [
                "1. Retrieved relevant document sections based on semantic similarity",
                "2. Analyzed context for information related to the question", 
                "3. Extracted key information that directly answers the question",
                "4. Formulated response based on available evidence"
            ],
            "key_evidence": [],
            "confidence_factors": []
        }
        
        # Extract supporting evidence with relevance scores
        for i, ctx in enumerate(contexts[:3]):
            if ctx['relevance_score'] > 0.7:
                rationale["key_evidence"].append({
                    "source": f"Document chunk {i+1}",
                    "relevance": round(ctx['relevance_score'], 3),
                    "excerpt": ctx['text'][:200] + "..."
                })
        
        # Add simple confidence (placeholder)
        rationale["confidence_factors"].append({"overall_confidence": max([ctx['relevance_score'] for ctx in contexts])})
        
        return rationale