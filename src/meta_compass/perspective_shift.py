"""
Perspective Shift Core Module

Handles perspective transformation and reframing.
"""

import numpy as np
from typing import Optional, Dict, Any, List
from enum import Enum


class PerspectiveType(Enum):
    """Types of perspectives for reframing."""
    OPTIMISTIC = "optimistic"
    PESSIMISTIC = "pessimistic"
    REALISTIC = "realistic"
    ALTERNATIVE = "alternative"
    CRITICAL = "critical"
    CREATIVE = "creative"
    SYSTEMIC = "systemic"
    TEMPORAL = "temporal"


class PerspectiveShiftCore:
    """
    Core perspective shifting and reframing engine.
    
    Enables viewing problems and ideas from multiple perspectives,
    facilitating creative insight and bias mitigation.
    
    Attributes:
        active_perspectives: Set of currently active perspectives
    """
    
    def __init__(self):
        """Initialize the perspective shift core."""
        self.active_perspectives: List[PerspectiveType] = []
        self._perspective_weights: Dict[PerspectiveType, float] = {}
    
    def shift_perspective(
        self,
        content: str,
        target_perspective: PerspectiveType,
    ) -> Dict[str, Any]:
        """
        Shift perspective on content.
        
        Args:
            content: Original content
            target_perspective: Target perspective
        
        Returns:
            Dictionary with shifted content
        """
        # Apply perspective transformation
        shifted_content = self._transform_content(content, target_perspective)
        
        # Update active perspectives
        if target_perspective not in self.active_perspectives:
            self.active_perspectives.append(target_perspective)
        
        # Set weight
        self._perspective_weights[target_perspective] = 1.0
        
        return {
            "original": content,
            "shifted": shifted_content,
            "perspective": target_perspective.value,
        }
    
    def _transform_content(
        self,
        content: str,
        perspective: PerspectiveType,
    ) -> str:
        """
        Transform content to target perspective.
        
        Args:
            content: Original content
            perspective: Target perspective
        
        Returns:
            Transformed content
        """
        # Placeholder transformations
        transformations = {
            PerspectiveType.OPTIMISTIC: self._optimistic_transform,
            PerspectiveType.PESSIMISTIC: self._pessimistic_transform,
            PerspectiveType.REALISTIC: self._realistic_transform,
            PerspectiveType.ALTERNATIVE: self._alternative_transform,
            PerspectiveType.CRITICAL: self._critical_transform,
            PerspectiveType.CREATIVE: self._creative_transform,
            PerspectiveType.SYSTEMIC: self._systemic_transform,
            PerspectiveType.TEMPORAL: self._temporal_transform,
        }
        
        transform_func = transformations.get(perspective, lambda c, p: c)
        return transform_func(content, perspective)
    
    def _optimistic_transform(self, content: str, perspective: PerspectiveType) -> str:
        """Optimistic transformation."""
        return f"[Optimistic View] {content} presents significant opportunities"
    
    def _pessimistic_transform(self, content: str, perspective: PerspectiveType) -> str:
        """Pessimistic transformation."""
        return f"[Pessimistic View] {content} reveals potential challenges"
    
    def _realistic_transform(self, content: str, perspective: PerspectiveType) -> str:
        """Realistic transformation."""
        return f"[Realistic View] {content} requires balanced assessment"
    
    def _alternative_transform(self, content: str, perspective: PerspectiveType) -> str:
        """Alternative transformation."""
        return f"[Alternative View] {content} could be approached differently"
    
    def _critical_transform(self, content: str, perspective: PerspectiveType) -> str:
        """Critical transformation."""
        return f"[Critical View] {content} needs scrutiny for validity"
    
    def _creative_transform(self, content: str, perspective: PerspectiveType) -> str:
        """Creative transformation."""
        return f"[Creative View] {content} inspires innovative approaches"
    
    def _systemic_transform(self, content: str, perspective: PerspectiveType) -> str:
        """Systemic transformation."""
        return f"[Systemic View] {content} connects to broader patterns"
    
    def _temporal_transform(self, content: str, perspective: PerspectiveType) -> str:
        """Temporal transformation."""
        return f"[Temporal View] {content} evolves over time"
    
    def multi_perspective_analysis(
        self,
        content: str,
        perspectives: Optional[List[PerspectiveType]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze content from multiple perspectives.
        
        Args:
            content: Content to analyze
            perspectives: List of perspectives (uses all if None)
        
        Returns:
            Dictionary with multi-perspective analysis
        """
        effective_perspectives = perspectives or self.active_perspectives
        
        if not effective_perspectives:
            return {"error": "No perspectives defined"}
        
        analyses = {}
        for perspective in effective_perspectives:
            result = self.shift_perspective(content, perspective)
            analyses[perspective.value] = result["shifted"]
        
        return {
            "content": content,
            "perspectives": analyses,
            "count": len(analyses),
        }
    
    def get_perspective_weights(self) -> Dict[PerspectiveType, float]:
        """
        Get current perspective weights.
        
        Returns:
            Dictionary of perspective weights
        """
        return self._perspective_weights.copy()
    
    def set_perspective_weight(
        self,
        perspective: PerspectiveType,
        weight: float,
    ) -> None:
        """
        Set weight for a perspective.
        
        Args:
            perspective: Perspective to weight
            weight: Weight value (0-1)
        """
        self._perspective_weights[perspective] = max(0.0, min(1.0, weight))
    
    def clear_perspectives(self) -> None:
        """Clear all active perspectives."""
        self.active_perspectives.clear()
        self._perspective_weights.clear()
    
    def __repr__(self) -> str:
        return f"PerspectiveShiftCore(active={len(self.active_perspectives)})"
    
    def analyze(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze perception from multiple perspectives.
        
        Args:
            perception: Perception data
        
        Returns:
            Multi-perspective analysis
        """
        query = perception.get("query") or ""
        
        if not query:
            return {"error": "No query provided"}
        
        # Analyze from multiple perspectives
        perspectives = [
            PerspectiveType.OPTIMISTIC,
            PerspectiveType.PESSIMISTIC,
            PerspectiveType.REALISTIC,
            PerspectiveType.ALTERNATIVE,
        ]
        
        analyses = {}
        for perspective in perspectives:
            result = self.shift_perspective(query, perspective)
            analyses[perspective.value] = result["shifted"]
        
        # Calculate oversight score based on perspective diversity
        oversight_score = min(1.0, len(analyses) * 0.25)
        
        return {
            "query": query,
            "perspectives": analyses,
            "count": len(analyses),
            "oversight_score": oversight_score,
        }
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"PerspectiveShiftCore(active={len(self.active_perspectives)})"
