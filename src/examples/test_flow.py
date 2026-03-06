# test_flow.py (run from repo root)
import sys
import os

# Ensure src/ is on path (from repo root)
sys.path.insert(0, os.path.abspath('src'))

from theme_analysis import ThemeAnalysisTool
from priority_vector import PriorityVector
from spiral_integration import SpiralRefinement
from provenance import ProvenanceStamp

def run_test():
    print("=== Full Flow Test Started ===\n")

    # Sample input text
    sample_text = """
    Della cried nearly all day, and into the night. She had only $1.87 to buy Jim a gift.
    Her hair was her pride, but she sold it for twenty dollars to buy a chain for his watch.
    When Jim came home, he stared at her short hair. His gift was combs for her long hair.
    They had sacrificed their treasures for each other.
    """

    # Step 1: Theme Analysis
    tool = ThemeAnalysisTool()
    themes = tool.analyze(sample_text)
    print("Detected Themes:")
    print(themes)
    print("")

    # Step 2: Priority Vector
    pv = PriorityVector(themes)
    print("Default Priority Vector:")
    print(pv.get_vector())
    print("")

    # Optional nudge
    nudge = {"poverty": 0.52}
    nudged_vector = pv.apply_nudge(nudge)
    print(f"After nudge {nudge}:")
    print(nudged_vector)
    print("")

    # Step 3: Spiral Refinement
    refiner = SpiralRefinement()
    refined, metrics = refiner.refine(sample_text, nudged_vector)
    print("Refined Text:")
    print(refined)
    print("")
    print("Metrics:")
    print(metrics)
    print("")

    # Step 4: Provenance Stamp
    output = {
        "refined_text": refined,
        "metrics": metrics,
        "priority_vector": nudged_vector
    }
    stamper = ProvenanceStamp()
    stamped = stamper.stamp_output(output)
    print("Final Stamped Output (excerpt):")
    print(stamped)

    print("\n=== Test Completed ===")


if __name__ == "__main__":
    run_test()

