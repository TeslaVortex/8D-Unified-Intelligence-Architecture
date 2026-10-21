"""
Unit Tests for Utils Module

Tests for embedding and helper utilities.
"""

import pytest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utils.embeddings import EmbeddingFunction, normalize_vector, validate_embedding, cosine_similarity
from src.utils.helpers import (
    generate_id,
    timestamp_now,
    safe_divide,
    clamp,
    interpolate,
    weighted_average,
    normalize_list,
    batch_process,
    merge_dicts,
    deep_copy,
    ensure_list,
    format_duration,
    truncate_string,
)


class TestEmbeddingFunction:
    """Tests for EmbeddingFunction class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.embedding_fn = EmbeddingFunction(dimension=128, seed=42)
    
    def test_initialization(self):
        """Test embedding function initialization."""
        assert self.embedding_fn.dimension == 128
        assert self.embedding_fn._seed == 42
    
    def test_generate_hash_embedding(self):
        """Test hash-based embedding generation."""
        embedding = self.embedding_fn.generate("test query", method="hash")
        
        assert isinstance(embedding, np.ndarray)
        assert embedding.shape[0] == 128
        assert np.all(np.isfinite(embedding))
    
    def test_generate_semantic_embedding(self):
        """Test semantic-based embedding generation."""
        embedding = self.embedding_fn.generate("test query", method="semantic")
        
        assert isinstance(embedding, np.ndarray)
        assert embedding.shape[0] == 128
        assert np.all(np.isfinite(embedding))
    
    def test_deterministic_hash(self):
        """Test that hash embeddings are deterministic."""
        embedding1 = self.embedding_fn.generate("test query", method="hash")
        embedding2 = self.embedding_fn.generate("test query", method="hash")
        
        assert np.array_equal(embedding1, embedding2)
    
    def test_different_texts_different_embeddings(self):
        """Test that different texts produce different embeddings."""
        embedding1 = self.embedding_fn.generate("text1", method="hash")
        embedding2 = self.embedding_fn.generate("text2", method="hash")
        
        assert not np.array_equal(embedding1, embedding2)
    
    def test_batch_generate(self):
        """Test batch embedding generation."""
        texts = ["text1", "text2", "text3"]
        embeddings = self.embedding_fn.batch_generate(texts, method="hash")
        
        assert len(embeddings) == 3
        assert all(isinstance(e, np.ndarray) for e in embeddings)
    
    def test_encode(self):
        """Test encoding with metadata."""
        result = self.embedding_fn.encode("test query")
        
        assert "embedding" in result
        assert "metadata" in result
        assert "dimension" in result["metadata"]
        assert "hash" in result["metadata"]
    
    def test_normalize_vector(self):
        """Test vector normalization."""
        vector = np.array([3.0, 4.0])
        normalized = normalize_vector(vector)
        
        assert len(normalized) == 2
        assert np.isclose(np.linalg.norm(normalized), 1.0)
    
    def test_validate_embedding_valid(self):
        """Test validation of valid embedding."""
        vector = np.array([0.1] * 128)
        assert validate_embedding(vector, dimension=128) is True
    
    def test_validate_embedding_invalid_dimension(self):
        """Test validation of invalid dimension."""
        vector = np.array([0.1] * 128)
        assert validate_embedding(vector, dimension=64) is False
    
    def test_validate_embedding_invalid_type(self):
        """Test validation of invalid type."""
        assert validate_embedding("not a vector") is False
    
    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        a = np.array([1.0, 0.0])
        b = np.array([1.0, 0.0])
        
        similarity = cosine_similarity(a, b)
        
        assert np.isclose(similarity, 1.0)


class TestHelpers:
    """Tests for helper functions."""
    
    def test_generate_id(self):
        """Test ID generation."""
        id1 = generate_id("test")
        id2 = generate_id("test")
        
        assert len(id1) > 0
        assert id1 != id2
    
    def test_timestamp_now(self):
        """Test timestamp generation."""
        ts1 = timestamp_now()
        ts2 = timestamp_now()
        
        assert len(ts1) > 0
        assert isinstance(ts1, str)
    
    def test_safe_divide(self):
        """Test safe division."""
        assert safe_divide(10.0, 2.0) == 5.0
        assert safe_divide(10.0, 0.0) == 0.0
        assert safe_divide("invalid", 2.0) == 0.0
    
    def test_clamp(self):
        """Test clamping."""
        assert clamp(5.0, 0.0, 10.0) == 5.0
        assert clamp(-5.0, 0.0, 10.0) == 0.0
        assert clamp(15.0, 0.0, 10.0) == 10.0
    
    def test_interpolate(self):
        """Test interpolation."""
        assert interpolate(0.0, 10.0, 0.0) == 0.0
        assert interpolate(0.0, 10.0, 1.0) == 10.0
        assert interpolate(0.0, 10.0, 0.5) == 5.0
    
    def test_weighted_average(self):
        """Test weighted average."""
        values = [1.0, 2.0, 3.0]
        weights = [1.0, 1.0, 1.0]
        
        result = weighted_average(values, weights)
        
        assert result == 2.0
    
    def test_normalize_list(self):
        """Test list normalization."""
        values = [1.0, 2.0, 3.0]
        normalized = normalize_list(values)
        
        assert len(normalized) == 3
        assert normalized[0] == 0.0
        assert normalized[2] == 1.0
    
    def test_batch_process(self):
        """Test batch processing."""
        items = [1, 2, 3, 4, 5]
        processor = lambda x: x * 2
        
        result = batch_process(items, processor)
        
        assert result == [2, 4, 6, 8, 10]
    
    def test_merge_dicts(self):
        """Test dictionary merging."""
        d1 = {"a": 1, "b": 2}
        d2 = {"c": 3, "d": 4}
        
        result = merge_dicts(d1, d2)
        
        assert result["a"] == 1
        assert result["c"] == 3
    
    def test_deep_copy(self):
        """Test deep copy."""
        obj = {"a": 1, "b": [2, 3]}
        copy = deep_copy(obj)
        
        assert copy == obj
        assert copy is not obj
        assert copy["b"] is not obj["b"]
    
    def test_ensure_list(self):
        """Test list conversion."""
        assert ensure_list([1, 2, 3]) == [1, 2, 3]
        assert ensure_list(1) == [1]
    
    def test_format_duration(self):
        """Test duration formatting."""
        assert "ms" in format_duration(0.5)
        assert "s" in format_duration(5.5)
        assert "m" in format_duration(60.5)
    
    def test_truncate_string(self):
        """Test string truncation."""
        assert len(truncate_string("short", 100)) == 5
        assert len(truncate_string("a" * 150, 100)) == 100
