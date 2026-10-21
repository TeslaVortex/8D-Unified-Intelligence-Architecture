"""
Input Sensory Dimension (α) Module

Processes raw sensory input and external stimuli.
"""

import numpy as np
from typing import Optional, Dict, Any, List
from scipy.stats import entropy


class InputSensoryDimension:
    """
    Alpha dimension - Input Sensory Processing.
    
    Handles the ingestion and initial processing of raw sensory
    input from the environment.
    
    Attributes:
        sensitivity: Sensitivity threshold for input detection
    """
    
    def __init__(self, sensitivity: float = 0.5):
        """
        Initialize the input sensory dimension.
        
        Args:
            sensitivity: Detection sensitivity threshold (0-1)
        """
        self.sensitivity = sensitivity
        self._embedding: Optional[np.ndarray] = None
    
    def process_input(
        self,
        stimuli: List[Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Process raw sensory stimuli.
        
        Args:
            stimuli: List of sensory stimuli
            metadata: Additional context
        
        Returns:
            Dictionary with processed input data
        """
        # Convert stimuli to embedding
        embedding = self._create_stimuli_embedding(stimuli)
        
        # Calculate input entropy
        entropy_score = self._calculate_input_entropy(stimuli)
        
        # Extract sensory features
        features = self._extract_sensory_features(stimuli)
        
        return {
            "embedding": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
            "entropy": float(entropy_score),
            "features": features,
            "metadata": metadata or {},
        }
    
    def _create_stimuli_embedding(
        self,
        stimuli: List[Any],
    ) -> np.ndarray:
        """
        Create an embedding from raw stimuli.
        
        Args:
            stimuli: Raw stimuli
        
        Returns:
            1D embedding vector
        """
        # Convert stimuli to numerical representation
        numerical = self._stimuli_to_numerical(stimuli)
        
        # Create embedding from numerical values
        embedding = self._numerical_to_embedding(numerical)
        
        return embedding
    
    def _stimuli_to_numerical(
        self,
        stimuli: List[Any],
    ) -> np.ndarray:
        """
        Convert stimuli to numerical representation.
        
        Args:
            stimuli: Raw stimuli
        
        Returns:
            Numerical array
        """
        # Placeholder implementation
        # In production, this would use actual encoding
        numerical = np.zeros(len(stimuli))
        
        for i, stimulus in enumerate(stimuli):
            if isinstance(stimulus, str):
                # Use character frequency as numeric value
                numerical[i] = len(stimulus) / 100.0
            elif isinstance(stimulus, (int, float)):
                numerical[i] = float(stimulus) / 100.0
            else:
                numerical[i] = 0.0
        
        return numerical
    
    def _numerical_to_embedding(
        self,
        numerical: np.ndarray,
    ) -> np.ndarray:
        """
        Convert numerical array to 8D embedding.
        
        Args:
            numerical: Numerical array
        
        Returns:
            8D embedding vector
        """
        # Placeholder: Create deterministic embedding
        # In production, use actual embedding model
        seed = int(sum(numerical) * 10000)
        rng = np.random.RandomState(seed)
        embedding = rng.randn(8)
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def _calculate_input_entropy(
        self,
        stimuli: List[Any],
    ) -> float:
        """
        Calculate entropy of input stimuli.
        
        Args:
            stimuli: Raw stimuli
        
        Returns:
            Entropy score
        """
        # Convert to probability distribution
        probabilities = self._stimuli_to_probabilities(stimuli)
        
        # Calculate Shannon entropy
        if len(probabilities) == 0:
            return 0.0
        
        # Filter out zero probabilities
        valid_probs = [p for p in probabilities if p > 0]
        
        if not valid_probs:
            return 0.0
        
        return float(entropy(valid_probs, base=2))
    
    def _stimuli_to_probabilities(
        self,
        stimuli: List[Any],
    ) -> List[float]:
        """
        Convert stimuli to probability distribution.
        
        Args:
            stimuli: Raw stimuli
        
        Returns:
            List of probabilities
        """
        if not stimuli:
            return []
        
        # Count occurrences
        counts = {}
        for stimulus in stimuli:
            key = str(stimulus)
            counts[key] = counts.get(key, 0) + 1
        
        # Convert to probabilities
        total = sum(counts.values())
        probabilities = [count / total for count in counts.values()]
        
        return probabilities
    
    def _extract_sensory_features(
        self,
        stimuli: List[Any],
    ) -> Dict[str, float]:
        """
        Extract sensory features from stimuli.
        
        Args:
            stimuli: Raw stimuli
        
        Returns:
            Dictionary of feature values
        """
        features = {}
        
        # Count total stimuli
        features["total_stimuli"] = float(len(stimuli))
        
        # Calculate diversity
        unique_stimuli = len(set(str(s) for s in stimuli))
        features["diversity"] = float(unique_stimuli / max(len(stimuli), 1))
        
        # Calculate average intensity (placeholder)
        intensities = []
        for stimulus in stimuli:
            if isinstance(stimulus, (int, float)):
                intensities.append(float(stimulus))
        
        if intensities:
            features["average_intensity"] = float(np.mean(intensities))
            features["max_intensity"] = float(max(intensities))
            features["min_intensity"] = float(min(intensities))
        
        return features
    
    def get_embedding(self) -> Optional[np.ndarray]:
        """
        Get the current dimension embedding.
        
        Returns:
            Embedding vector or None
        """
        return self._embedding
    
    def set_embedding(self, embedding: np.ndarray) -> None:
        """
        Set the dimension embedding.
        
        Args:
            embedding: New embedding vector
        """
        self._embedding = embedding
    
    def normalize(self) -> None:
        """Normalize the current embedding."""
        if self._embedding is not None:
            norm = np.linalg.norm(self._embedding)
            if norm > 0:
                self._embedding = self._embedding / norm
    
    def __repr__(self) -> str:
        return f"InputSensoryDimension(sensitivity={self.sensitivity})"
    
    def __str__(self) -> str:
        return self.__repr__()
