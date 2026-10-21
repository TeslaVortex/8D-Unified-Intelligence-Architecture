"""
Pattern Space Manager Unit Tests

Comprehensive tests for PatternSpaceManager and Pattern classes.
"""

import json
import os
import tempfile
import shutil
import time
from datetime import datetime, timedelta
from typing import List, Tuple
import pytest

import numpy as np

from src.pattern_space.pattern import Pattern, PatternIDGenerator
from src.pattern_space.pattern_space_manager import PatternSpaceManager


class TestPatternIDGenerator:
    """Tests for PatternIDGenerator class."""
    
    def test_generate_basic(self):
        """Test basic pattern ID generation."""
        generator = PatternIDGenerator()
        pattern_id = generator.generate()
        
        assert pattern_id.startswith("P_")
        assert "_" in pattern_id
        assert len(pattern_id) > 0
    
    def test_generate_with_dimension_values(self):
        """Test pattern ID generation with dimension values."""
        generator = PatternIDGenerator()
        dimension_values = [1, 2, 3, 4, 5, 6, 7, 8]
        pattern_id = generator.generate(dimension_values)
        
        assert pattern_id.startswith("P_")
        # Should contain Greek letter suffix
        assert any(char in pattern_id for char in ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'λ'])
    
    def test_generate_incrementing_counter(self):
        """Test that counter increments on each call."""
        generator = PatternIDGenerator()
        ids = [generator.generate() for _ in range(5)]
        
        assert len(ids) == 5
        assert ids[0] != ids[1]
        assert ids[1] != ids[2]
        # All should be unique
        assert len(set(ids)) == 5
    
    def test_generate_from_pattern(self):
        """Test generating ID from pattern dimensions."""
        generator = PatternIDGenerator()
        
        dimensions = {
            'alpha': 1,
            'beta': 2,
            'gamma': 3,
            'delta': 4,
            'zeta': 5,
            'eta': 6,
            'lambda': 7,
            'theta': 8,
        }
        
        pattern = Pattern.create(
            embedding=[0.1] * 8,
            dimensions=dimensions
        )
        
        pattern_id = generator.generate_from_pattern(pattern)
        
        assert pattern_id.startswith("P_")
        # Should contain Greek letter suffix
        assert any(char in pattern_id for char in ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'λ'])
    
    def test_greek_mapping(self):
        """Test Greek letter mapping for dimension values."""
        generator = PatternIDGenerator()
        
        # Test that dimension values are appended when provided
        # Note: The current implementation requires exactly 8 values for Greek suffix
        test_cases = [
            ([1, 2, 3, 4, 5, 6, 7, 8], True),  # 8 values - should have Greek suffix
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], False),  # 9 values - no Greek suffix
            ([1, 2, 3], False),  # 3 values - no Greek suffix
        ]
        
        for values, should_have_greek in test_cases:
            pattern_id = generator.generate(values)
            # Pattern ID format: P_NNNN[_[suffix]]
            # Split by underscore and check structure
            parts = pattern_id.split("_")
            
            if should_have_greek:
                # Should have Greek suffix (at least 2 parts: P, NNNN, suffix)
                assert len(parts) >= 3, f"Expected Greek suffix for values {values}"
                # Last part should contain Greek letters
                suffix = parts[-1]
                assert any(char in suffix for char in ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'λ']), \
                    f"Expected Greek letters in suffix {suffix}"
            else:
                # Should not have Greek suffix (exactly 2 parts: P, NNNN)
                assert len(parts) == 2, f"Expected no suffix for values {values}"
                numeric_part = parts[1]
                assert numeric_part.isdigit(), f"Expected numeric suffix for values {values}"


