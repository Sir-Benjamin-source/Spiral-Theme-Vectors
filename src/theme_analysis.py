# src/theme_analysis.py (updated with real-ish auditors)
"""
ThemeAnalysisTool: Detects themes with confidence scores from input text.

Uses simple but real generality (chain replication via n-grams) and literary pattern matching.
"""

from typing import Dict, List, Tuple
import re
from collections import Counter, defaultdict

class GeneralityAuditor:
    """Real-ish: scores motif replication using bigram/trigram overlap."""
    def score_chain_replication(self, text: str, motif: str) -> float:
        if not motif:
            return 0.0
        lower_text = text.lower()
        words = re.findall(r'\b\w+\b', lower_text)
        if len(words) < 5:
            return 0.0
        
        # Build bigrams
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        motif_bigrams = [f"{motif.lower()} {motif.lower()}", motif.lower()]  # simple motif variants
        
        count = sum(1 for bg in bigrams if any(m in bg for m in motif_bigrams))
        return min(1.0, count / max(1, len(bigrams) / 10))  # normalize

class LiteraryAuditor:
    """Real-ish: keyword + motif pattern matcher for common literary themes."""
    def __init__(self):
        # Simple keyword sets (expandable)
        self.theme_keywords = {
            "sacrifice": ["sacrifice", "gave up", "sold", "offered", "treasures"],
            "irony": ["stared", "useless", "futile", "irony", "twist"],
            "poverty": ["poor", "meager", "$", "flat", "wages"],
            "biblical_allusion": ["magi", "wise", "gift", "sheba", "solomon"],
            "love": ["love", "devotion", "embrace", "heart"],
            "gender_roles": ["pride", "provider", "she", "he"]
        }
    
    def detect_themes(self, text: str) -> List[Tuple[str, float]]:
        lower_text = text.lower()
        detected = []
        for theme, keywords in self.theme_keywords.items():
            matches = sum(lower_text.count(k) for k in keywords)
            conf = min(1.0, matches / max(1, len(lower_text.split()) / 50))
            if conf > 0.2:  # loose threshold
                detected.append((theme, conf))
        return sorted(detected, key=lambda x: x[1], reverse=True) or [("unknown", 0.1)]


class ThemeAnalysisTool:
    def __init__(self):
        self.generality_auditor = GeneralityAuditor()
        self.literary_auditor = LiteraryAuditor()
        self.min_confidence_threshold = 0.3  # lowered slightly for realism
    
    def analyze(self, text: str) -> Dict[str, float]:
        if not text.strip():
            raise ValueError("Input text cannot be empty")
            
        literary_results = self.literary_auditor.detect_themes(text)
        
        theme_confidences: Dict[str, float] = {}
        for theme, lit_conf in literary_results:
            replication_prob = self.generality_auditor.score_chain_replication(text, theme)
            combined_conf = 0.55 * lit_conf + 0.45 * replication_prob
            if combined_conf >= self.min_confidence_threshold:
                theme_confidences[theme] = round(combined_conf, 3)
        
        return theme_confidences or {"default": 0.5}
    
    def get_key_motifs(self, text: str, top_n: int = 5) -> List[str]:
        words = re.findall(r'\b\w+\b', text.lower())
        common = Counter(words).most_common(top_n)
        return [word for word, _ in common]


# Test block (optional — can be removed or kept)
if __name__ == "__main__":
    sample = """
    Della cried nearly all day, and into the night. She had only $1.87 to buy Jim a gift.
    Her hair was her pride, but she sold it for twenty dollars to buy a chain for his watch.
    When Jim came home, he stared at her short hair. His gift was combs for her long hair.
    They had sacrificed their treasures for each other.
    """
    tool = ThemeAnalysisTool()
    print(tool.analyze(sample))