"""
Simplified Encrypted Threat Detector for Testing
Works without external dependencies
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any

class EncryptedThreatDetector:
    """Simplified encrypted threat detector"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.suspicious_domains = [
            "malware.com", "evil.org", "bad.net", "suspicious.info"
        ]
        self.suspicious_ports = [4444, 8080, 9999, 1337, 31337]
        self.dga_patterns = [
            r'[a-z]{8,}\.com',  # Random long domains
            r'[a-z]{4,}\d{4,}\.net',  # Mixed alphanumeric
        ]
    
    def detect_encrypted_threats(self, network_data: Dict) -> Dict:
        """Detect encrypted threats from network data"""
        try:
            threats_detected = []
            threat_types = []
            risk_score = 0.0
            
            # Analyze TLS hosts
            tls_hosts = network_data.get("tls_hosts", [])
            for host in tls_hosts:
                if self._is_suspicious_domain(host):
                    threats_detected.append({
                        "type": "Suspicious TLS Host",
                        "details": {"host": host},
                        "risk_level": "medium"
                    })
                    threat_types.append("Suspicious TLS Host")
                    risk_score += 0.2
            
            # Analyze DNS queries
            dns_queries = network_data.get("dns_queries", [])
            for query in dns_queries:
                if self._is_dga_domain(query):
                    threats_detected.append({
                        "type": "DGA Domain",
                        "details": {"domain": query},
                        "risk_level": "high"
                    })
                    threat_types.append("DGA Domain")
                    risk_score += 0.3
            
            # Analyze connections
            connections = network_data.get("connections", [])
            for conn in connections:
                if self._is_suspicious_connection(conn):
                    threats_detected.append({
                        "type": "Suspicious Connection",
                        "details": conn,
                        "risk_level": "medium"
                    })
                    threat_types.append("Suspicious Connection")
                    risk_score += 0.1
            
            # Determine threat level
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
                    "tls_hosts_analyzed": len(tls_hosts),
                    "dns_queries_analyzed": len(dns_queries),
                    "connections_analyzed": len(connections)
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
    
    def detect_c2_communication(self, network_data: Dict) -> Dict:
        """Detect command and control communication"""
        try:
            c2_indicators = []
            risk_score = 0.0
            
            # Check for beaconing patterns
            connections = network_data.get("connections", [])
            if len(connections) > 10:  # Many connections might indicate beaconing
                c2_indicators.append("High connection count")
                risk_score += 0.2
            
            # Check for suspicious ports
            for conn in connections:
                if isinstance(conn, dict) and "port" in conn:
                    if conn["port"] in self.suspicious_ports:
                        c2_indicators.append(f"Suspicious port: {conn['port']}")
                        risk_score += 0.3
            
            # Check for data exfiltration patterns
            dns_queries = network_data.get("dns_queries", [])
            if len(dns_queries) > 20:  # Many DNS queries might indicate data exfiltration
                c2_indicators.append("High DNS query count")
                risk_score += 0.2
            
            return {
                "c2_detected": len(c2_indicators) > 0,
                "indicators": c2_indicators,
                "risk_score": min(10.0, risk_score * 10),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "c2_detected": False,
                "indicators": [],
                "risk_score": 0.0,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _is_suspicious_domain(self, domain: str) -> bool:
        """Check if domain is suspicious"""
        domain_lower = domain.lower()
        return any(suspicious in domain_lower for suspicious in self.suspicious_domains)
    
    def _is_dga_domain(self, domain: str) -> bool:
        """Check if domain matches DGA patterns"""
        for pattern in self.dga_patterns:
            if re.search(pattern, domain.lower()):
                return True
        return False
    
    def _is_suspicious_connection(self, conn: Dict) -> bool:
        """Check if connection is suspicious"""
        if isinstance(conn, dict):
            port = conn.get("port", 0)
            return port in self.suspicious_ports
        return False





