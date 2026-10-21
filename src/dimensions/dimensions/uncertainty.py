"""
Uncertainty Dimension (η) Module

Processes uncertainty and probabilistic reasoning.
"""

import numpy as np
from typing import Optional, Dict, Any, List
from scipy.stats import entropy, binom


class UncertaintyDimension:
    """
    Eta dimension - Uncertainty Processing.
    
    Handles uncertainty quantification, probabilistic reasoning,
    and confidence assessment.
    
    Attributes:
        confidence_threshold: Minimum confidence threshold
    """
    
    def __init__(self, confidence_threshold: float = 0.6):
        """
        Initialize the uncertainty dimension.
        
        Args:
            confidence_threshold: Minimum confidence threshold (0-1)
        """
        self.confidence_threshold = confidence_threshold
        self._uncertainty_embedding: Optional[np.ndarray] = None
    
    def quantify_uncertainty(
        self,
        predictions: List[Dict[str, Any]],
        observations: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Quantify uncertainty in predictions.
        
        Args:
            predictions: List of predictions with confidence scores
            observations: Optional list of observations
        
        Returns:
            Dictionary with uncertainty metrics
        """
        # Create uncertainty embedding
        embedding = self._create_uncertainty_embedding(predictions, observations)
        
        # Calculate uncertainty metrics
        metrics = self._calculate_uncertainty_metrics(predictions, observations)
        
        return {
            "embedding": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
            "metrics": metrics,
        }
    
    def _create_uncertainty_embedding(
        self,
        predictions: List[Dict[str, Any]],
        observations: Optional[List[Dict[str, Any]]],
    ) -> np.ndarray:
        """
        Create embedding from uncertainty data.
        
        Args:
            predictions: Prediction data
            observations: Observation data
        
        Returns:
            8D uncertainty embedding
        """
        embedding = np.zeros(8)
        
        # Prediction confidence (dimension 0)
        confidences = [p.get("confidence", 0.5) for p in predictions]
        if confidences:
            embedding[0] = np.mean(confidences)
        
        # Prediction variance (dimension 1)
        if len(confidences) > 1:
            embedding[1] = np.std(confidences)
        
        # Entropy-based uncertainty (dimension 2)
        if confidences:
            probs = np.array(confidences) / sum(confidences)
            embedding[2] = entropy(probs)
        
        # Observation agreement (dimensions 3-7)
        if observations and len(observations) > 1:
            obs_confidences = [o.get("confidence", 0.5) for o in observations]
            embedding[3:8] = np.array(obs_confidences[:4])
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def _calculate_uncertainty_metrics(
        self,
        predictions: List[Dict[str, Any]],
        observations: Optional[List[Dict[str, Any]]],
    ) -> Dict[str, float]:
        """
        Calculate uncertainty metrics.
        
        Args:
            predictions: Prediction data
            observations: Observation data
        
        Returns:
            Dictionary of metrics
        """
        if not predictions:
            return {}
        
        metrics = {}
        
        # Average confidence
        confidences = [p.get("confidence", 0.5) for p in predictions]
        metrics["avg_confidence"] = float(np.mean(confidences))
        
        # Confidence variance
        if len(confidences) > 1:
            metrics["confidence_variance"] = float(np.var(confidences))
        
        # Below threshold count
        below_threshold = sum(1 for c in confidences if c < self.confidence_threshold)
        metrics["below_threshold"] = float(below_threshold / len(confidences))
        
        # Overall uncertainty
        metrics["overall_uncertainty"] = float(1.0 - metrics["avg_confidence"])
        
        return metrics
    
    def assess_confidence(
        self,
        prediction: Dict[str, Any],
    ) -> float:
        """
        Assess confidence in a prediction.
        
        Args:
            prediction: Prediction data
        
        Returns:
            Confidence score (0-1)
        """
        confidence = prediction.get("confidence", 0.5)
        
        # Apply threshold adjustment
        if confidence < self.confidence_threshold:
            confidence = confidence * 0.5
        
        return float(confidence)
    
    def get_embedding(self) -> Optional[np.ndarray]:
        """
        Get current uncertainty embedding.
        
        Returns:
            Uncertainty embedding or None
        """
        return self._uncertainty_embedding
    
    def set_embedding(self, embedding: np.ndarray) -> None:
        """
        Set uncertainty embedding.
        
        Args:
            embedding: New embedding
        """
        self._uncertainty_embedding = embedding
    
    def normalize(self) -> None:
        """Normalize current uncertainty embedding."""
        if self._uncertainty_embedding is not None:
            norm = np.linalg.norm(self._uncertainty_embedding)
            if norm > 0:
                self._uncertainty_embedding = self._uncertainty_embedding / norm
    
    def __repr__(self) -> str:
        return f"UncertaintyDimension(threshold={self.confidence_threshold:.2f})"
    
    def __str__(self) -> str:
        return self.__repr__()
