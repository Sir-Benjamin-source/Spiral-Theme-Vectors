# src/spiral_integration.py
"""
SpiralIntegration: Applies Spiral Theory refinement loops with thematic emphasis.

Takes input text + priority vector and runs iterative refinement passes:
1. Idea generation (weighted by vector)
2. Elaboration & theme expansion
3. Structure & arc organization
4. Tone/style polish & final refinement

Produces refined text + basic metrics.
"""

from typing import Dict, Tuple, List
import random  # placeholder for creative variation


class SpiralRefinement:
    """
    Executes the 4-loop spiral refinement process with vector-weighted emphasis.
    
    Each loop builds on the previous, incorporating thematic priorities.
    """
    
    def __init__(self):
        # Relative influence per loop (adjustable)
        self.loop_weights = {
            "idea_generation": 0.25,
            "elaboration": 0.25,
            "structure": 0.25,
            "refinement": 0.25
        }
        # Placeholder for future real spiral engine integration
        self.variation_phrases = [
            "Deepened emotional resonance. ",
            "Amplified thematic layering. ",
            "Tightened narrative arc. ",
            "Polished stylistic nuance. "
        ]
    
    def refine(self, 
               original_text: str, 
               priority_vector: Dict[str, float]) -> Tuple[str, Dict[str, float]]:
        """
        Run full spiral refinement with thematic emphasis.
        
        Args:
            original_text: Raw input text to refine
            priority_vector: Dict[theme: weight] from PriorityVector
            
        Returns:
            (refined_text, metrics_dict)
        """
        if not original_text.strip():
            raise ValueError("Input text cannot be empty")
            
        current_text = original_text
        emphasis_boost = sum(priority_vector.values()) * 0.15  # small global influence
        
        # Run each loop sequentially
        for loop_name, base_weight in self.loop_weights.items():
            # Boost this loop's influence based on vector strength
            loop_boost = emphasis_boost * base_weight * 4  # scale to noticeable effect
            
            current_text = self._apply_loop(
                current_text,
                loop_name,
                loop_boost,
                priority_vector
            )
        
        # Placeholder metrics (replace with real scoring in production)
        metrics = {
            "creativity": round(random.uniform(70, 92) + emphasis_boost * 10, 1),
            "engagement": round(random.uniform(75, 95) + emphasis_boost * 8, 1),
            "clarity": round(random.uniform(80, 98) + emphasis_boost * 5, 1),
            "validity_prob": round(random.uniform(85, 96) + emphasis_boost * 4, 1)
        }
        
        return current_text, metrics
    
    def _apply_loop(self, 
                    text: str, 
                    loop_name: str, 
                    boost: float, 
                    priority_vector: Dict[str, float]) -> str:
        """
        Simulate one spiral refinement loop with vector-weighted variation.
        """
        # Choose variation phrase based on dominant theme
        dominant_theme = max(priority_vector.items(), key=lambda x: x[1])[0] if priority_vector else "default"
        
        prefix = f"[{loop_name.upper()}] "
        variation = random.choice(self.variation_phrases)
        
        # Apply "thematic flavor" based on boost and dominant theme
        if boost > 0.1:
            flavor = f"({dominant_theme} emphasis intensified) "
        else:
            flavor = ""
        
        # Simulate refinement by appending a stylized continuation
        continuation = f"Refined with {variation}{flavor}in the spirit of {dominant_theme}. "
        
        return prefix + continuation + text[:120] + "..."  # truncated for demo readability


# Quick manual test block
if __name__ == "__main__":
    # Example input (abridged Gift of the Magi snippet)
    sample_text = """
    Della cried nearly all day, and into the night. She had only $1.87 to buy Jim a gift.
    Her hair was her pride, but she sold it for twenty dollars to buy a chain for his watch.
    When Jim came home, he stared at her short hair. His gift was combs for her long hair.
    They had sacrificed their treasures for each other.
    """
    
    # Simulate a priority vector (from earlier PriorityVector output)
    example_vector = {
        "sacrifice": 0.50,
        "irony": 0.25,
        "poverty": 0.15,
        "love": 0.10
    }
    
    refiner = SpiralRefinement()
    refined_text, metrics = refiner.refine(sample_text, example_vector)
    
    print("=== Original (truncated) ===")
    print(sample_text.strip()[:150] + "...\n")
    
    print("=== Refined Output ===")
    print(refined_text)
    
    print("\n=== Metrics ===")
    print(metrics)