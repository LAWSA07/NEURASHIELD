"""
Simplified Ensemble Detector for Testing
Works without external dependencies
"""

import json
from datetime import datetime
from typing import Dict, List, Any

# Import simplified modules
try:
    from .signature_detector_simple import SignatureDetector
    from .file_analyzer_simple import FileAnalyzer
    from .behavioral_analyzer_simple import BehavioralAnalyzer
    from .encrypted_detector_simple import EncryptedThreatDetector
    from .social_engineering_detector_simple import SocialEngineeringDetector
except ImportError:
    # Fallback imports
    from enhanced_models.signature_detector_simple import SignatureDetector
    from enhanced_models.file_analyzer_simple import FileAnalyzer
    from enhanced_models.behavioral_analyzer_simple import BehavioralAnalyzer
    from enhanced_models.encrypted_detector_simple import EncryptedThreatDetector
    from enhanced_models.social_engineering_detector_simple import SocialEngineeringDetector

class EnhancedThreatDetector:
    """Simplified ensemble threat detection class"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        
        # Initialize all detection modules
        self.signature_detector = SignatureDetector(self.config.get('signature', {}))
        self.file_analyzer = FileAnalyzer(self.config.get('file_analysis', {}))
        self.behavioral_analyzer = BehavioralAnalyzer(self.config.get('behavioral', {}))
        self.encrypted_detector = EncryptedThreatDetector(self.config.get('encrypted', {}))
        self.social_engineering_detector = SocialEngineeringDetector(self.config.get('social_engineering', {}))
        
        # Detection weights
        self.detection_weights = {
            'signature': 0.25,
            'file_analysis': 0.20,
            'behavioral': 0.20,
            'encrypted': 0.15,
            'social_engineering': 0.20
        }
    
    def detect_threats(self, data: Dict) -> Dict:
        """Comprehensive threat detection using all modules"""
        try:
            results = {
                "timestamp": datetime.now().isoformat(),
                "threats_detected": [],
                "threat_types": [],
                "overall_risk_score": 0.0,
                "threat_level": "low",
                "confidence": 0.0,
                "module_results": {}
            }
            
            # Run signature detection if file path provided
            if "file_path" in data:
                try:
                    sig_result = self.signature_detector.detect_threats(data["file_path"])
                    results["module_results"]["signature"] = sig_result
                    
                    if sig_result.get("detected"):
                        results["threats_detected"].append({
                            "type": "Signature Match",
                            "details": sig_result,
                            "module": "signature"
                        })
                        results["threat_types"].append("Signature Match")
                except Exception as e:
                    results["module_results"]["signature"] = {"error": str(e)}
            
            # Run file analysis if file path provided
            if "file_path" in data:
                try:
                    file_result = self.file_analyzer.predict(data["file_path"])
                    results["module_results"]["file_analysis"] = file_result
                    
                    if file_result.get("prediction") in ["malicious", "suspicious"]:
                        results["threats_detected"].append({
                            "type": "File-based Threat",
                            "details": file_result,
                            "module": "file_analysis"
                        })
                        results["threat_types"].append("File-based Threat")
                except Exception as e:
                    results["module_results"]["file_analysis"] = {"error": str(e)}
            
            # Run behavioral analysis if system data provided
            if "system_data" in data:
                try:
                    behavioral_data = self.behavioral_analyzer.collect_behavioral_data()
                    behavioral_result = self.behavioral_analyzer.analyze_behavior(behavioral_data)
                    results["module_results"]["behavioral"] = behavioral_result
                    
                    if behavioral_result.get("threats_detected"):
                        results["threats_detected"].extend(behavioral_result["threats_detected"])
                        results["threat_types"].extend(behavioral_result.get("threat_types", []))
                except Exception as e:
                    results["module_results"]["behavioral"] = {"error": str(e)}
            
            # Run encrypted threat detection if network data provided
            if "network_data" in data:
                try:
                    encrypted_result = self.encrypted_detector.detect_encrypted_threats(data["network_data"])
                    results["module_results"]["encrypted"] = encrypted_result
                    
                    if encrypted_result.get("threats_detected"):
                        results["threats_detected"].extend(encrypted_result["threats_detected"])
                        results["threat_types"].extend(encrypted_result.get("threat_types", []))
                except Exception as e:
                    results["module_results"]["encrypted"] = {"error": str(e)}
            
            # Run social engineering detection if communication data provided
            if "communication_data" in data:
                try:
                    se_result = self.social_engineering_detector.detect_social_engineering(data["communication_data"])
                    results["module_results"]["social_engineering"] = se_result
                    
                    if se_result.get("threats_detected"):
                        results["threats_detected"].extend(se_result["threats_detected"])
                        results["threat_types"].extend(se_result.get("threat_types", []))
                except Exception as e:
                    results["module_results"]["social_engineering"] = {"error": str(e)}
            
            # Calculate ensemble decision
            ensemble_decision = self._calculate_ensemble_decision(results)
            results.update(ensemble_decision)
            
            return results
            
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "threats_detected": [],
                "threat_types": [],
                "overall_risk_score": 0.0,
                "threat_level": "error",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _calculate_ensemble_decision(self, results: Dict) -> Dict:
        """Calculate final ensemble decision"""
        try:
            total_risk_score = 0.0
            total_confidence = 0.0
            threat_count = len(results["threats_detected"])
            
            # Calculate weighted scores from each module
            for module_name, weight in self.detection_weights.items():
                module_result = results["module_results"].get(module_name, {})
                
                if "error" not in module_result:
                    # Extract risk score from module result
                    if module_name == "signature":
                        if module_result.get("detected"):
                            total_risk_score += weight * module_result.get("confidence", 0.0) * 10
                            total_confidence += weight * module_result.get("confidence", 0.0)
                    
                    elif module_name == "file_analysis":
                        if module_result.get("prediction") in ["malicious", "suspicious"]:
                            total_risk_score += weight * module_result.get("confidence", 0.0) * 10
                            total_confidence += weight * module_result.get("confidence", 0.0)
                    
                    elif module_name in ["behavioral", "encrypted", "social_engineering"]:
                        risk_score = module_result.get("overall_risk_score", 0.0)
                        total_risk_score += weight * risk_score
                        total_confidence += weight * (risk_score / 10.0)
            
            # Determine threat level
            if total_risk_score >= 7.0:
                threat_level = "high"
            elif total_risk_score >= 4.0:
                threat_level = "medium"
            else:
                threat_level = "low"
            
            # Calculate final confidence
            final_confidence = min(1.0, total_confidence)
            
            return {
                "overall_risk_score": min(10.0, total_risk_score),
                "threat_level": threat_level,
                "confidence": final_confidence,
                "threat_count": threat_count
            }
            
        except Exception as e:
            return {
                "overall_risk_score": 0.0,
                "threat_level": "error",
                "confidence": 0.0,
                "threat_count": 0,
                "error": str(e)
            }
    
    def detect_advanced_threats(self, data: Dict) -> Dict:
        """Detect advanced threats using specialized methods"""
        try:
            advanced_threats = []
            
            # Check for zero-day indicators
            if "system_data" in data:
                behavioral_data = self.behavioral_analyzer.collect_behavioral_data()
                behavioral_result = self.behavioral_analyzer.analyze_behavior(behavioral_data)
                
                if behavioral_result.get("threat_level") == "high":
                    advanced_threats.append({
                        "type": "Zero-day Exploit",
                        "confidence": 0.7,
                        "indicators": behavioral_result.get("threats_detected", [])
                    })
            
            # Check for fileless malware
            if "system_data" in data:
                behavioral_data = self.behavioral_analyzer.collect_behavioral_data()
                for proc in behavioral_data.get("processes", []):
                    if proc.get("name", "").lower() in ["powershell.exe", "wscript.exe", "cscript.exe"]:
                        advanced_threats.append({
                            "type": "Fileless Malware",
                            "confidence": 0.6,
                            "indicators": [{"process": proc["name"], "cmdline": proc.get("cmdline", [])}]
                        })
            
            # Check for encrypted threats
            if "network_data" in data:
                encrypted_result = self.encrypted_detector.detect_encrypted_threats(data["network_data"])
                if encrypted_result.get("threat_level") == "high":
                    advanced_threats.append({
                        "type": "Encrypted Malware",
                        "confidence": 0.8,
                        "indicators": encrypted_result.get("threats_detected", [])
                    })
            
            return {
                "advanced_threats": advanced_threats,
                "timestamp": datetime.now().isoformat(),
                "threat_count": len(advanced_threats)
            }
            
        except Exception as e:
            return {
                "advanced_threats": [],
                "timestamp": datetime.now().isoformat(),
                "threat_count": 0,
                "error": str(e)
            }
    
    def update_detection_weights(self, new_weights: Dict):
        """Update detection module weights"""
        try:
            # Normalize weights
            total_weight = sum(new_weights.values())
            if total_weight > 0:
                self.detection_weights = {k: v/total_weight for k, v in new_weights.items()}
            else:
                # Reset to default weights
                self.detection_weights = {
                    'signature': 0.25,
                    'file_analysis': 0.20,
                    'behavioral': 0.20,
                    'encrypted': 0.15,
                    'social_engineering': 0.20
                }
        except Exception as e:
            print(f"Error updating weights: {e}")
