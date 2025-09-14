"""
Simplified Signature Detector for Testing
Works without external dependencies
"""

import os
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any

class SignatureDetector:
    """Simplified signature-based threat detector"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.signature_database = {}
        self.yara_rules = {}
        self._load_sample_signatures()
    
    def _load_sample_signatures(self):
        """Load sample signatures for testing"""
        # Sample malicious file hashes
        self.signature_database = {
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Trojan.Generic",
            "d41d8cd98f00b204e9800998ecf8427e": "Malware.Sample",
            "5d41402abc4b2a76b9719d911017c592": "Virus.Test"
        }
        
        # Sample YARA rules
        self.yara_rules = {
            "suspicious_strings": {
                "description": "Detects suspicious strings",
                "strings": ["cmd.exe", "powershell", "DownloadString"],
                "condition": "2 of them"
            }
        }
    
    def detect_threats(self, file_path: str) -> Dict:
        """Detect threats using signature-based methods"""
        try:
            if not os.path.exists(file_path):
                return {
                    "detected": False,
                    "threat_type": "Unknown",
                    "confidence": 0.0,
                    "method": "signature",
                    "timestamp": datetime.now().isoformat(),
                    "error": "File not found"
                }
            
            # Calculate file hash
            file_hash = self._calculate_hash(file_path)
            
            # Check against signature database
            if file_hash in self.signature_database:
                return {
                    "detected": True,
                    "threat_type": self.signature_database[file_hash],
                    "confidence": 0.95,
                    "method": "signature",
                    "timestamp": datetime.now().isoformat(),
                    "details": {
                        "hash": file_hash,
                        "signature_match": True
                    }
                }
            
            # Check with YARA rules
            yara_result = self._check_yara_rules(file_path)
            if yara_result["detected"]:
                return yara_result
            
            return {
                "detected": False,
                "threat_type": "Clean",
                "confidence": 0.0,
                "method": "signature",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "hash": file_hash,
                    "signature_match": False
                }
            }
            
        except Exception as e:
            return {
                "detected": False,
                "threat_type": "Error",
                "confidence": 0.0,
                "method": "signature",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _calculate_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
        except:
            return "error_hash"
    
    def _check_yara_rules(self, file_path: str) -> Dict:
        """Check file against YARA rules"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            for rule_name, rule in self.yara_rules.items():
                matches = 0
                for string in rule["strings"]:
                    if string.lower() in content:
                        matches += 1
                
                if matches >= 2:  # Simple condition check
                    return {
                        "detected": True,
                        "threat_type": f"YARA: {rule_name}",
                        "confidence": 0.8,
                        "method": "yara",
                        "timestamp": datetime.now().isoformat(),
                        "details": {
                            "rule": rule_name,
                            "matches": matches
                        }
                    }
            
            return {
                "detected": False,
                "threat_type": "Clean",
                "confidence": 0.0,
                "method": "yara",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "detected": False,
                "threat_type": "Error",
                "confidence": 0.0,
                "method": "yara",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }





