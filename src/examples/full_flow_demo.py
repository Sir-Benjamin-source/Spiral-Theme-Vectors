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
    print("Inside run_test() — starting now")
    
    sample_text = """
    Della cried nearly all day, and into the night. She had only $1.87 to buy Jim a gift.
    Her hair was her pride, but she sold it for twenty dollars to buy a chain for his watch.
    When Jim came home, he stared at her short hair. His gift was combs for her long hair.
    They had sacrificed their treasures for each other.
    """
    print("Sample text loaded")

    print("Creating ThemeAnalysisTool...")
    tool = ThemeAnalysisTool()
    print("Tool created OK")

    print("Running analyze()...")
    themes = tool.analyze(sample_text)
    print("Themes detected:")
    print(themes)
    print("")

    print("Creating PriorityVector...")
    pv = PriorityVector(themes)
    print("Vector created OK")

    print("Applying nudge...")
    nudge = {"poverty": 0.52}
    nudged_vector = pv.apply_nudge(nudge)
    print(f"After nudge {nudge}:")
    print(nudged_vector)
    print("")

    print("Creating SpiralRefinement...")
    refiner = SpiralRefinement()
    print("Refiner created OK")

    print("Running refine()...")
    refined, metrics = refiner.refine(sample_text, nudged_vector)
    print("Refined Text:")
    print(refined)
    print("")
    print("Metrics:")
    print(metrics)
    print("")

    print("Preparing output for stamp...")
    output = {
        "refined_text": refined,
        "metrics": metrics,
        "priority_vector": nudged_vector,
        "themes": themes
    }
    stamper = ProvenanceStamp()
    stamped = stamper.stamp_output(output)
    print("Stamped Output (excerpt):")
    print(stamped)
    print("\n")

    # NEW: Log the analysis
    print("Creating logger...")
    logger = AnalysisLogger()
    print("Logger created OK")

    logger.log_analysis(
        input_text=sample_text,
        output=stamped,
        connections=["Magi sacrifice baseline", "poverty nudge test"],
        notes="Full flow demo run with upgraded theme detection and poverty emphasis"
    )
    print("Logged to data/logs/analyses.json")
    print("Recent logs (last 2):")
    print(logger.get_logs(limit=2))
    print("\n=== Test Completed ===")
