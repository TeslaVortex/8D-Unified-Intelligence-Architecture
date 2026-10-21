"""
Unit tests for TensorOperations

Tests for core 8D tensor operations including:
- Embedding generation
- Similarity calculations
- Distance metrics
- Vector operations
"""

import numpy as np
import pytest
from typing import Tuple

from src.novelty_engine.tensor_operations import TensorOperations


class TestTensorOperations:
    """Tests for TensorOperations class."""
    
    @pytest.fixture
    def operations(self):
        """Create a test operations instance."""
        return TensorOperations()
    
    def test_embed_basic(self, operations):
        """Test basic text embedding."""
        text = "test query for embedding"
        embedding = operations.embed(text, embedding_dim=8)
        
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) == 8
    
    def test_embed_empty_string(self, operations):
        """Test embedding of empty string."""
        embedding = operations.embed("", embedding_dim=8)
        
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) == 8
    
    def test_embed_different_texts(self, operations):
        """Test that different texts produce different embeddings."""
        embedding1 = operations.embed("first text")
        embedding2 = operations.embed("second text")
        
        assert not np.array_equal(embedding1, embedding2)
    
    def test_embed_deterministic(self, operations):
        """Test that same text produces same embedding (deterministic)."""
        embedding1 = operations.embed("deterministic test")
        embedding2 = operations.embed("deterministic test")
        
        assert np.array_equal(embedding1, embedding2)
    
    def test_embed_different_dimensions(self, operations):
        """Test embedding with different dimensions."""
        embedding_4d = operations.embed("test", embedding_dim=4)
        embedding_8d = operations.embed("test", embedding_dim=8)
        
        assert len(embedding_4d) == 4
        assert len(embedding_8d) == 8
    
    def test_embed_returns_normalized(self, operations):
        """Test that embeddings are normalized."""
        text = "normalization test"
        embedding = operations.embed(text, embedding_dim=8)
        
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 1e-6
    
    def test_embed_invalid_dimension(self, operations):
        """Test embedding with invalid dimension."""
        with pytest.raises(Exception):
            operations.embed("test", embedding_dim=-1)
    
    def test_calculate_cosine_similarity(self, operations):
        """Test cosine similarity calculation."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        similarity = operations.calculate_cosine_similarity(v1, v2)
        
        assert isinstance(similarity, float)
        assert -1.0 <= similarity <= 1.0
    
    def test_calculate_cosine_similarity_same_vector(self, operations):
        """Test cosine similarity with same vector."""
        v = np.random.randn(8)
        
        similarity = operations.calculate_cosine_similarity(v, v)
        
        # Allow small floating point tolerance
        assert abs(similarity - 1.0) < 1e-10
    
    def test_calculate_cosine_similarity_opposite_vectors(self, operations):
        """Test cosine similarity with opposite vectors."""
        v = np.random.randn(8)
        opposite = -v
        
        similarity = operations.calculate_cosine_similarity(v, opposite)
        
        # Allow small floating point tolerance
        assert abs(similarity - (-1.0)) < 1e-10
    
    def test_calculate_cosine_similarity_orthogonal_vectors(self, operations):
        """Test cosine similarity with orthogonal vectors."""
        # Create truly orthogonal vectors using Gram-Schmidt process
        v1 = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        v2 = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        
        similarity = operations.calculate_cosine_similarity(v1, v2)
        
        # Orthogonal vectors should have similarity close to 0
        assert abs(similarity) < 1e-10
    
    def test_calculate_cosine_similarity_invalid_input_type(self, operations):
        """Test cosine similarity with invalid input type."""
        v1 = [1, 2, 3, 4, 5, 6, 7, 8]  # Not numpy array
        v2 = np.random.randn(8)
        
        with pytest.raises(TypeError):
            operations.calculate_cosine_similarity(v1, v2)
    
    def test_calculate_cosine_similarity_shape_mismatch(self, operations):
        """Test cosine similarity with shape mismatch."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(10)
        
        with pytest.raises(ValueError):
            operations.calculate_cosine_similarity(v1, v2)
    
    def test_calculate_structural_similarity(self, operations):
        """Test structural similarity calculation."""
        topo_a = np.random.randn(8)
        topo_b = np.random.randn(8)
        
        similarity = operations.calculate_structural_similarity(topo_a, topo_b)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    def test_calculate_structural_similarity_same_vector(self, operations):
        """Test structural similarity with same vector."""
        v = np.random.randn(8)
        
        similarity = operations.calculate_structural_similarity(v, v)
        
        assert similarity == 1.0
    
    def test_calculate_structural_similarity_binary_vectors(self, operations):
        """Test structural similarity with binary vectors."""
        binary_a = np.random.randint(0, 2, 8).astype(float)
        binary_b = np.random.randint(0, 2, 8).astype(float)
        
        similarity = operations.calculate_structural_similarity(binary_a, binary_b)
        
        assert 0.0 <= similarity <= 1.0
    
    def test_calculate_structural_similarity_invalid_input_type(self, operations):
        """Test structural similarity with invalid input type."""
        topo_a = [1, 2, 3, 4, 5, 6, 7, 8]  # Not numpy array
        topo_b = np.random.randn(8)
        
        with pytest.raises(TypeError):
            operations.calculate_structural_similarity(topo_a, topo_b)
    
    def test_calculate_structural_similarity_shape_mismatch(self, operations):
        """Test structural similarity with shape mismatch."""
        topo_a = np.random.randn(8)
        topo_b = np.random.randn(10)
        
        with pytest.raises(ValueError):
            operations.calculate_structural_similarity(topo_a, topo_b)
    
    def test_calculate_temporal_alignment(self, operations):
        """Test temporal alignment calculation."""
        t1 = np.random.randn(8)
        t2 = np.random.randn(8)
        
        alignment = operations.calculate_temporal_alignment(t1, t2)
        
        assert isinstance(alignment, float)
        assert 0.0 <= alignment <= 1.0
    
    def test_calculate_temporal_alignment_same_vector(self, operations):
        """Test temporal alignment with same vector."""
        t = np.random.randn(8)
        
        alignment = operations.calculate_temporal_alignment(t, t)
        
        assert alignment == 1.0
    
    def test_calculate_temporal_alignment_different_vectors(self, operations):
        """Test temporal alignment with different vectors."""
        t1 = np.random.randn(8) * 2
        t2 = np.random.randn(8) / 2
        
        alignment = operations.calculate_temporal_alignment(t1, t2)
        
        assert 0.0 <= alignment <= 1.0
    
    def test_calculate_temporal_alignment_invalid_input_type(self, operations):
        """Test temporal alignment with invalid input type."""
        t1 = [1, 2, 3, 4, 5, 6, 7, 8]  # Not numpy array
        t2 = np.random.randn(8)
        
        with pytest.raises(TypeError):
            operations.calculate_temporal_alignment(t1, t2)
    
    def test_calculate_temporal_alignment_shape_mismatch(self, operations):
        """Test temporal alignment with shape mismatch."""
        t1 = np.random.randn(8)
        t2 = np.random.randn(10)
        
        with pytest.raises(ValueError):
            operations.calculate_temporal_alignment(t1, t2)
    
    def test_normalize_vector(self, operations):
        """Test vector normalization."""
        v = np.random.randn(8) * 2
        
        normalized = operations.normalize_vector(v)
        
        assert isinstance(normalized, np.ndarray)
        assert len(normalized) == 8
        assert abs(np.linalg.norm(normalized) - 1.0) < 1e-6
    
    def test_normalize_zero_vector(self, operations):
        """Test normalization of zero vector."""
        zero_vector = np.zeros(8)
        
        normalized = operations.normalize_vector(zero_vector)
        
        assert np.array_equal(normalized, zero_vector)
    
    def test_normalize_vector_already_normalized(self, operations):
        """Test normalization of already normalized vector."""
        v = np.random.randn(8)
        normalized_v = operations.normalize_vector(v)
        
        normalized_again = operations.normalize_vector(normalized_v)
        
        # Use allclose for floating point comparison
        assert np.allclose(normalized_v, normalized_again)
    
    def test_compute_distance_cosine(self, operations):
        """Test cosine distance computation."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        distance = operations.compute_distance(v1, v2, metric="cosine")
        
        assert isinstance(distance, float)
        assert 0.0 <= distance <= 2.0  # Cosine distance is 1 - similarity
    
    def test_compute_distance_euclidean(self, operations):
        """Test Euclidean distance computation."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        distance = operations.compute_distance(v1, v2, metric="euclidean")
        
        assert isinstance(distance, float)
        assert distance >= 0.0
    
    def test_compute_distance_jaccard(self, operations):
        """Test Jaccard distance computation."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        distance = operations.compute_distance(v1, v2, metric="jaccard")
        
        assert isinstance(distance, float)
        assert 0.0 <= distance <= 1.0
    
    def test_compute_distance_invalid_metric(self, operations):
        """Test distance computation with invalid metric."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        with pytest.raises(ValueError):
            operations.compute_distance(v1, v2, metric="invalid")
    
    def test_project_to_hypercube(self, operations):
        """Test projection to hypercube."""
        v = np.random.randn(8) * 2
        
        projected = operations.project_to_hypercube(v)
        
        assert isinstance(projected, np.ndarray)
        assert len(projected) == 8
        assert np.all(projected >= -1)
        assert np.all(projected <= 1)
    
    def test_project_to_hypercube_already_in_range(self, operations):
        """Test projection for vector already in range."""
        v = np.random.uniform(-1, 1, 8)
        
        projected = operations.project_to_hypercube(v)
        
        assert np.array_equal(v, projected)
    
    def test_compute_euclidean_distance(self, operations):
        """Test Euclidean distance computation."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        distance = operations.compute_euclidean_distance(v1, v2)
        
        assert isinstance(distance, float)
        assert distance >= 0.0
    
    def test_compute_euclidean_distance_same_vector(self, operations):
        """Test Euclidean distance with same vector."""
        v = np.random.randn(8)
        
        distance = operations.compute_euclidean_distance(v, v)
        
        assert distance == 0.0
    
    def test_normalize_to_unit_sphere(self, operations):
        """Test normalization to unit sphere."""
        v = np.random.randn(8) * 2
        
        normalized = operations.normalize_to_unit_sphere(v)
        
        assert isinstance(normalized, np.ndarray)
        assert len(normalized) == 8
        assert abs(np.linalg.norm(normalized) - 1.0) < 1e-6
    
    def test_normalize_to_unit_sphere_zero_vector(self, operations):
        """Test normalization to unit sphere for zero vector."""
        zero_vector = np.zeros(8)
        
        normalized = operations.normalize_to_unit_sphere(zero_vector)
        
        assert np.array_equal(normalized, zero_vector)
    
    def test_vector_dot_product(self, operations):
        """Test vector dot product."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        dot_product = operations.vector_dot_product(v1, v2)
        
        assert isinstance(dot_product, float)
        
        # Verify with numpy
        expected = np.dot(v1, v2)
        assert np.isclose(dot_product, expected)
    
    def test_vector_dot_product_same_vector(self, operations):
        """Test dot product with same vector."""
        v = np.random.randn(8)
        
        dot_product = operations.vector_dot_product(v, v)
        
        expected = np.dot(v, v)
        assert np.isclose(dot_product, expected)
    
    def test_vector_dot_product_invalid_input_type(self, operations):
        """Test dot product with invalid input type."""
        v1 = [1, 2, 3, 4, 5, 6, 7, 8]  # Not numpy array
        v2 = np.random.randn(8)
        
        # numpy handles list input gracefully
        result = operations.vector_dot_product(v1, v2)
        assert isinstance(result, float)
    
    def test_vector_angle(self, operations):
        """Test angle calculation."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        angle = operations.vector_angle(v1, v2)
        
        assert isinstance(angle, float)
        assert 0.0 <= angle <= np.pi
    
    def test_vector_angle_same_vector(self, operations):
        """Test angle with same vector."""
        v = np.random.randn(8)
        
        angle = operations.vector_angle(v, v)
        
        assert angle == 0.0
    
    def test_vector_angle_orthogonal_vectors(self, operations):
        """Test angle with orthogonal vectors."""
        # Create truly orthogonal vectors
        v1 = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        v2 = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        
        angle = operations.vector_angle(v1, v2)
        
        # Orthogonal vectors should have angle close to 90 degrees (pi/2 radians)
        assert abs(angle - np.pi/2) < 0.001  # Close to 90 degrees
    
    def test_vector_angle_zero_vector(self, operations):
        """Test angle with zero vector."""
        v1 = np.random.randn(8)
        zero_vector = np.zeros(8)
        
        angle = operations.vector_angle(v1, zero_vector)
        
        assert angle == 0.0
    
    def test_vector_angle_invalid_input_type(self, operations):
        """Test angle with invalid input type."""
        v1 = [1, 2, 3, 4, 5, 6, 7, 8]  # Not numpy array
        v2 = np.random.randn(8)
        
        # numpy handles list input gracefully
        angle = operations.vector_angle(v1, v2)
        assert isinstance(angle, float)


class TestIntegration:
    """Integration tests for tensor operations."""
    
    def test_embed_and_similarity(self):
        """Test embedding followed by similarity calculation."""
        operations = TensorOperations()
        
        # Create embeddings
        text1 = "first concept"
        text2 = "second concept"
        
        embedding1 = operations.embed(text1)
        embedding2 = operations.embed(text2)
        
        # Calculate similarity
        similarity = operations.calculate_cosine_similarity(embedding1, embedding2)
        
        assert isinstance(similarity, float)
        assert -1.0 <= similarity <= 1.0
    
    def test_multiple_similarity_metrics(self):
        """Test all similarity metrics."""
        operations = TensorOperations()
        
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        cosine_sim = operations.calculate_cosine_similarity(v1, v2)
        structural_sim = operations.calculate_structural_similarity(v1, v2)
        temporal_align = operations.calculate_temporal_alignment(v1, v2)
        
        assert -1.0 <= cosine_sim <= 1.0
        assert 0.0 <= structural_sim <= 1.0
        assert 0.0 <= temporal_align <= 1.0
    
    def test_distance_and_similarity_relationship(self):
        """Test relationship between distance and similarity."""
        operations = TensorOperations()
        
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        cosine_sim = operations.calculate_cosine_similarity(v1, v2)
        cosine_dist = operations.compute_distance(v1, v2, metric="cosine")
        
        # Distance should be 1 - similarity
        expected_dist = 1.0 - cosine_sim
        assert np.isclose(cosine_dist, expected_dist)
    
    def test_batch_embedding_generation(self):
        """Test generating multiple embeddings."""
        operations = TensorOperations()
        
        texts = [f"concept {i}" for i in range(10)]
        embeddings = [operations.embed(text) for text in texts]
        
        assert len(embeddings) == 10
        assert all(len(e) == 8 for e in embeddings)
        # Check normalization with tolerance
        assert all(abs(np.linalg.norm(e) - 1.0) < 1e-6 for e in embeddings)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
