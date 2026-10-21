"""
Action/Output Dimension (θ) Module

Handles action generation and output formatting.
"""

import numpy as np
from typing import Optional, Dict, Any, List
from enum import Enum


class ActionPriority(Enum):
    """Action priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class ActionOutputDimension:
    """
    Theta dimension - Action/Output Processing.
    
    Manages action generation, output formatting,
    and response generation.
    
    Attributes:
        default_priority: Default action priority
    """
    
    def __init__(self, default_priority: ActionPriority = ActionPriority.MEDIUM):
        """
        Initialize the action output dimension.
        
        Args:
            default_priority: Default action priority
        """
        self.default_priority = default_priority
        self._action_embedding: Optional[np.ndarray] = None
        self._output_template: Optional[Dict[str, str]] = None
    
    def generate_action(
        self,
        context: Dict[str, Any],
        priority: Optional[ActionPriority] = None,
    ) -> Dict[str, Any]:
        """
        Generate an action based on context.
        
        Args:
            context: Context for action generation
            priority: Optional action priority
        
        Returns:
            Dictionary with action details
        """
        effective_priority = priority or self.default_priority
        
        # Create action embedding
        embedding = self._create_action_embedding(context, effective_priority)
        
        # Generate action details
        action = self._generate_action_details(context, effective_priority)
        
        return {
            "embedding": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
            "action": action,
        }
    
    def _create_action_embedding(
        self,
        context: Dict[str, Any],
        priority: ActionPriority,
    ) -> np.ndarray:
        """
        Create embedding from action context.
        
        Args:
            context: Context data
            priority: Action priority
        
        Returns:
            8D action embedding
        """
        embedding = np.zeros(8)
        
        # Priority score (dimension 0)
        priority_scores = {
            ActionPriority.LOW: 0.25,
            ActionPriority.MEDIUM: 0.5,
            ActionPriority.HIGH: 0.75,
            ActionPriority.CRITICAL: 1.0,
        }
        embedding[0] = priority_scores[priority]
        
        # Context features (dimensions 1-7)
        # We need exactly 7 features for dimensions 1-7
        context_features = []
        feature_idx = 0
        
        for key, value in context.items():
            if feature_idx >= 7:
                break
            if isinstance(value, (int, float)):
                context_features.append(min(1.0, abs(value) / 10))
            elif isinstance(value, str):
                context_features.append(len(value) / 100)
            else:
                context_features.append(0.5)
            feature_idx += 1
        
        # Fill remaining dimensions with 0.5
        while len(context_features) < 7:
            context_features.append(0.5)
        
        embedding[1:8] = np.array(context_features[:7])
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def _generate_action_details(
        self,
        context: Dict[str, Any],
        priority: ActionPriority,
    ) -> Dict[str, Any]:
        """
        Generate action details.
        
        Args:
            context: Context data
            priority: Action priority
        
        Returns:
            Action details dictionary
        """
        return {
            "priority": priority.value,
            "context": context,
            "action_type": "generate_response",
            "metadata": {
                "source": "action_output_dimension",
                "confidence": 0.8,
            },
        }
    
    def format_output(
        self,
        data: Dict[str, Any],
        format_type: str = "json",
    ) -> str:
        """
        Format output data.
        
        Args:
            data: Data to format
            format_type: Output format type
        
        Returns:
            Formatted string
        """
        if format_type == "json":
            import json
            return json.dumps(data, indent=2)
        elif format_type == "text":
            return str(data)
        else:
            return json.dumps(data)
    
    def get_embedding(self) -> Optional[np.ndarray]:
        """
        Get current action embedding.
        
        Returns:
            Action embedding or None
        """
        return self._action_embedding
    
    def set_embedding(self, embedding: np.ndarray) -> None:
        """
        Set action embedding.
        
        Args:
            embedding: New embedding
        """
        self._action_embedding = embedding
    
    def normalize(self) -> None:
        """Normalize current action embedding."""
        if self._action_embedding is not None:
            norm = np.linalg.norm(self._action_embedding)
            if norm > 0:
                self._action_embedding = self._action_embedding / norm
    
    def __repr__(self) -> str:
        return f"ActionOutputDimension(priority={self.default_priority.value})"
    
    def __str__(self) -> str:
        return self.__repr__()
