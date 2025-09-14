"""
Simplified Social Engineering Detector for Testing
Works without external dependencies
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any

class SocialEngineeringDetector:
    """Simplified social engineering detector"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.urgency_keywords = [
            "urgent", "immediately", "asap", "expires", "limited time",
            "act now", "don't wait", "last chance", "final notice"
        ]
        self.authority_keywords = [
            "bank", "paypal", "amazon", "microsoft", "apple", "google",
            "irs", "fbi", "police", "court", "legal", "official"
        ]
        self.suspicious_urls = [
            "bit.ly", "tinyurl.com", "goo.gl", "t.co", "short.link"
        ]
        self.phishing_indicators = [
            "verify account", "update information", "suspended account",
            "security breach", "unusual activity", "click here"
        ]
    
    def detect_social_engineering(self, data: Dict) -> Dict:
        """Comprehensive social engineering detection"""
        try:
            threats_detected = []
            threat_types = []
            risk_score = 0.0
            
            # Analyze email content
            email_data = data.get("email", {})
            if email_data:
                email_result = self._analyze_email(email_data)
                if email_result["suspicious"]:
                    threats_detected.append({
                        "type": "Suspicious Email",
                        "details": email_result,
                        "risk_level": email_result["risk_level"]
                    })
                    threat_types.append("Suspicious Email")
                    risk_score += email_result["risk_score"]
            
            # Analyze URLs
            urls = data.get("urls", [])
            for url in urls:
                url_result = self._analyze_url(url)
                if url_result["suspicious"]:
                    threats_detected.append({
                        "type": "Suspicious URL",
                        "details": url_result,
                        "risk_level": url_result["risk_level"]
                    })
                    threat_types.append("Suspicious URL")
                    risk_score += url_result["risk_score"]
            
            # Analyze general content
            content = data.get("content", "")
            if content:
                content_result = self._analyze_content(content)
                if content_result["suspicious"]:
                    threats_detected.append({
                        "type": "Suspicious Content",
                        "details": content_result,
                        "risk_level": content_result["risk_level"]
                    })
                    threat_types.append("Suspicious Content")
                    risk_score += content_result["risk_score"]
            
            # Determine overall threat level
            if risk_score >= 0.6:
                threat_level = "high"
            elif risk_score >= 0.3:
                threat_level = "medium"
            else:
                threat_level = "low"
            
            return {
                "threats_detected": threats_detected,
                "threat_types": threat_types,
                "threat_level": threat_level,
                "overall_risk_score": min(10.0, risk_score * 10),
                "timestamp": datetime.now().isoformat(),
                "analysis_summary": {
                    "email_analyzed": bool(email_data),
                    "urls_analyzed": len(urls),
                    "content_analyzed": bool(content)
                }
            }
            
        except Exception as e:
            return {
                "threats_detected": [],
                "threat_types": [],
                "threat_level": "error",
                "overall_risk_score": 0.0,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _analyze_email(self, email_data: Dict) -> Dict:
        """Analyze email for social engineering indicators"""
        try:
            content = email_data.get("content", "").lower()
            subject = email_data.get("subject", "").lower()
            sender = email_data.get("sender", "").lower()
            
            risk_score = 0.0
            indicators = []
            
            # Check for urgency
            urgency_count = sum(1 for keyword in self.urgency_keywords if keyword in content or keyword in subject)
            if urgency_count > 0:
                indicators.append(f"Urgency detected ({urgency_count} keywords)")
                risk_score += 0.2
            
            # Check for authority
            authority_count = sum(1 for keyword in self.authority_keywords if keyword in content or keyword in subject)
            if authority_count > 0:
                indicators.append(f"Authority claimed ({authority_count} keywords)")
                risk_score += 0.2
            
            # Check for phishing indicators
            phishing_count = sum(1 for indicator in self.phishing_indicators if indicator in content)
            if phishing_count > 0:
                indicators.append(f"Phishing indicators ({phishing_count} found)")
                risk_score += 0.3
            
            # Check sender domain
            if "@" in sender:
                domain = sender.split("@")[1]
                if self._is_suspicious_domain(domain):
                    indicators.append("Suspicious sender domain")
                    risk_score += 0.2
            
            suspicious = risk_score > 0.3
            risk_level = "high" if risk_score > 0.6 else "medium" if risk_score > 0.3 else "low"
            
            return {
                "suspicious": suspicious,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "indicators": indicators,
                "urgency_score": urgency_count,
                "authority_score": authority_count,
                "phishing_score": phishing_count
            }
            
        except Exception as e:
            return {
                "suspicious": False,
                "risk_score": 0.0,
                "risk_level": "error",
                "error": str(e)
            }
    
    def _analyze_url(self, url: str) -> Dict:
        """Analyze URL for social engineering indicators"""
        try:
            url_lower = url.lower()
            risk_score = 0.0
            indicators = []
            
            # Check for shortened URLs
            if any(shortener in url_lower for shortener in self.suspicious_urls):
                indicators.append("Shortened URL detected")
                risk_score += 0.3
            
            # Check for typosquatting patterns
            if self._is_typosquatting(url):
                indicators.append("Possible typosquatting")
                risk_score += 0.4
            
            # Check for suspicious TLD
            if url_lower.endswith(('.tk', '.ml', '.ga', '.cf')):
                indicators.append("Suspicious TLD")
                risk_score += 0.2
            
            suspicious = risk_score > 0.3
            risk_level = "high" if risk_score > 0.6 else "medium" if risk_score > 0.3 else "low"
            
            return {
                "suspicious": suspicious,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "indicators": indicators,
                "url": url
            }
            
        except Exception as e:
            return {
                "suspicious": False,
                "risk_score": 0.0,
                "risk_level": "error",
                "error": str(e)
            }
    
    def _analyze_content(self, content: str) -> Dict:
        """Analyze general content for social engineering"""
        try:
            content_lower = content.lower()
            risk_score = 0.0
            indicators = []
            
            # Check for urgency
            urgency_count = sum(1 for keyword in self.urgency_keywords if keyword in content_lower)
            if urgency_count > 0:
                indicators.append(f"Urgency detected ({urgency_count} keywords)")
                risk_score += 0.2
            
            # Check for authority
            authority_count = sum(1 for keyword in self.authority_keywords if keyword in content_lower)
            if authority_count > 0:
                indicators.append(f"Authority claimed ({authority_count} keywords)")
                risk_score += 0.2
            
            # Check for phishing indicators
            phishing_count = sum(1 for indicator in self.phishing_indicators if indicator in content_lower)
            if phishing_count > 0:
                indicators.append(f"Phishing indicators ({phishing_count} found)")
                risk_score += 0.3
            
            suspicious = risk_score > 0.3
            risk_level = "high" if risk_score > 0.6 else "medium" if risk_score > 0.3 else "low"
            
            return {
                "suspicious": suspicious,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "indicators": indicators,
                "urgency_score": urgency_count,
                "authority_score": authority_count,
                "phishing_score": phishing_count
            }
            
        except Exception as e:
            return {
                "suspicious": False,
                "risk_score": 0.0,
                "risk_level": "error",
                "error": str(e)
            }
    
    def _is_suspicious_domain(self, domain: str) -> bool:
        """Check if domain is suspicious"""
        suspicious_domains = [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com"  # Common spoofed domains
        ]
        return domain in suspicious_domains
    
    def _is_typosquatting(self, url: str) -> bool:
        """Simple typosquatting detection"""
        # This is a simplified version - in reality, you'd use more sophisticated algorithms
        suspicious_patterns = [
            "goog1e", "amaz0n", "paypa1", "micr0soft", "app1e"
        ]
        return any(pattern in url.lower() for pattern in suspicious_patterns)





