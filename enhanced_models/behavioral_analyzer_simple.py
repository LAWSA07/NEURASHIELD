"""
Simplified Behavioral Analyzer for Testing
Works without external dependencies
"""

import os
import json
import psutil
from datetime import datetime
from typing import Dict, List, Any

class BehavioralAnalyzer:
    """Simplified behavioral analysis for zero-day and fileless threats"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.suspicious_processes = [
            "powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe",
            "mshta.exe", "regsvr32.exe", "rundll32.exe"
        ]
        self.suspicious_commands = [
            "DownloadString", "Invoke-Expression", "IEX", "Invoke-WebRequest",
            "net user", "net group", "wmic", "schtasks"
        ]
    
    def collect_behavioral_data(self) -> Dict:
        """Collect current system behavioral data"""
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "processes": [],
                "network_connections": [],
                "system_metrics": {}
            }
            
            # Collect process information
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    data["processes"].append({
                        "pid": proc_info['pid'],
                        "name": proc_info['name'],
                        "cmdline": proc_info['cmdline'],
                        "cpu_percent": proc_info['cpu_percent'],
                        "memory_percent": proc_info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Collect network connections
            try:
                connections = psutil.net_connections(kind='inet')
                for conn in connections[:50]:  # Limit to first 50 connections
                    data["network_connections"].append({
                        "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                        "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                        "status": conn.status,
                        "pid": conn.pid
                    })
            except:
                pass
            
            # Collect system metrics
            try:
                data["system_metrics"] = {
                    "cpu_percent": psutil.cpu_percent(interval=1),
                    "memory_percent": psutil.virtual_memory().percent,
                    "disk_usage": psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
                }
            except:
                pass
            
            return data
            
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "processes": [],
                "network_connections": [],
                "system_metrics": {}
            }
    
    def analyze_behavior(self, data: Dict) -> Dict:
        """Analyze behavioral data for threats"""
        try:
            threats_detected = []
            threat_types = []
            risk_score = 0.0
            
            # Analyze processes
            suspicious_processes = []
            for proc in data.get("processes", []):
                if proc["name"].lower() in [p.lower() for p in self.suspicious_processes]:
                    suspicious_processes.append(proc)
                    risk_score += 0.2
            
            if suspicious_processes:
                threats_detected.append({
                    "type": "Suspicious Process",
                    "details": suspicious_processes,
                    "risk_level": "medium"
                })
                threat_types.append("Suspicious Process")
            
            # Analyze command lines
            suspicious_commands = []
            for proc in data.get("processes", []):
                cmdline = " ".join(proc.get("cmdline", []))
                for cmd in self.suspicious_commands:
                    if cmd.lower() in cmdline.lower():
                        suspicious_commands.append({
                            "process": proc["name"],
                            "command": cmd,
                            "full_cmdline": cmdline
                        })
                        risk_score += 0.3
            
            if suspicious_commands:
                threats_detected.append({
                    "type": "Suspicious Commands",
                    "details": suspicious_commands,
                    "risk_level": "high"
                })
                threat_types.append("Suspicious Commands")
            
            # Analyze network connections
            suspicious_connections = []
            for conn in data.get("network_connections", []):
                if conn.get("remote_address") and ":" in conn["remote_address"]:
                    port = int(conn["remote_address"].split(":")[1])
                    if port in [4444, 8080, 9999, 1337]:  # Common malware ports
                        suspicious_connections.append(conn)
                        risk_score += 0.1
            
            if suspicious_connections:
                threats_detected.append({
                    "type": "Suspicious Network",
                    "details": suspicious_connections,
                    "risk_level": "medium"
                })
                threat_types.append("Suspicious Network")
            
            # Determine overall threat level
            if risk_score >= 0.7:
                threat_level = "high"
            elif risk_score >= 0.4:
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
                    "suspicious_processes": len(suspicious_processes),
                    "suspicious_commands": len(suspicious_commands),
                    "suspicious_connections": len(suspicious_connections)
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





