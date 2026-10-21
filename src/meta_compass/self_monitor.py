"""
Self-Monitoring Module

Handles continuous self-monitoring and oversight.
"""

import time
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class MonitorState(Enum):
    """Monitoring states."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class SelfMonitor:
    """
    Continuous self-monitoring engine.
    
    Provides ongoing oversight of the intelligence system,
    detecting issues, biases, and areas for improvement.
    
    Attributes:
        monitoring_interval: Check interval in seconds
    """
    
    def __init__(self, monitoring_interval: float = 1.0):
        """
        Initialize the self monitor.
        
        Args:
            monitoring_interval: Check interval in seconds
        """
        self.monitoring_interval = monitoring_interval
        self._state = MonitorState.ACTIVE
        self._checks: List[Dict[str, Any]] = []
        self._last_check_time: Optional[float] = None
    
    def check(
        self,
        perception: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Run a self-monitoring check on perception.
        
        Args:
            perception: Perceived input
        
        Returns:
            Check results
        """
        results = self._perform_checks(perception, perception.get("context"))
        
        # Record check
        check_record = {
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "context": perception.get("context") or {},
        }
        self._checks.append(check_record)
        
        # Update state
        if results.get("issues"):
            self._state = MonitorState.ACTIVE
        else:
            self._state = MonitorState.COMPLETED
        
        return results
    
    def identify_assumptions(
        self,
        perception: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Identify assumptions in the perception.
        
        Args:
            perception: Perceived input
        
        Returns:
            List of identified assumptions
        """
        assumptions = []
        query = perception.get("query") or ""
        
        # Extract common assumptions from query
        assumption_keywords = [
            ("assume", "Assumption detected"),
            ("believe", "Belief-based assumption"),
            ("suppose", "Supposition detected"),
            ("likely", "Probability assumption"),
        ]
        
        for keyword, label in assumption_keywords:
            if keyword.lower() in query.lower():
                assumptions.append({
                    "type": label,
                    "keyword": keyword,
                    "confidence": 0.7,
                })
        
        return assumptions
    
    def detect_blind_spots(
        self,
        perception: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Detect potential blind spots in the perception.
        
        Args:
            perception: Perceived input
        
        Returns:
            List of detected blind spots
        """
        blind_spots = []
        query = perception.get("query") or ""
        features = perception.get("features") or {}
        
        # Detect potential blind spots based on query characteristics
        if features.get("length", 0) < 10:
            blind_spots.append({
                "type": "insufficient_context",
                "description": "Query is too short for comprehensive analysis",
                "severity": "medium",
            })
        
        if not features.get("punctuation_ratio", 0) > 0:
            blind_spots.append({
                "type": "missing_structure",
                "description": "Query lacks punctuation which may affect interpretation",
                "severity": "low",
            })
        
        return blind_spots
    
    def run_check(
        self,
        system_state: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run a self-monitoring check.
        
        Args:
            system_state: Current system state
            context: Additional context
        
        Returns:
            Check results
        """
        start_time = time.time()
        
        # Perform checks
        results = self._perform_checks(system_state, context)
        
        # Record check
        check_record = {
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "duration_ms": (time.time() - start_time) * 1000,
            "context": context or {},
        }
        self._checks.append(check_record)
        
        # Update state
        if results.get("issues"):
            self._state = MonitorState.ACTIVE
        else:
            self._state = MonitorState.COMPLETED
        
        return results
    
    def _perform_checks(
        self,
        system_state: Dict[str, Any],
        context: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Perform self-monitoring checks.
        
        Args:
            system_state: Current system state
            context: Additional context
        
        Returns:
            Check results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
            "warnings": [],
            "oversight_score": 0.9,
        }
        
        # Consistency check
        consistency = self._check_consistency(system_state)
        results["checks"]["consistency"] = consistency
        
        # Bias detection
        bias = self._detect_bias(system_state, context)
        results["checks"]["bias"] = bias
        
        # Resource check
        resources = self._check_resources(system_state)
        results["checks"]["resources"] = resources
        
        # Compile issues and warnings
        if not consistency.get("passed"):
            results["issues"].extend(consistency.get("issues", []))
        
        if not bias.get("passed"):
            results["issues"].extend(bias.get("issues", []))
        
        if not resources.get("passed"):
            results["warnings"].extend(resources.get("warnings", []))
        
        return results
    
    def _check_consistency(
        self,
        system_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Check system consistency.
        
        Args:
            system_state: Current state
        
        Returns:
            Consistency check results
        """
        issues = []
        
        # Check for contradictory states
        state_values = system_state.get("values", {})
        if state_values:
            # Simple consistency check (placeholder)
            for key, value in state_values.items():
                if value < 0 or value > 1:
                    issues.append(f"Invalid value for {key}: {value}")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
        }
    
    def _detect_bias(
        self,
        system_state: Dict[str, Any],
        context: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Detect potential biases.
        
        Args:
            system_state: Current state
            context: Additional context
        
        Returns:
            Bias detection results
        """
        issues = []
        
        # Check for selection bias (placeholder)
        if context:
            sample_size = context.get("sample_size", 0)
            if sample_size < 10:
                issues.append("Small sample size may indicate selection bias")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
        }
    
    def _check_resources(
        self,
        system_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Check resource usage.
        
        Args:
            system_state: Current state
        
        Returns:
            Resource check results
        """
        warnings = []
        
        # Check memory usage (placeholder)
        memory = system_state.get("memory_usage", 0)
        if memory > 0.9:
            warnings.append("High memory usage detected")
        
        # Check CPU usage (placeholder)
        cpu = system_state.get("cpu_usage", 0)
        if cpu > 0.9:
            warnings.append("High CPU usage detected")
        
        return {
            "passed": len(warnings) == 0,
            "warnings": warnings,
        }
    
    def get_monitoring_report(self) -> Dict[str, Any]:
        """
        Get monitoring report.
        
        Returns:
            Monitoring report
        """
        if not self._checks:
            return {"error": "No checks performed"}
        
        latest_check = self._checks[-1]
        
        return {
            "state": self._state.value,
            "last_check": latest_check.get("timestamp"),
            "checks_count": len(self._checks),
            "latest_results": latest_check.get("results"),
        }
    
    def pause(self) -> None:
        """Pause monitoring."""
        self._state = MonitorState.PAUSED
    
    def resume(self) -> None:
        """Resume monitoring."""
        self._state = MonitorState.ACTIVE
    
    def clear_checks(self) -> None:
        """Clear check history."""
        self._checks.clear()
    
    def __repr__(self) -> str:
        return f"SelfMonitor(state={self._state.value}, checks={len(self._checks)})"
    
    def __str__(self) -> str:
        return self.__repr__()
