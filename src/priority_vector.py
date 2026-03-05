# src/priority_vector.py
"""
PriorityVector: Grounded, constrained thematic emphasis weights.

Derived from detected theme confidences and clamped against textual evidence.
Prevents hallucination by rejecting or limiting unsupported themes.
"""

from typing import Dict, Optional
import copy


class PriorityVector:
    """
    Manages thematic emphasis weights tied to detected text evidence.
    
    - Defaults are generated proportional to theme confidence scores.
    - Nudges are allowed only on supported themes and within safe bounds.
    - Ensures all variation remains text-grounded.
    """
    
    def __init__(self, theme_confidences: Dict[str, float]):
        """
        Initialize with detected theme confidences from text analysis.
        
        Args:
            theme_confidences: Dict[theme_name: confidence_score (0.0–1.0)]
                               Example: {'sacrifice': 0.92, 'irony': 0.88, 'poverty': 0.65}
        """
        if not theme_confidences:
            raise ValueError("Theme confidences cannot be empty")
            
        self.theme_confidences = copy.deepcopy(theme_confidences)
        self.default_vector = self._normalize(self._compute_default())
        self.current_vector: Optional[Dict[str, float]] = None
        self.supported_themes = set(theme_confidences.keys())
    
    def _compute_default(self) -> Dict[str, float]:
        """Generate initial vector proportional to confidence scores."""
        total_conf = sum(self.theme_confidences.values())
        if total_conf == 0:
            return {theme: 0.0 for theme in self.theme_confidences}
        return {theme: conf / total_conf for theme, conf in self.theme_confidences.items()}
    
    def _normalize(self, vector: Dict[str, float]) -> Dict[str, float]:
        """Normalize vector so sum ≈ 1.0."""
        total = sum(vector.values())
        if total == 0:
            return vector  # avoid div by zero
        return {k: v / total for k, v in vector.items()}
    
    def apply_nudge(self, nudge: Dict[str, float], max_delta: float = 0.3, max_multiplier: float = 2.0) -> Dict[str, float]:
        """
        Apply user/agent nudge to the default vector with safety clamps.
        
        Args:
            nudge: Dict[theme: delta_value] — adjustments to apply
            max_delta: Maximum allowed change per axis (default 0.3)
            max_multiplier: Max multiple of original confidence-derived weight
            
        Returns:
            Normalized adjusted vector
        """
        adjusted = copy.deepcopy(self.default_vector)
        
        for theme, delta in nudge.items():
            if theme not in self.supported_themes:
                # Silently ignore unsupported themes (or log in production)
                continue
                
            original_weight = self.default_vector.get(theme, 0.0)
            max_allowed = min(
                original_weight + max_delta,
                original_weight * max_multiplier
            )
            min_allowed = max(0.0, original_weight - max_delta)
            
            new_weight = original_weight + delta
            new_weight = max(min_allowed, min(max_allowed, new_weight))
            
            adjusted[theme] = new_weight
        
        # Re-normalize
        self.current_vector = self._normalize(adjusted)
        return self.current_vector
    
    def get_vector(self) -> Dict[str, float]:
        """Return the current (or default) vector."""
        return self.current_vector or self.default_vector
    
    def get_supported_themes(self) -> set:
        """Return set of themes with textual evidence."""
        return self.supported_themes
    
    def __repr__(self) -> str:
        return f"PriorityVector(default={self.default_vector}, current={self.current_vector})"


# Quick example usage (for manual testing / README)
if __name__ == "__main__":
    # Simulate detected themes from text analysis
    example_confidences = {
        "sacrifice": 0.92,
        "irony": 0.88,
        "poverty": 0.65,
        "biblical_allusion": 0.80
    }
    
    pv = PriorityVector(example_confidences)
    print("Default vector:", pv.get_vector())
    
    # Nudge toward poverty lens
    nudged = pv.apply_nudge({"poverty": 0.52})
    print("After nudge:", nudged)
    
    # Try an unsupported theme (should be ignored)
    pv.apply_nudge({"cyberpunk_dystopia": 0.9})
    print("After invalid nudge (ignored):", pv.get_vector())
