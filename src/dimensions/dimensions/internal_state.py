"""
Internal State Dimension (β) Module

Tracks and processes internal system state.
"""

import numpy as np
from typing import Optional, Dict, Any, List
from scipy.optimize import minimize


class InternalStateDimension:
    """
    Beta dimension - Internal State Processing.
    
    Monitors and processes the internal state of the intelligence system,
    including cognitive load, attention allocation, and resource usage.
    
    Attributes:
        state_capacity: Maximum state capacity
    """
    
    def __init__(self, state_capacity: float = 1.0):
        """
        Initialize the internal state dimension.
        
        Args:
            state_capacity: Maximum state capacity (0-1)
        """
        self.state_capacity = state_capacity
        self._state_embedding: Optional[np.ndarray] = None
        self._current_load = 0.0
    
    def update_state(
        self,
        cognitive_load: float,
        attention_allocation: Dict[str, float],
        resource_usage: Dict[str, float],
    ) -> Dict[str, Any]:
        """
        Update internal state with current metrics.
        
        Args:
            cognitive_load: Current cognitive load (0-1)
            attention_allocation: Attention distribution across domains
            resource_usage: Resource consumption metrics
        
        Returns:
            Dictionary with updated state
        """
        # Update current load
        self._current_load = min(1.0, cognitive_load)
        
        # Create state embedding
        embedding = self._create_state_embedding(
            cognitive_load, attention_allocation, resource_usage
        )
        
        # Calculate state metrics
        metrics = self._calculate_state_metrics(
            cognitive_load, attention_allocation, resource_usage
        )
        
        return {
            "embedding": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
            "cognitive_load": float(cognitive_load),
            "attention_allocation": attention_allocation,
            "resource_usage": resource_usage,
            "metrics": metrics,
        }
    
    def _create_state_embedding(
        self,
        cognitive_load: float,
        attention_allocation: Dict[str, float],
        resource_usage: Dict[str, float],
    ) -> np.ndarray:
        """
        Create embedding from internal state.
        
        Args:
            cognitive_load: Current cognitive load
            attention_allocation: Attention distribution
            resource_usage: Resource usage
        
        Returns:
            8D state embedding
        """
        # Create state vector from inputs
        state_vector = np.zeros(8)
        
        # Cognitive load (dimension 0)
        state_vector[0] = cognitive_load
        
        # Attention dimensions (1-5)
        attention_values = list(attention_allocation.values())
        if len(attention_values) >= 5:
            state_vector[1:6] = attention_values[:5]
        elif len(attention_values) > 0:
            # Normalize if less than 5 values
            total = sum(attention_values)
            normalized = [v / total for v in attention_values]
            state_vector[1:1+len(normalized)] = normalized
        
        # Resource dimensions (6-7)
        resource_values = list(resource_usage.values())
        if len(resource_values) >= 2:
            state_vector[6:8] = resource_values[:2]
        elif len(resource_values) > 0:
            state_vector[6] = resource_values[0]
        
        # Normalize
        norm = np.linalg.norm(state_vector)
        if norm > 0:
            state_vector = state_vector / norm
        
        return state_vector
    
    def _calculate_state_metrics(
        self,
        cognitive_load: float,
        attention_allocation: Dict[str, float],
        resource_usage: Dict[str, float],
    ) -> Dict[str, float]:
        """
        Calculate state metrics.
        
        Args:
            cognitive_load: Current cognitive load
            attention_allocation: Attention distribution
            resource_usage: Resource usage
        
        Returns:
            Dictionary of metrics
        """
        metrics = {}
        
        # Overall efficiency
        total_attention = sum(attention_allocation.values())
        metrics["total_attention"] = float(total_attention)
        
        # Attention balance
        if len(attention_allocation) > 1:
            attention_values = list(attention_allocation.values())
            mean_attention = np.mean(attention_values)
            std_attention = np.std(attention_values)
            metrics["attention_balance"] = float(1.0 - (std_attention / (mean_attention + 1e-8)))
        
        # Resource efficiency
        total_resources = sum(resource_usage.values())
        metrics["total_resources"] = float(total_resources)
        
        # State health
        health = 1.0 - cognitive_load
        metrics["state_health"] = float(health)
        
        return metrics
    
    def optimize_attention_allocation(
        self,
        current_allocation: Dict[str, float],
        target_domains: List[str],
    ) -> Dict[str, float]:
        """
        Optimize attention allocation for target domains.
        
        Args:
            current_allocation: Current attention distribution
            target_domains: Priority domains
        
        Returns:
            Optimized attention allocation
        """
        # Simple optimization: increase attention to target domains
        total_current = sum(current_allocation.values())
        
        if total_current == 0:
            return {domain: 1.0 / len(target_domains) for domain in target_domains}
        
        # Calculate current proportions
        proportions = {k: v / total_current for k, v in current_allocation.items()}
        
        # Boost target domains
        for domain in target_domains:
            if domain in proportions:
                proportions[domain] = proportions[domain] * 1.5
            else:
                # Add new domain with weight
                proportions[domain] = 0.2
        
        # Renormalize
        total = sum(proportions.values())
        if total > 0:
            proportions = {k: v / total for k, v in proportions.items()}
        
        return proportions
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current internal state.
        
        Returns:
            Current state dictionary
        """
        return {
            "type": "internal_state",
            "cognitive_load": self._current_load,
            "state_capacity": self.state_capacity,
            "utilization": self._current_load / self.state_capacity,
        }
    
    def get_embedding(self) -> Optional[np.ndarray]:
        """
        Get current state embedding.
        
        Returns:
            State embedding or None
        """
        return self._state_embedding
    
    def set_state_embedding(self, embedding: np.ndarray) -> None:
        """
        Set state embedding.
        
        Args:
            embedding: New state embedding
        """
        self._state_embedding = embedding
    
    def normalize_state(self) -> None:
        """Normalize current state."""
        if self._state_embedding is not None:
            norm = np.linalg.norm(self._state_embedding)
            if norm > 0:
                self._state_embedding = self._state_embedding / norm
    
    def __repr__(self) -> str:
        return f"InternalStateDimension(capacity={self.state_capacity:.2f})"
    
    def __str__(self) -> str:
        return self.__repr__()
