"""
Embedding Functions Module

Provides embedding generation utilities for the 8D intelligence system.
"""

import numpy as np
from typing import Optional, List, Dict, Any
import hashlib
import json


class EmbeddingFunction:
    """
    Embedding function for generating vector representations.
    
    Provides deterministic embedding generation using a combination
    of hash-based and semantic-based approaches.
    
    Attributes:
        dimension: Embedding dimension (default: 768)
        seed: Random seed for reproducibility
    """
    
    def __init__(self, dimension: int = 768, seed: Optional[int] = None):
        """
        Initialize the embedding function.
        
        Args:
            dimension: Embedding vector dimension
            seed: Random seed for reproducibility
        """
        self.dimension = dimension
        self._seed = seed
        self._random_state = np.random.RandomState(seed)
    
    def generate(self, text: str, method: str = "hash") -> np.ndarray:
        """
        Generate embedding vector from text.
        
        Args:
            text: Input text to embed
            method: Embedding method ('hash' or 'semantic')
        
        Returns:
            numpy array of embedding vector
        """
        if method == "hash":
            return self._hash_embedding(text)
        elif method == "semantic":
            return self._semantic_embedding(text)
        else:
            raise ValueError(f"Unknown embedding method: {method}")
    
    def _hash_embedding(self, text: str) -> np.ndarray:
        """
        Generate hash-based embedding.
        
        Creates a deterministic embedding from text hash.
        
        Args:
            text: Input text
        
        Returns:
            numpy array of embedding vector
        """
        # Create hash from text
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        # Convert hash to numeric values
        hash_values = [int(text_hash[i:i+2], 16) for i in range(0, len(text_hash), 2)]
        
        # Normalize to [0, 1] range
        normalized = np.array(hash_values, dtype=np.float64) / 255.0
        
        # Resample to target dimension if needed
        if len(normalized) < self.dimension:
            normalized = np.pad(
                normalized,
                (0, self.dimension - len(normalized)),
                constant_values=0.0
            )
        elif len(normalized) > self.dimension:
            normalized = normalized[:self.dimension]
        
        # Normalize to unit vector
        normalized = normalized / (np.linalg.norm(normalized) + 1e-8)
        
        return normalized
    
    def _semantic_embedding(self, text: str) -> np.ndarray:
        """
        Generate semantic-based embedding.
        
        Creates embedding from character/word frequency analysis.
        
        Args:
            text: Input text
        
        Returns:
            numpy array of embedding vector
        """
        # Tokenize text
        tokens = text.lower().split()
        
        # Generate embedding from token properties
        embedding = np.zeros(self.dimension, dtype=np.float64)
        
        for token in tokens[:100]:  # Limit to first 100 tokens
            # Character-level features
            char_freq = np.bincount([ord(c) % self.dimension for c in token], minlength=self.dimension)
            embedding += char_freq.astype(np.float64) / len(token)
        
        # Normalize
        norm = np.linalg.norm(embedding) + 1e-8
        embedding = embedding / norm
        
        return embedding
    
    def batch_generate(self, texts: List[str], method: str = "hash") -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts
            method: Embedding method
        
        Returns:
            List of embedding vectors
        """
        return [self.generate(text, method) for text in texts]
    
    def encode(self, text: str) -> Dict[str, Any]:
        """
        Generate embedding with metadata.
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with embedding and metadata
        """
        embedding = self.generate(text)
        metadata = {
            "dimension": self.dimension,
            "method": "hash",
            "hash": hashlib.sha256(text.encode()).hexdigest()[:16],
            "length": len(text),
        }
        return {"embedding": embedding, "metadata": metadata}


def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """
    Normalize a vector to unit length.
    
    Args:
        vector: Input vector
        
    Returns:
        Normalized vector
    """
    norm = np.linalg.norm(vector) + 1e-8
    return vector / norm


def validate_embedding(vector: np.ndarray, dimension: Optional[int] = None) -> bool:
    """
    Validate an embedding vector.
    
    Args:
        vector: Vector to validate
        dimension: Expected dimension (optional)
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(vector, np.ndarray):
        return False
    
    if dimension is not None and vector.shape[0] != dimension:
        return False
    
    # Check if vector is finite
    if not np.all(np.isfinite(vector)):
        return False
    
    return True


def clamp_value(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Clamp a value to a range.
    
    Args:
        value: Input value
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Cosine similarity value in [-1, 1]
    """
    a_normalized = a / (np.linalg.norm(a) + 1e-8)
    b_normalized = b / (np.linalg.norm(b) + 1e-8)
    return float(np.dot(a_normalized, b_normalized))