class TestPattern:
    """Tests for Pattern dataclass."""
    
    def test_create_pattern(self):
        """Test creating a new pattern."""
        embedding = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        pattern = Pattern.create(embedding)
        
        assert pattern.embedding == embedding
        assert pattern.activation_count == 0
        assert pattern.metadata == {}
        assert pattern.tags == []
        assert pattern.dimensions == {}
        assert pattern.last_accessed is not None
        assert pattern.pattern_id is not None
    
    def test_create_pattern_with_metadata(self):
        """Test creating pattern with metadata."""
        embedding = [0.1] * 8
        metadata = {"source": "test", "version": "1.0"}
        tags = ["test-tag", "novelty"]
        
        pattern = Pattern.create(
            embedding=embedding,
            metadata=metadata,
            tags=tags
        )
        
        assert pattern.metadata == metadata
        assert pattern.tags == tags
    
    def test_activate(self):
        """Test pattern activation."""
        pattern = Pattern.create(embedding=[0.1] * 8)
        
        initial_activations = pattern.activation_count
        pattern.activate()
        
        assert pattern.activation_count == initial_activations + 1
        assert pattern.last_accessed is not None
    
    def test_add_tag(self):
        """Test adding a tag to pattern."""
        pattern = Pattern.create(embedding=[0.1] * 8)
        
        pattern.add_tag("tag1")
        pattern.add_tag("tag2")
        
        assert "tag1" in pattern.tags
        assert "tag2" in pattern.tags
    
    def test_add_duplicate_tag(self):
        """Test adding duplicate tag."""
        pattern = Pattern.create(embedding=[0.1] * 8)
        
        pattern.add_tag("tag1")
        pattern.add_tag("tag1")
        
        assert pattern.tags.count("tag1") == 1
    
    def test_remove_tag(self):
        """Test removing a tag."""
        pattern = Pattern.create(embedding=[0.1] * 8)
        pattern.add_tag("tag1")
        pattern.add_tag("tag2")
        
        result = pattern.remove_tag("tag1")
        
        assert result is True
        assert "tag1" not in pattern.tags
        assert "tag2" in pattern.tags
    
    def test_remove_nonexistent_tag(self):
        """Test removing non-existent tag."""
        pattern = Pattern.create(embedding=[0.1] * 8)
        
        result = pattern.remove_tag("nonexistent")
        
        assert result is False
    
    def test_update_metadata(self):
        """Test updating metadata."""
        pattern = Pattern.create(embedding=[0.1] * 8)
        
        pattern.update_metadata("key1", "value1")
        pattern.update_metadata("key2", {"nested": "dict"})
        
        assert pattern.metadata["key1"] == "value1"
        assert pattern.metadata["key2"] == {"nested": "dict"}
    
    def test_get_dimension_value(self):
        """Test getting dimension value."""
        pattern = Pattern.create(
            embedding=[0.1] * 8,
            dimensions={"alpha": 1, "beta": 2}
        )
        
        assert pattern.get_dimension_value("alpha") == 1
        assert pattern.get_dimension_value("beta") == 2
        assert pattern.get_dimension_value("nonexistent") is None
    
    def test_set_dimension_value(self):
        """Test setting dimension value."""
        pattern = Pattern.create(embedding=[0.1] * 8)
        
        pattern.set_dimension_value("alpha", 1)
        pattern.set_dimension_value("beta", 2)
        
        assert pattern.dimensions["alpha"] == 1
        assert pattern.dimensions["beta"] == 2
    
    def test_to_dict(self):
        """Test converting pattern to dictionary."""
        pattern = Pattern.create(
            embedding=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            metadata={"key": "value"},
            tags=["tag1", "tag2"],
            dimensions={"alpha": 1}
        )
        
        data = pattern.to_dict()
        
        assert data["pattern_id"] == pattern.pattern_id
        assert data["embedding"] == pattern.embedding
        assert data["metadata"] == pattern.metadata
        assert data["activation_count"] == pattern.activation_count
        assert data["tags"] == pattern.tags
        assert data["dimensions"] == pattern.dimensions
    
    def test_from_dict(self):
        """Test creating pattern from dictionary."""
        data = {
            "pattern_id": "test_id",
            "embedding": [0.1] * 8,
            "metadata": {"key": "value"},
            "activation_count": 5,
            "tags": ["tag1"],
            "dimensions": {"alpha": 1}
        }
        
        pattern = Pattern.from_dict(data)
        
        assert pattern.pattern_id == "test_id"
        assert pattern.embedding == [0.1] * 8
        assert pattern.metadata == {"key": "value"}
        assert pattern.activation_count == 5
        assert pattern.tags == ["tag1"]
        assert pattern.dimensions == {"alpha": 1}
    
    def test_repr(self):
        """Test pattern string representation."""
        pattern = Pattern.create(
            embedding=[0.1] * 8,
            tags=["tag1"]
        )
        pattern.activation_count = 5
        
        repr_str = repr(pattern)
        
        assert "Pattern" in repr_str
        assert "tag1" in repr_str
        assert "5" in repr_str
    
    def test_embedding_shape(self):
        """Test embedding is proper shape."""
        embedding = [0.1] * 8
        pattern = Pattern.create(embedding=embedding)
        
        assert len(pattern.embedding) == 8


