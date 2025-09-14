"""
Simplified File Analyzer for Testing
Works without external dependencies
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any

class FileAnalyzer:
    """Simplified file-based malware analyzer"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.malicious_patterns = [
            "cmd.exe", "powershell", "DownloadString", "Invoke-Expression",
            "regsvr32", "rundll32", "wscript", "cscript", "mshta"
        ]
        self.suspicious_extensions = [".exe", ".bat", ".cmd", ".ps1", ".vbs", ".js"]
    
    def predict(self, file_path: str) -> Dict:
        """Analyze file for malware characteristics"""
        try:
            if not os.path.exists(file_path):
                return {
                    "prediction": "error",
                    "confidence": 0.0,
                    "threat_type": "File Not Found",
                    "timestamp": datetime.now().isoformat(),
                    "error": "File not found"
                }
            
            # Basic file analysis
            file_size = os.path.getsize(file_path)
            file_extension = os.path.splitext(file_path)[1].lower()
            
            # Check file extension
            is_suspicious_extension = file_extension in self.suspicious_extensions
            
            # Read file content for pattern analysis
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
            except:
                # Binary file - check size and extension
                if is_suspicious_extension and file_size > 1024:
                    return {
                        "prediction": "suspicious",
                        "confidence": 0.6,
                        "threat_type": "Suspicious Binary",
                        "timestamp": datetime.now().isoformat(),
                        "features": {
                            "file_size": file_size,
                            "extension": file_extension,
                            "is_binary": True
                        }
                    }
                else:
                    return {
                        "prediction": "benign",
                        "confidence": 0.8,
                        "threat_type": "Clean File",
                        "timestamp": datetime.now().isoformat(),
                        "features": {
                            "file_size": file_size,
                            "extension": file_extension,
                            "is_binary": True
                        }
                    }
            
            # Analyze content for malicious patterns
            malicious_count = 0
            found_patterns = []
            
            for pattern in self.malicious_patterns:
                if pattern.lower() in content:
                    malicious_count += 1
                    found_patterns.append(pattern)
            
            # Calculate threat score
            threat_score = malicious_count / len(self.malicious_patterns)
            
            if threat_score > 0.3:
                prediction = "malicious"
                confidence = min(0.9, 0.5 + threat_score * 0.4)
                threat_type = "Script-based Malware"
            elif threat_score > 0.1:
                prediction = "suspicious"
                confidence = 0.6
                threat_type = "Potentially Suspicious"
            else:
                prediction = "benign"
                confidence = 0.8
                threat_type = "Clean File"
            
            return {
                "prediction": prediction,
                "confidence": confidence,
                "threat_type": threat_type,
                "timestamp": datetime.now().isoformat(),
                "features": {
                    "file_size": file_size,
                    "extension": file_extension,
                    "malicious_patterns": found_patterns,
                    "threat_score": threat_score,
                    "pattern_count": malicious_count
                }
            }
            
        except Exception as e:
            return {
                "prediction": "error",
                "confidence": 0.0,
                "threat_type": "Analysis Error",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }





