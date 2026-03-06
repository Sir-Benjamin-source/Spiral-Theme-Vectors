# examples/full_flow_demo.py (

import sys
import os


REPO_ROOT = '/workspaces/Spiral-Theme-Vectors'
sys.path.insert(0, os.path.join(REPO_ROOT, 'src'))

# Verify path for debugging
print("sys.path includes src?:", any('src' in p for p in sys.path))

# Now imports
from theme_analysis import ThemeAnalysisTool
from priority_vector import PriorityVector
from spiral_integration import SpiralRefinement
from provenance import ProvenanceStamp
from analysis_logger import AnalysisLogger 

print("Attempting imports...")
try:
    from theme_analysis import ThemeAnalysisTool
    print("ThemeAnalysisTool imported OK")
except Exception as e:
    print("Import failed:", str(e))

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
    print("\nTop Motifs:")
    print(tool.get_key_motifs(sample_text))
    print("\n")

    pv = PriorityVector(themes)
    print("Default Priority Vector:")
    print(pv.get_vector())
    print("\n")

    nudge = {"poverty": 0.52}
    nudged_vector = pv.apply_nudge(nudge)
    print(f"After nudge {nudge}:")
    print(nudged_vector)
    print("\n")

    refiner = SpiralRefinement()
    refined, metrics = refiner.refine(sample_text, nudged_vector)
    print("Refined Text:")
    print(refined)
    print("\nMetrics:")
    print(metrics)
    print("\n")

    output = {
        "refined_text": refined,
        "metrics": metrics,
        "priority_vector": nudged_vector,
        "themes": themes  # add for completeness
    }
    stamper = ProvenanceStamp()
    stamped = stamper.stamp_output(output)
    print("Stamped Output (excerpt):")
    print(stamped)
    print("\n")

    # NEW: Log the analysis
    logger = AnalysisLogger()
    logger.log_analysis(
        input_text=sample_text,
        output=stamped,  # use stamped output
        connections=["Magi sacrifice baseline", "poverty nudge test"],
        notes="Full flow demo run with upgraded theme detection and poverty emphasis"
    )
    print("Logged to data/logs/analyses.json")
    print("Recent logs (last 2):")
    print(logger.get_logs(limit=2))
    print("\n=== Test Completed ===")