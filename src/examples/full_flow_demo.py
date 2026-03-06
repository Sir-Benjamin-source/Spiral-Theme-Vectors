# examples/full_flow_demo.py
"""
End-to-end demo: text → theme analysis → priority vector → spiral refinement → provenance stamp
"""

import sys
import os

# Add src/ to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from theme_analysis import ThemeAnalysisTool
from priority_vector import PriorityVector
from spiral_integration import SpiralRefinement
from provenance import ProvenanceStamp


def full_flow_demo(input_text: str, nudge: dict = None):
    print("=== Starting Full Flow Demo ===\n")
    print("Input text (truncated):")
    print(input_text.strip()[:150] + "..." if len(input_text) > 150 else input_text.strip())
    print("\n")

    # 1. Theme Analysis
    tool = ThemeAnalysisTool()
    themes = tool.analyze(input_text)
    print("Detected Themes & Confidences:")
    print(themes)
    print("\n")

    # 2. Priority Vector
    pv = PriorityVector(themes)
    print("Default Priority Vector:")
    print(pv.get_vector())
    print("\n")

    if nudge:
        nudged_vector = pv.apply_nudge(nudge)
        print(f"After nudge {nudge}:")
        print(nudged_vector)
        print("\n")
        active_vector = nudged_vector
    else:
        active_vector = pv.get_vector()

    # 3. Spiral Refinement
    refiner = SpiralRefinement()
    refined_text, metrics = refiner.refine(input_text, active_vector)
    print("Refined Output:")
    print(refined_text)
    print("\nMetrics:")
    print(metrics)
    print("\n")

    # 4. Provenance Stamp
    output_dict = {
        "original_text": input_text[:200],  # truncated for demo
        "refined_text": refined_text,
        "metrics": metrics,
        "priority_vector": active_vector
    }
    stamper = ProvenanceStamp()
    stamped = stamper.stamp_output(output_dict)
    print("Final Stamped Output (excerpt):")
    print(stamped)


# Run demo
if __name__ == "__main__":
    # Sample text (abridged Gift of the Magi)
    sample = """
    Della cried nearly all day, and into the night. She had only $1.87 to buy Jim a gift.
    Her hair was her pride, but she sold it for twenty dollars to buy a chain for his watch.
    When Jim came home, he stared at her short hair. His gift was combs for her long hair.
    They had sacrificed their treasures for each other. Of all who give gifts these two were the wisest.
    """

    # Optional nudge (comment out to use default)
    nudge_example = {"poverty": 0.52}

    full_flow_demo(sample, nudge=nudge_example)