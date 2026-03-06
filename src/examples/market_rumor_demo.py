# examples/market_rumor_demo.py
import sys
import os

# Force-add src/ (absolute for Codespace reliability)
sys.path.insert(0, '/workspaces/Spiral-Theme-Vectors/src')

from theme_analysis import ThemeAnalysisTool
from priority_vector import PriorityVector
from spiral_integration import SpiralRefinement
from provenance import ProvenanceStamp
from analysis_logger import AnalysisLogger

print("=== Market Rumor Test ===\n")

# Sample market rumor text
market_text = """
Rumors swirling that major exchange is insolvent after $2B withdrawal spike. CEO silent, on-chain data shows unusual transfers to cold wallets. Community in panic — is this FTX 2.0?
"""

# Step 1: Theme Analysis
tool = ThemeAnalysisTool()  # <-- This line was missing
themes = tool.analyze(market_text)
print("Detected Themes:")
print(themes)
print("")

# Step 2: Priority Vector
pv = PriorityVector(themes)
print("Default Priority Vector:")
print(pv.get_vector())
print("")

# Optional nudge (e.g., boost fear/speculation)
nudge = {"fear": 0.6, "speculation": 0.3}
nudged_vector = pv.apply_nudge(nudge)
print(f"After nudge {nudge}:")
print(nudged_vector)
print("")

# Step 3: Spiral Refinement
refiner = SpiralRefinement()
refined, metrics = refiner.refine(market_text, nudged_vector)
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
    "priority_vector": nudged_vector,
    "themes": themes
}
stamper = ProvenanceStamp()
stamped = stamper.stamp_output(output)
print("Stamped Output (excerpt):")
print(stamped)
print("\n")

# Step 5: Log it
logger = AnalysisLogger()
logger.log_analysis(
    input_text=market_text,
    output=stamped,
    connections=["Crypto FUD rumor", "speculation emphasis"],
    notes="Market rumor test with fear/speculation nudge"
)
print("Logged to data/logs/analyses.json")
print("Recent logs (last 2):")
print(logger.get_logs(limit=2))

print("\n=== Market Test Completed ===")
