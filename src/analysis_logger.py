# src/analysis_logger.py
"""
AnalysisLogger: Records summaries, analyses, and refinements to JSON log.

Enables the repo to accumulate examples for future reference, connections, and extension.
"""

from typing import Dict, Any
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
                     connections: List[str] = None, 
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
    
    def get_logs(self, limit: int = 10) -> List[Dict]:
        """Retrieve last N log entries."""
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        return logs[-limit:]

    def search_logs(self, query: str) -> List[Dict]:
        """Simple keyword search on notes or input_snippet."""
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        return [entry for entry in logs if query.lower() in entry["input_snippet"].lower() or query.lower() in entry["notes"].lower()]


# Quick manual test block
if __name__ == "__main__":
    logger = AnalysisLogger()
    
    # Sample log entry
    sample_output = {
        "themes": {"sacrifice": 0.693},
        "vector": {"sacrifice": 0.26},
        "refined_text": "Sample refined text...",
        "metrics": {"creativity": 84},
        "stamp": "v1.0#example-hash"
    }
    
    logger.log_analysis(
        input_text="Della cried nearly all day...",
        output=sample_output,
        connections=["Magi poverty lens"],
        notes="Test log with connections"
    )
    
    recent = logger.get_logs(limit=1)
    print("Recent log entry:")
    print(recent)
    
    searched = logger.search_logs("poverty")
    print("\nSearched for 'poverty':")
    print(searched)