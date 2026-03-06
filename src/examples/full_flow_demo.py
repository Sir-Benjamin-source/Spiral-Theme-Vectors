# examples/full_flow_demo.py (updated path handling)

import sys
import os

# Get repo root (works whether run from root or examples/)
REPO_ROOT = '/workspaces/Spiral-Theme-Vectors'
sys.path.insert(0, os.path.join(REPO_ROOT, 'src'))

# Now imports
from theme_analysis import ThemeAnalysisTool
from priority_vector import PriorityVector
from spiral_integration import SpiralRefinement
from provenance import ProvenanceStamp

def run_test():
    print("=== Full Flow Test Started ===\n")

    sample_text = """
    Della cried nearly all day, and into the night. She had only $1.87 to buy Jim a gift.
    Her hair was her pride, but she sold it for twenty dollars to buy a chain for his watch.
    When Jim came home, he stared at her short hair. His gift was combs for her long hair.
    They had sacrificed their treasures for each other.
    """

    tool = ThemeAnalysisTool()
    themes = tool.analyze(sample_text)
    print("Detected Themes & Confidences:")
    print(themes)
    print("\nTop Motifs (for debugging):")
    print(tool.get_key_motifs(sample_text))
    print("\n")

    pv = PriorityVector(themes)
    print("Default Priority Vector:")
    print(pv.get_vector())
    print("\n")

    nudge = {"poverty": 0.52}
    nudged = pv.apply_nudge(nudge)
    print(f"After nudge {nudge}:")
    print(nudged)
    print("\n")

    refiner = SpiralRefinement()
    refined, metrics = refiner.refine(sample_text, nudged)
    print("Refined Text:")
    print(refined)
    print("\nMetrics:")
    print(metrics)
    print("\n")

    output = {
        "refined_text": refined,
        "metrics": metrics,
        "priority_vector": nudged
    }
    stamper = ProvenanceStamp()
    stamped = stamper.stamp_output(output)
    print("Stamped Output (excerpt):")
    print(stamped)

    print("\n=== Test Completed ===")


if __name__ == "__main__":
    run_test()