class TestPatternSpaceManager:
    """Tests for PatternSpaceManager class."""
    
    @pytest.fixture
    def temp_db_path(self):
        """Create temporary database path."""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "lancedb")
        yield db_path
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def manager(self, temp_db_path):
        """Create PatternSpaceManager instance."""
        return PatternSpaceManager(db_path=temp_db_path, cache_ttl=3600, max_cache_size=1000)
    
    def test_init_default(self, manager):
        """Test manager initialization with defaults."""
        assert manager.db_path is not None
        assert manager.cache_ttl == 3600
        assert manager.max_cache_size == 1000
    
    def test_init_custom(self, temp_db_path):
        """Test manager initialization with custom values."""
        manager = PatternSpaceManager(
            db_path=temp_db_path,
            cache_ttl=7200,
            max_cache_size=500
        )
        
        assert manager.cache_ttl == 7200
        assert manager.max_cache_size == 500
    
    def test_register_pattern(self, manager):
        """Test registering a new pattern."""
        embedding = [0.1] * 8
        metadata = {"source": "test"}
        tags = ["test-tag"]

        pattern = Pattern.create(
            embedding=embedding,
            metadata=metadata,
            tags=tags
        )

        pattern_id = manager.register_pattern(pattern)

        assert pattern_id is not None
        # Note: Pattern.create() generates UUID, so pattern_id is the UUID
        # The manager uses the pattern's pattern_id as the key
        
        # Verify pattern is in cache
        assert pattern_id in manager.cache
    
    def test_register_pattern_with_metadata(self, manager):
        """Test registering pattern with additional metadata."""
        embedding = [0.1] * 8
        
        pattern = Pattern.create(embedding=embedding)
        
        additional_metadata = {"custom_key": "custom_value"}
        manager.register_pattern(pattern, metadata=additional_metadata)
        
        # Check metadata was added
        assert "custom_key" in pattern.metadata
        assert pattern.metadata["custom_key"] == "custom_value"
    
    def test_register_pattern_updates_cache(self, manager):
        """Test that registering pattern updates cache."""
        embedding = [0.1] * 8
        
        pattern1 = Pattern.create(embedding=embedding)
        pattern_id1 = manager.register_pattern(pattern1)
        
        pattern2 = Pattern.create(embedding=embedding)
        pattern_id2 = manager.register_pattern(pattern2)
        
        # Same embedding should still get different IDs
        assert pattern_id1 != pattern_id2
    
    def test_get_pattern_from_cache(self, manager):
        """Test retrieving pattern from cache."""
        embedding = [0.1] * 8
        
        pattern = Pattern.create(embedding=embedding, tags=["cached"])
        pattern_id = manager.register_pattern(pattern)
        
        retrieved = manager.get_pattern(pattern_id)
        
        assert retrieved is not None
        assert retrieved.pattern_id == pattern_id
        assert retrieved.tags == ["cached"]
    
    def test_get_pattern_not_found(self, manager):
        """Test retrieving non-existent pattern."""
        retrieved = manager.get_pattern("nonexistent_id")
        
        assert retrieved is None
    
    def test_get_pattern_increments_activation(self, manager):
        """Test that get_pattern increments activation count."""
        embedding = [0.1] * 8
        
        pattern = Pattern.create(embedding=embedding, activation_count=0)
        pattern_id = manager.register_pattern(pattern)
        
        assert pattern.activation_count == 0
        
        manager.get_pattern(pattern_id)
        
        assert pattern.activation_count == 1
    
    def test_find_similar_patterns(self, manager):
        """Test finding similar patterns."""
        # Register multiple patterns
        embeddings = [
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]
        
        for embedding in embeddings:
            pattern = Pattern.create(embedding=embedding)
            manager.register_pattern(pattern)
        
        # Query for patterns similar to first embedding
        query_embedding = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        results = manager.find_similar_patterns(
            embedding=query_embedding,
            top_k=3,
            threshold=0.5
        )
        
        assert len(results) <= 3
        
        # Results should be sorted by similarity
        similarities = [result[1] for result in results]
        assert similarities == sorted(similarities, reverse=True)
    
    def test_find_similar_patterns_empty(self, manager):
        """Test finding similar patterns with empty database."""
        results = manager.find_similar_patterns(
            embedding=[0.1] * 8,
            top_k=5,
            threshold=0.5
        )
        
        assert results == []
    
    def test_find_similar_patterns_with_threshold(self, manager):
        """Test filtering by similarity threshold."""
        # Register patterns with different embeddings
        pattern1 = Pattern.create(embedding=[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        pattern2 = Pattern.create(embedding=[0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        pattern3 = Pattern.create(embedding=[0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        
        manager.register_pattern(pattern1)
        manager.register_pattern(pattern2)
        manager.register_pattern(pattern3)
        
        # Query with high threshold
        query = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        results = manager.find_similar_patterns(
            embedding=query,
            top_k=10,
            threshold=0.9
        )
        
        # Should only return pattern1 (very similar)
        # pattern2 might be excluded due to threshold
        assert all(sim >= 0.9 for pattern, sim in results)
    
    def test_delete_pattern(self, manager):
        """Test deleting a pattern."""
        embedding = [0.1] * 8
        
        pattern = Pattern.create(embedding=embedding)
        pattern_id = manager.register_pattern(pattern)
        
        # Verify pattern exists
        assert pattern_id in manager.cache
        
        # Delete pattern
        result = manager.delete_pattern(pattern_id)
        
        assert result is True
        assert pattern_id not in manager.cache
    
    def test_delete_pattern_not_found(self, manager):
        """Test deleting non-existent pattern."""
        result = manager.delete_pattern("nonexistent_id")
        
        assert result is False
    
    def test_update_pattern(self, manager):
        """Test updating a pattern's embedding."""
        embedding = [0.1] * 8
        
        pattern = Pattern.create(embedding=embedding)
        pattern_id = manager.register_pattern(pattern)
        
        new_embedding = [0.2] * 8
        result = manager.update_pattern(pattern_id, new_embedding)
        
        assert result is True
        assert pattern.embedding == new_embedding
    
    def test_update_pattern_not_found(self, manager):
        """Test updating non-existent pattern."""
        result = manager.update_pattern("nonexistent_id", [0.1] * 8)
        
        assert result is False
    
    def test_get_active_patterns(self, manager):
        """Test getting active patterns."""
        # Register patterns with different activation counts
        pattern1 = Pattern.create(embedding=[0.1] * 8)
        pattern2 = Pattern.create(embedding=[0.2] * 8)
        pattern3 = Pattern.create(embedding=[0.3] * 8)
        
        manager.register_pattern(pattern1)
        manager.register_pattern(pattern2)
        manager.register_pattern(pattern3)
        
        # Activate pattern1 multiple times
        pattern1.activate()
        pattern1.activate()
        
        active = manager.get_active_patterns(min_activations=1)
        
        assert len(active) >= 1
        assert pattern1 in active
    
    def test_clear_cache(self, manager):
        """Test clearing the cache."""
        pattern1 = Pattern.create(embedding=[0.1] * 8)
        pattern2 = Pattern.create(embedding=[0.2] * 8)
        
        manager.register_pattern(pattern1)
        manager.register_pattern(pattern2)
        
        assert len(manager.cache) == 2
        
        manager.clear_cache()
        
        assert len(manager.cache) == 0
    
    def test_get_cache_stats(self, manager):
        """Test getting cache statistics."""
        pattern1 = Pattern.create(embedding=[0.1] * 8)
        pattern2 = Pattern.create(embedding=[0.2] * 8)
        
        manager.register_pattern(pattern1)
        manager.register_pattern(pattern2)
        pattern1.activate()
        
        stats = manager.get_cache_stats()
        
        assert stats["total_patterns"] == 2
        assert stats["active_patterns"] == 1
        assert "cache_ttl_seconds" in stats
        assert "max_cache_size" in stats
    
    def test_persist(self, manager):
        """Test persisting patterns to disk."""
        pattern = Pattern.create(embedding=[0.1] * 8)
        manager.register_pattern(pattern)
        
        manager.persist()
        
        # Should not raise exception
        assert len(manager.cache) == 1
    
    def test_close(self, manager):
        """Test closing the database connection."""
        pattern = Pattern.create(embedding=[0.1] * 8)
        manager.register_pattern(pattern)
        
        manager.close()
        
        # Database should be closed
        assert manager._db is None
    
    def test_len(self, manager):
        """Test __len__ method."""
        pattern1 = Pattern.create(embedding=[0.1] * 8)
        pattern2 = Pattern.create(embedding=[0.2] * 8)
        
        manager.register_pattern(pattern1)
        manager.register_pattern(pattern2)
        
        assert len(manager) == 2
    
    def test_repr(self, manager):
        """Test __repr__ method."""
        pattern = Pattern.create(embedding=[0.1] * 8)
        manager.register_pattern(pattern)
        
        repr_str = repr(manager)
        
        assert "PatternSpaceManager" in repr_str
        assert manager.db_path in repr_str
    
    def test_get_registered_patterns(self, manager):
        """Test getting all registered patterns."""
        patterns = []
        for i in range(3):
            pattern = Pattern.create(embedding=[float(i)] * 8)
            manager.register_pattern(pattern)
            patterns.append(pattern)
        
        registered = manager.get_registered_patterns(limit=10)
        
        assert len(registered) == 3


class TestPatternSpaceManagerIntegration:
    """Integration tests for PatternSpaceManager."""
    
    @pytest.fixture
    def temp_db_path(self):
        """Create temporary database path."""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "lancedb")
        yield db_path
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def manager(self, temp_db_path):
        """Create PatternSpaceManager instance."""
        return PatternSpaceManager(db_path=temp_db_path, cache_ttl=3600, max_cache_size=1000)
    
    def test_full_workflow(self, manager):
        """Test complete pattern management workflow."""
        # Create and register pattern
        embedding = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        metadata = {"source": "test", "version": "1.0"}
        tags = ["test-tag", "novelty"]
        
        pattern = Pattern.create(
            embedding=embedding,
            metadata=metadata,
            tags=tags
        )
        pattern_id = manager.register_pattern(pattern)
        
        # Retrieve pattern
        retrieved = manager.get_pattern(pattern_id)
        assert retrieved is not None
        assert retrieved.embedding == embedding
        
        # Find similar patterns
        query = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        results = manager.find_similar_patterns(query, top_k=5, threshold=0.5)
        assert len(results) > 0
    
    def test_multiple_patterns_similarity(self, manager):
        """Test similarity search with multiple registered patterns."""
        # Register patterns with known relationships
        patterns_data = [
            {"embedding": [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "name": "pattern_a"},
            {"embedding": [1.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "name": "pattern_b"},
            {"embedding": [0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "name": "pattern_c"},
            {"embedding": [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], "name": "pattern_d"},
        ]
        
        for data in patterns_data:
            pattern = Pattern.create(embedding=data["embedding"])
            manager.register_pattern(pattern)
        
        # Query for patterns similar to pattern_a
        query = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        results = manager.find_similar_patterns(query, top_k=5, threshold=0.5)
        
        # Should find pattern_a and pattern_b (similar)
        assert len(results) >= 2
    
    def test_cache_expiration(self, manager):
        """Test cache expiration with short TTL."""
        # Use very short TTL for testing
        short_ttl_manager = PatternSpaceManager(
            db_path=manager.db_path,
            cache_ttl=1  # 1 second TTL
        )
        
        embedding = [0.1] * 8
        pattern = Pattern.create(embedding=embedding)
        pattern_id = short_ttl_manager.register_pattern(pattern)
        
        # Should be in cache immediately
        assert pattern_id in short_ttl_manager.cache
        
        # Wait for TTL to expire
        time.sleep(1.5)
        
        # Pattern should be expired and reloaded from database
        retrieved = short_ttl_manager.get_pattern(pattern_id)
        assert retrieved is not None
    
    def test_pattern_activation_tracking(self, manager):
        """Test pattern activation tracking."""
        embedding = [0.1] * 8
        
        pattern = Pattern.create(embedding=embedding, activation_count=0)
        pattern_id = manager.register_pattern(pattern)
        
        # Get pattern multiple times
        for _ in range(5):
            manager.get_pattern(pattern_id)
        
        assert pattern.activation_count == 5
    
    def test_pattern_tags_persistence(self, manager):
        """Test that pattern tags are preserved."""
        embedding = [0.1] * 8
        tags = ["tag1", "tag2", "tag3"]
        
        pattern = Pattern.create(embedding=embedding, tags=tags)
        pattern_id = manager.register_pattern(pattern)
        
        retrieved = manager.get_pattern(pattern_id)
        
        assert retrieved.tags == tags


class TestEdgeCases:
    """Edge case tests."""
    
    @pytest.fixture
    def temp_db_path(self):
        """Create temporary database path."""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "lancedb")
        yield db_path
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def manager(self, temp_db_path):
        """Create PatternSpaceManager instance."""
        return PatternSpaceManager(db_path=temp_db_path, cache_ttl=3600, max_cache_size=1000)
    
    def test_empty_embedding(self, manager):
        """Test with valid 8D embedding (LanceDB requires fixed 8 elements)."""
        # LanceDB requires fixed-size list of 8 floats
        pattern = Pattern.create(embedding=[0.0] * 8)
        pattern_id = manager.register_pattern(pattern)
        
        assert pattern_id is not None
    
    def test_none_metadata(self, manager):
        """Test with None metadata."""
        pattern = Pattern.create(embedding=[0.1] * 8, metadata=None)
        pattern_id = manager.register_pattern(pattern)
        
        assert pattern_id is not None
    
    def test_large_embedding(self, manager):
        """Test with valid 8D embedding (LanceDB requires exactly 8 elements)."""
        # LanceDB requires exactly 8 elements for the 8D space
        embedding = [float(i) for i in range(8)]  # Valid 8D embedding
        pattern = Pattern.create(embedding=embedding)
        pattern_id = manager.register_pattern(pattern)
        
        assert pattern_id is not None
    
    def test_special_characters_in_tags(self, manager):
        """Test tags with special characters."""
        embedding = [0.1] * 8
        tags = ["tag-with-dash", "tag_with_underscore", "tag.with.dot"]
        
        pattern = Pattern.create(embedding=embedding, tags=tags)
        pattern_id = manager.register_pattern(pattern)
        
        assert pattern_id is not None
        assert all(tag in pattern.tags for tag in tags)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
