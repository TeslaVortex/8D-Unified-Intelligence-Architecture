"""
Social/Cultural Dimension (ζ) Module

Processes social and cultural context.
"""

import numpy as np
from typing import Optional, Dict, Any, List


class SocialDimension:
    """
    Zeta dimension - Social/Cultural Processing.
    
    Handles social context, cultural patterns,
    and interpersonal dynamics.
    
    Attributes:
        cultural_sensitivity: Cultural awareness level
    """
    
    def __init__(self, cultural_sensitivity: float = 0.7):
        """
        Initialize the social dimension.
        
        Args:
            cultural_sensitivity: Cultural awareness level (0-1)
        """
        self.cultural_sensitivity = cultural_sensitivity
        self._social_embedding: Optional[np.ndarray] = None
    
    def analyze_social_context(
        self,
        interactions: List[Dict[str, Any]],
        cultural_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze social context and cultural factors.
        
        Args:
            interactions: List of interaction data
            cultural_context: Cultural context information
        
        Returns:
            Dictionary with social analysis
        """
        # Create social embedding
        embedding = self._create_social_embedding(interactions, cultural_context)
        
        # Calculate social metrics
        metrics = self._calculate_social_metrics(interactions)
        
        return {
            "embedding": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
            "metrics": metrics,
            "cultural_context": cultural_context or {},
        }
    
    def _create_social_embedding(
        self,
        interactions: List[Dict[str, Any]],
        cultural_context: Optional[Dict[str, Any]],
    ) -> np.ndarray:
        """
        Create embedding from social data.
        
        Args:
            interactions: Interaction data
            cultural_context: Cultural context
        
        Returns:
            8D social embedding
        """
        embedding = np.zeros(8)
        
        # Interaction count (dimension 0)
        embedding[0] = float(len(interactions) / 10)
        
        # Cultural diversity (dimension 1)
        if cultural_context:
            cultures = set(cultural_context.get("cultures", []))
            embedding[1] = min(1.0, len(cultures) / 5)
        
        # Social complexity (dimension 2)
        if interactions:
            complexity = sum(
                1 for i in interactions 
                if i.get("complexity", 0) > 0
            )
            embedding[2] = complexity / max(len(interactions), 1)
        
        # Trust indicators (dimensions 3-7)
        if interactions:
            trust_scores = [i.get("trust", 0.5) for i in interactions]
            # Average trust for dimensions 3-7
            avg_trust = np.mean(trust_scores) if trust_scores else 0.5
            embedding[3:8] = [avg_trust, avg_trust, avg_trust, avg_trust, avg_trust]
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def _calculate_social_metrics(
        self,
        interactions: List[Dict[str, Any]],
    ) -> Dict[str, float]:
        """
        Calculate social metrics.
        
        Args:
            interactions: Interaction data
        
        Returns:
            Dictionary of metrics
        """
        if not interactions:
            return {}
        
        metrics = {}
        
        # Interaction count
        metrics["interaction_count"] = float(len(interactions))
        
        # Average trust
        trust_scores = [i.get("trust", 0.5) for i in interactions]
        metrics["avg_trust"] = float(np.mean(trust_scores))
        
        # Social cohesion
        if len(interactions) > 1:
            trust_variance = np.var(trust_scores)
            metrics["cohesion"] = float(1.0 - trust_variance)
        
        # Cultural representation
        metrics["cultural_sensitivity"] = float(self.cultural_sensitivity)
        
        return metrics
    
    def get_embedding(self) -> Optional[np.ndarray]:
        """
        Get current social embedding.
        
        Returns:
            Social embedding or None
        """
        return self._social_embedding
    
    def set_embedding(self, embedding: np.ndarray) -> None:
        """
        Set social embedding.
        
        Args:
            embedding: New embedding
        """
        self._social_embedding = embedding
    
    def normalize(self) -> None:
        """Normalize current social embedding."""
        if self._social_embedding is not None:
            norm = np.linalg.norm(self._social_embedding)
            if norm > 0:
                self._social_embedding = self._social_embedding / norm
    
    def __repr__(self) -> str:
        return f"SocialDimension(sensitivity={self.cultural_sensitivity:.2f})"
    
    def __str__(self) -> str:
        return self.__repr__()
