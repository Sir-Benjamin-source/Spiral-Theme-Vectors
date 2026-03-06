#!/usr/bin/env bash
set -euo pipefail

echo "========================================"
echo "  Spiral-Theme-Vectors Full Flow Test  "
echo "========================================"
echo ""

# 1. Ensure we're in the repo root
cd "$(dirname "$0")" || exit 1

# 2. Activate Python environment if needed (Codespace usually has python3 ready)
PYTHON=python3

# 3. Create a temporary test script that runs the full flow
cat > /tmp/test_flow.py << 'EOF'
import sys
import os

# Add src/ to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

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
    print("Stamped Output (excerpt):")
    print(stamped)

    print("\n=== Test Completed Successfully ===")


if __name__ == "__main__":
    run_test()
EOF

# 4. Run the test
echo "Running full flow test..."
$PYTHON /tmp/test_flow.py

# 5. Clean up
rm -f /tmp/test_flow.py

echo ""
echo "Test finished. Check output above for any errors or unexpected behavior."
echo "If all steps printed without tracebacks → we're golden."