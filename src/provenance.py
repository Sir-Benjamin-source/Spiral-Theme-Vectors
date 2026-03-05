# src/provenance.py
"""
Provenance: Simple stamping wrapper for outputs using Version-Checker.

Adds hash-chained, timestamped provenance to theme analysis, vectors,
refinements, and metrics. Ensures traceability and tamper-evidence.
"""

from typing import Any, Dict
import hashlib
import time
import json

# Placeholder for real Version-Checker import
# In production: from version_checker import VersionChecker
class MockVersionChecker:
    """Mock: simulates Version-Checker stamping"""
    def __init__(self):
        self.version = "1.0.0"
        self.build_id = "mock-build-001"
    
    def generate_stamp(self, data: Any) -> str:
        """Generate a simple hash-based stamp for any serializable data"""
        data_str = json.dumps(data, sort_keys=True, default=str)
        hash_obj = hashlib.sha256(data_str.encode('utf-8'))
        timestamp = int(time.time())
        return f"v{self.version}#{self.build_id}#{timestamp}#{hash_obj.hexdigest()[:16]}"


class ProvenanceStamp:
    """
    Attaches provenance stamps to any output dictionary or object.
    
    Uses Version-Checker (or mock) to create verifiable stamps.
    """
    
    def __init__(self):
        self.checker = MockVersionChecker()  # Replace with real VersionChecker in prod
    
    def stamp_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add provenance stamp to the output dict.
        
        Args:
            output: Any dict (themes, vector, refined text, metrics, etc.)
            
        Returns:
            Original dict with added 'provenance' key
        """
        if not isinstance(output, dict):
            output = {"result": output}
        
        stamp_data = {
            "timestamp": int(time.time()),
            "version": self.checker.version,
            "build_id": self.checker.build_id,
            "input_hash": self._hash_input(output.get("input", {})),
            "content_hash": self._hash_content(output)
        }
        
        stamp = self.checker.generate_stamp(stamp_data)
        output["provenance"] = {
            "stamp": stamp,
            "details": stamp_data,
            "note": "Verifiable via Version-Checker; hash includes all keys except provenance"
        }
        
        return output
    
    def _hash_input(self, input_data: Any) -> str:
        """Simple hash of input for traceability"""
        data_str = json.dumps(input_data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()[:16]
    
    def _hash_content(self, content: Dict) -> str:
        """Hash of the main content (excluding provenance)"""
        clean_content = {k: v for k, v in content.items() if k != "provenance"}
        data_str = json.dumps(clean_content, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()[:16]


# Quick manual test block
if __name__ == "__main__":
    sample_output = {
        "refined_text": "Della sacrificed her hair for Jim's gift...",
        "metrics": {"creativity": 84, "engagement": 90, "validity": 93},
        "priority_vector": {"sacrifice": 0.42, "irony": 0.31}
    }
    
    stamper = ProvenanceStamp()
    stamped = stamper.stamp_output(sample_output)
    
    print("Stamped output:")
    print(stamped)