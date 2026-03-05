# src/theme_analysis.py
"""
ThemeAnalysisTool: Detects themes with confidence scores from input text.

Uses generality checks (replicated chains, motif validity) and literary pattern matching
to produce a confidence-weighted theme dictionary that feeds PriorityVector.
"""

from typing import Dict, List, Tuple
import re
from collections import Counter

# Placeholder for future integration with Spiral-Path auditors
# In real impl, replace with actual imports from Spiral-Path
class MockGeneralityAuditor:
    def score_chain_replication(self, text: str, motif: str) -> float:
        """Mock: returns probability of motif replication (0.0–1.0)"""
        # In production: use real auditor logic (e.g., ControversySniffer, chain matching)
        count = len(re.findall(re.escape(motif), text.lower()))
        return min(1.0, count / max(1, len(text.split()) / 50))  # simple heuristic

class MockLiteraryAuditor:
    def detect_themes(self, text: str) -> List[Tuple[str, float]]:
        """Mock: returns (theme, confidence) pairs from text"""
        # In production: integrate author profiles, genre generalities, arc mapping
        common_themes = {
            "sacrifice": 0.92,
            "irony": 0.88,
            "poverty": 0.65,
            "biblical_allusion": 0.80,
            "love": 0.75,
            "gender_roles": 0.50
        }
        # Filter to those with some evidence
        detected = [(t, c) for t, c in common_themes.items() if "sacrifice" in text.lower() or "gift" in text.lower()]
        return detected or [("unknown", 0.1)]


class ThemeAnalysisTool:
    """
    Analyzes input text to extract themes with confidence scores.
    
    Combines generality (chain replication) and literary (motif/arc) checks.
    Outputs a dict suitable for PriorityVector initialization.
    """
    
    def __init__(self):
        self.generality_auditor = MockGeneralityAuditor()  # Replace with real in prod
        self.literary_auditor = MockLiteraryAuditor()      # Replace with real in prod
        self.min_confidence_threshold = 0.4
    
    def analyze(self, text: str) -> Dict[str, float]:
        """
        Run full theme detection on input text.
        
        Returns:
            Dict[theme_name: confidence_score] — ready for PriorityVector
        """
        if not text.strip():
            raise ValueError("Input text cannot be empty")
            
        # Step 1: Literary detection (motifs, arcs, allusions)
        literary_results = self.literary_auditor.detect_themes(text)
        
        # Step 2: Generality validation (chain replication, motif strength)
        theme_confidences: Dict[str, float] = {}
        for theme, lit_conf in literary_results:
            # Score how well the theme replicates in chains
            replication_prob = self.generality_auditor.score_chain_replication(text, theme)
            
            # Combine: weighted average (literary confidence + replication)
            combined_conf = 0.6 * lit_conf + 0.4 * replication_prob
            
            if combined_conf >= self.min_confidence_threshold:
                theme_confidences[theme] = combined_conf
        
        # Step 3: Fallback if no themes meet threshold
        if not theme_confidences:
            theme_confidences["default"] = 0.5  # minimal safe fallback
        
        return theme_confidences
    
    def get_key_motifs(self, text: str, top_n: int = 5) -> List[str]:
        """
        Extract frequent motifs/words for debugging or generality checks.
        """
        words = re.findall(r'\b\w+\b', text.lower())
        common = Counter(words).most_common(top_n)
        return [word for word, _ in common]


# Quick manual test block
if __name__ == "__main__":
    # Example text snippet (abridged Gift of the Magi)
    sample_text = """
    Della cried nearly all day, and into the night. She had only $1.87 to buy Jim a gift.
    Her hair was her pride, but she sold it for twenty dollars to buy a chain for his watch.
    When Jim came home, he stared at her short hair. His gift was combs for her long hair.
    They had sacrificed their treasures for each other.
    """
    
    tool = ThemeAnalysisTool()
    themes = tool.analyze(sample_text)
    print("Detected themes with confidences:", themes)
    
    # Simulate feeding to PriorityVector (once we have it)
    # from priority_vector import PriorityVector
    # pv = PriorityVector(themes)
    # print(pv)
