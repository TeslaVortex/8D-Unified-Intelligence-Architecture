"""
Tensor Operations Module

Core 8D tensor operations for novelty detection.
"""

import numpy as np
from typing import Optional, Tuple
from scipy.spatial.distance import cosine, jaccard


class TensorOperations:
    """
    Core tensor operations for 8D space manipulation.
    
    Provides mathematical operations for computing similarity,
    distance, and alignment between 8-dimensional vectors.
    """
    
    DIMENSIONALITY = 8
    
    @staticmethod
    def embed(text: str, embedding_dim: int = 8) -> np.ndarray:
        """
        Create an 8D embedding from text.
        
        This is a placeholder for actual embedding generation.
        In production, this would use a pre-trained model.
        
        Args:
            text: Input text to embed
            embedding_dim: Dimensionality of the embedding (default: 8)
        
        Returns:
            numpy.ndarray: 8D embedding vector normalized to unit length
        """
        # Placeholder: Create deterministic embedding based on text hash
        # In production, replace with actual embedding model
        seed = sum(ord(c) for c in text)
        base_vector = np.random.RandomState(seed).randn(embedding_dim)
        return normalize_vector(base_vector)
    
    @staticmethod
    def calculate_cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            v1: First embedding vector
            v2: Second embedding vector
        
        Returns:
            float: Cosine similarity between -1 and 1
        """
        if not isinstance(v1, np.ndarray) or not isinstance(v2, np.ndarray):
            raise TypeError("Both inputs must be numpy arrays")
        
        if v1.shape != v2.shape:
            raise ValueError(f"Shape mismatch: {v1.shape} vs {v2.shape}")
        
        # Normalize vectors
        v1_norm = normalize_vector(v1)
        v2_norm = normalize_vector(v2)
        
        # Calculate cosine similarity
        similarity = np.dot(v1_norm, v2_norm)
        
        # Ensure result is in valid range
        similarity = np.clip(similarity, -1.0, 1.0)
        
        return float(similarity)
    
    @staticmethod
    def calculate_structural_similarity(
        topo_a: np.ndarray,
        topo_b: np.ndarray,
    ) -> float:
        """
        Calculate Jaccard similarity for structural/topological comparison.
        
        Args:
            topo_a: First topological representation
            topo_b: Second topological representation
        
        Returns:
            float: Jaccard similarity between 0 and 1
        """
        if not isinstance(topo_a, np.ndarray) or not isinstance(topo_b, np.ndarray):
            raise TypeError("Both inputs must be numpy arrays")
        
        if topo_a.shape != topo_b.shape:
            raise ValueError(f"Shape mismatch: {topo_a.shape} vs {topo_b.shape}")
        
        # Convert to boolean for structural comparison
        binary_a = (topo_a > 0).astype(int)
        binary_b = (topo_b > 0).astype(int)
        
        # Calculate Jaccard similarity
        intersection = np.sum(binary_a & binary_b)
        union = np.sum(binary_a | binary_b)
        
        if union == 0:
            return 1.0
        
        similarity = intersection / union
        return float(similarity)
    
    @staticmethod
    def calculate_temporal_alignment(
        t1: np.ndarray,
        t2: np.ndarray,
    ) -> float:
        """
        Calculate temporal alignment between two temporal representations.
        
        Args:
            t1: First temporal representation
            t2: Second temporal representation
        
        Returns:
            float: Temporal alignment score between 0 and 1
        """
        if not isinstance(t1, np.ndarray) or not isinstance(t2, np.ndarray):
            raise TypeError("Both inputs must be numpy arrays")
        
        if t1.shape != t2.shape:
            raise ValueError(f"Shape mismatch: {t1.shape} vs {t2.shape}")
        
        # Calculate temporal distance
        temporal_diff = np.mean(np.abs(t1 - t2))
        
        # Convert to alignment score (higher is better alignment)
        alignment = 1.0 - temporal_diff
        
        # Ensure result is in valid range
        alignment = np.clip(alignment, 0.0, 1.0)
        
        return float(alignment)
    
    @staticmethod
    def normalize_vector(vector: np.ndarray) -> np.ndarray:
        """
        Normalize a vector to unit length.
        
        Args:
            vector: Input vector
        
        Returns:
            numpy.ndarray: Normalized vector
        """
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
    
    @staticmethod
    def compute_distance(
        v1: np.ndarray,
        v2: np.ndarray,
        metric: str = "cosine",
    ) -> float:
        """
        Compute distance between two vectors.
        
        Args:
            v1: First vector
            v2: Second vector
            metric: Distance metric to use ('cosine', 'euclidean', 'jaccard')
        
        Returns:
            float: Distance between vectors
        """
        if metric == "cosine":
            return 1.0 - TensorOperations.calculate_cosine_similarity(v1, v2)
        elif metric == "euclidean":
            return float(np.linalg.norm(v1 - v2))
        elif metric == "jaccard":
            return 1.0 - TensorOperations.calculate_structural_similarity(v1, v2)
        else:
            raise ValueError(f"Unknown metric: {metric}")
    
    @staticmethod
    def project_to_hypercube(vector: np.ndarray) -> np.ndarray:
        """
        Project a vector onto the unit hypercube.
        
        Args:
            vector: Input vector
        
        Returns:
            numpy.ndarray: Vector projected to [-1, 1]^8
        """
        clamped = np.clip(vector, -1, 1)
        return clamped
    
    @staticmethod
    def compute_euclidean_distance(v1: np.ndarray, v2: np.ndarray) -> float:
        """
        Compute Euclidean distance between two vectors.
        
        Args:
            v1: First vector
            v2: Second vector
        
        Returns:
            float: Euclidean distance
        """
        return float(np.linalg.norm(v1 - v2))
    
    @staticmethod
    def normalize_to_unit_sphere(vector: np.ndarray) -> np.ndarray:
        """
        Normalize vector to lie on unit sphere.
        
        Args:
            vector: Input vector
        
        Returns:
            numpy.ndarray: Vector on unit sphere
        """
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
    
    @staticmethod
    def vector_dot_product(v1: np.ndarray, v2: np.ndarray) -> float:
        """
        Compute dot product of two vectors.
        
        Args:
            v1: First vector
            v2: Second vector
        
        Returns:
            float: Dot product
        """
        return float(np.dot(v1, v2))
    
    @staticmethod
    def vector_angle(v1: np.ndarray, v2: np.ndarray) -> float:
        """
        Calculate angle between two vectors in radians.
        
        Args:
            v1: First vector
            v2: Second vector
        
        Returns:
            float: Angle in radians
        """
        dot_product = TensorOperations.vector_dot_product(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        
        cosine = dot_product / (norm_v1 * norm_v2)
        cosine = np.clip(cosine, -1.0, 1.0)
        
        return float(np.arccos(cosine))


def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """
    Normalize a vector to unit length.
    
    Args:
        vector: Input vector
    
    Returns:
        numpy.ndarray: Normalized vector
    """
    return TensorOperations.normalize_vector(vector)


def validate_embedding(vector: np.ndarray, dim: int = 8) -> bool:
    """
    Validate that a vector is a proper embedding.
    
    Args:
        vector: Vector to validate
        dim: Expected dimensionality
    
    Returns:
        bool: True if valid embedding
    """
    if not isinstance(vector, np.ndarray):
        return False
    
    if vector.shape[0] != dim:
        return False
    
    return True
