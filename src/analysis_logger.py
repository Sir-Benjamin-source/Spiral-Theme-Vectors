# src/analysis_logger.py
"""
AnalysisLogger: Records summaries, analyses, and refinements to JSON log.

Enables the repo to accumulate examples for future reference, connections, and extension.
"""

from doctest import OutputChecker
from typing import Dict, Any, Optional
import json
import os
import time

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'analyses.json')


class AnalysisLogger:
    """
    Logs analysis outputs to a JSON file for accumulation and retrieval.
    
    Each entry includes timestamp, input snippet, output, and optional connections.
    """
    
    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        self.log_file = LOG_FILE
        self._ensure_log_exists()
    
    def _ensure_log_exists(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)
    
    def log_analysis(self, 
                     input_text: str, 
                     output: Dict[str, Any], 
                     connections: Optional[list[str]] = None, 
                     notes: str = "") -> None:
        """
        Append a new analysis entry to the log.
        
        Args:
            input_text: Original input (truncated if long)
            output: Dict with themes, vector, refined_text, metrics, stamp
            connections: Optional list of related example IDs or descriptions
            notes: Optional user/agent note
        """
        entry = {
            "id": int(time.time()),  # simple unique ID
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "input_snippet": input_text[:200] + "..." if len(input_text) > 200 else input_text,
            "output": output,
            "connections": connections or [],
            "notes": notes
        }
        
        with open(self.log_file, 'r+') as f:
            logs = json.load(f)
            logs.append(entry)
            f.seek(0)
            json.dump(logs, f, indent=4)
    
    def get_logs(self, limit: int = 10) -> list[Dict]:
        """Retrieve last N log entries."""
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        return logs[-limit:]

    def search_logs(self, query: str) -> list[Dict]:
        """Simple keyword search on notes or input_snippet."""
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        return [entry for entry in logs if query.lower() in entry["input_snippet"].lower() or query.lower() in entry["notes"].lower()]

# Quick manual test block (self-contained — no external variables needed)
if __name__ == "__main__":
    logger = AnalysisLogger()
    
    # Define sample data right here
    sample_input = "Della cried nearly all day, and into the night. She had only $1.87 to buy Jim a gift..."
    
    sample_output = {
        "themes": {"sacrifice": 0.693},
        "vector": {"sacrifice": 0.26},
        "refined_text": "Sample refined text with thematic emphasis...",
        "metrics": {"creativity": 84, "engagement": 90},
        "stamp": "v1.0#example-hash"
    }
    
    logger.log_analysis(
        input_text=sample_input,
        output=sample_output,
        connections=["Magi poverty lens", "sacrifice baseline"],
        notes="Test log entry with connections and notes"
    )
    
    print("Recent log entry:")
    print(logger.get_logs(limit=1))
    
    print("\nSearched for 'poverty':")
    print(logger.search_logs("poverty"))