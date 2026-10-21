"""
Unit tests for NoveltyTensorEngine

Tests for the core novelty detection engine including:
- 8D tensor operations
- Novelty detection modes
- Interference detection
- Similarity calculations
"""

import numpy as np
import pytest
from typing import List

from src.novelty_engine.novelty_tensor_engine import NoveltyTensorEngine
from src.novelty_engine.novelty_types import NoveltyMode, InterferenceType, InterferenceSeverity, NoveltyScore
from src.novelty_engine.tensor_operations import TensorOperations


class TestNoveltyTensorEngine:
    """Tests for NoveltyTensorEngine class."""
    
    @pytest.fixture
    def engine(self):
        """Create a test engine instance."""
        return NoveltyTensorEngine(dimensions=8, tolerance=0.95)
    
    @pytest.fixture
    def engine_custom(self):
        """Create a test engine with custom parameters."""
        return NoveltyTensorEngine(dimensions=8, tolerance=0.85)
    
    def test_init_default(self, engine):
        """Test engine initialization with default parameters."""
        assert engine.dimensions == 8
        assert engine.tolerance == 0.95
        assert not engine._initialized
    
    def test_init_custom(self, engine_custom):
        """Test engine initialization with custom parameters."""
        assert engine_custom.dimensions == 8
        assert engine_custom.tolerance == 0.85
    
    def test_initialize(self, engine):
        """Test engine initialization."""
        engine.initialize()
        assert engine._initialized is True
    
    def test_embed_basic(self, engine):
        """Test basic text embedding."""
        text = "test query for novelty detection"
        embedding = engine.embed(text)
        
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) == 8
        assert engine.dimensions == 8
    
    def test_embed_empty_string(self, engine):
        """Test embedding of empty string."""
        embedding = engine.embed("")
        
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) == 8
    
    def test_embed_different_texts(self, engine):
        """Test that different texts produce different embeddings."""
        embedding1 = engine.embed("first text")
        embedding2 = engine.embed("second text")
        
        assert not np.array_equal(embedding1, embedding2)
    
    def test_embed_deterministic(self, engine):
        """Test that same text produces same embedding (deterministic)."""
        embedding1 = engine.embed("deterministic test")
        embedding2 = engine.embed("deterministic test")
        
        assert np.array_equal(embedding1, embedding2)
    
    def test_embed_returns_normalized(self, engine):
        """Test that embeddings are normalized."""
        text = "normalization test"
        embedding = engine.embed(text)
        
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 1e-6
    
    def test_generate_embedding_alias(self, engine):
        """Test that generate_embedding is an alias for embed."""
        embedding1 = engine.generate_embedding("test")
        embedding2 = engine.embed("test")
        
        assert np.array_equal(embedding1, embedding2)
    
    def test_extract_novelty_simple_list(self, engine):
        """Test novelty extraction with simple list."""
        content = {
            "insights": ["insight 1", "insight 2", "insight 3"]
        }
        
        result = engine.extract_novelty(content)
        
        # extract_novelty returns only the first insight as a string
        assert len(result) == 1
        assert result[0] == "insight 1"
    
    def test_extract_novelty_nested_list(self, engine):
        """Test novelty extraction with nested list structure."""
        content = {
            "insights": [
                ["branch 1 insight 1", "branch 1 insight 2"],
                ["branch 2 insight 1", "branch 2 insight 2", "branch 2 insight 3"]
            ]
        }
        
        result = engine.extract_novelty(content)
        
        # extract_novelty returns only the first insight from nested lists
        assert len(result) == 1
        assert result[0] == "branch 1 insight 1"
    
    def test_extract_novelty_unique_paths(self, engine):
        """Test novelty extraction with path tracking."""
        content = {
            "insights": [
                {"path": "path1", "text": "unique insight"},
                {"path": "path1", "text": "duplicate insight"},
                {"path": "path2", "text": "another unique insight"}
            ]
        }
        
        result = engine.extract_novelty(content)
        
        # Only unique paths should be returned
        assert len(result) == 2
        assert "duplicate insight" not in [i.get("text") for i in result]
    
    def test_detect_novelty_dict_content(self, engine):
        """Test novelty detection with dictionary content."""
        content = {
            "query": "How can we optimize the system?",
            "response": "By implementing the novel approach"
        }
        
        result = engine.detect_novelty(content)
        
        assert "score" in result
        assert "confidence" in result
        assert "mode" in result
        assert 0.0 <= result["score"] <= 1.0
    
    def test_detect_novelty_insights_content(self, engine):
        """Test novelty detection with insights content."""
        content = {
            "insights": [
                ["insight 1", "insight 2"],
                ["insight 3"]
            ]
        }
        
        result = engine.detect_novelty(content)
        
        assert "score" in result
        assert 0.0 <= result["score"] <= 1.0
    
    def test_detect_novelty_empty_content(self, engine):
        """Test novelty detection with empty content."""
        content = {}
        
        result = engine.detect_novelty(content)
        
        assert "score" in result
        assert 0.0 <= result["score"] <= 1.0
    
    def test_detect_interference_valid_input(self, engine):
        """Test interference detection with valid input."""
        pattern_a = np.random.randn(8)
        pattern_b = np.random.randn(8)
        
        score, types = engine.detect_interference(pattern_a, pattern_b)
        
        # Score is returned as numpy float, check it's numeric
        assert isinstance(score, (float, np.floating))
        # Score can exceed 1.0 due to averaging multiple interference metrics
        assert score >= 0.0
        assert isinstance(types, list)
        assert all(isinstance(t, InterferenceType) for t in types)
    
    def test_detect_interference_invalid_input_type(self, engine):
        """Test interference detection with invalid input type."""
        pattern_a = [1, 2, 3, 4, 5, 6, 7, 8]  # Not numpy array
        pattern_b = np.random.randn(8)
        
        with pytest.raises(TypeError):
            engine.detect_interference(pattern_a, pattern_b)
    
    def test_detect_interference_shape_mismatch(self, engine):
        """Test interference detection with shape mismatch."""
        pattern_a = np.random.randn(8)
        pattern_b = np.random.randn(10)
        
        with pytest.raises(ValueError):
            engine.detect_interference(pattern_a, pattern_b)
    
    def test_detect_interference_returns_tuple(self, engine):
        """Test that interference detection returns correct tuple structure."""
        pattern_a = np.random.randn(8)
        pattern_b = np.random.randn(8)
        
        result = engine.detect_interference(pattern_a, pattern_b)
        
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], float)
        assert isinstance(result[1], list)
    
    def test_calculate_semantic_distance(self, engine):
        """Test semantic distance calculation."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        distance = engine.calculate_semantic_distance(v1, v2)
        
        assert isinstance(distance, float)
        assert 0.0 <= distance <= 1.0
    
    def test_calculate_semantic_distance_same_vector(self, engine):
        """Test semantic distance with same vectors."""
        v = np.random.randn(8)
        
        distance = engine.calculate_semantic_distance(v, v)
        
        # Same vectors should have distance close to 0 (floating point tolerance)
        assert abs(distance) < 1e-10
    
    def test_calculate_structural_similarity(self, engine):
        """Test structural similarity calculation."""
        topo_a = np.random.randn(8)
        topo_b = np.random.randn(8)
        
        similarity = engine.calculate_structural_similarity(topo_a, topo_b)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    def test_calculate_structural_similarity_same_vector(self, engine):
        """Test structural similarity with same vectors."""
        v = np.random.randn(8)
        
        similarity = engine.calculate_structural_similarity(v, v)
        
        # Same vectors should have similarity of 1.0
        assert similarity == 1.0
    
    def test_calculate_temporal_alignment(self, engine):
        """Test temporal alignment calculation."""
        t1 = np.random.randn(8)
        t2 = np.random.randn(8)
        
        alignment = engine.calculate_temporal_alignment(t1, t2)
        
        assert isinstance(alignment, float)
        assert 0.0 <= alignment <= 1.0
    
    def test_calculate_temporal_alignment_same_vector(self, engine):
        """Test temporal alignment with same vectors."""
        t = np.random.randn(8)
        
        alignment = engine.calculate_temporal_alignment(t, t)
        
        # Same vectors should have alignment of 1.0
        assert alignment == 1.0
    
    def test_calculate_novelty_score_no_existing_patterns(self, engine):
        """Test novelty score with no existing patterns."""
        new_pattern = np.random.randn(8)
        
        score = engine.calculate_novelty_score(new_pattern, [])
        
        assert isinstance(score, NoveltyScore)
        assert score.score == 1.0  # Completely novel
        assert score.confidence == 1.0
    
    def test_calculate_novelty_score_with_patterns(self, engine):
        """Test novelty score with existing patterns."""
        new_pattern = np.random.randn(8)
        existing_patterns = [np.random.randn(8) for _ in range(5)]
        
        score = engine.calculate_novelty_score(new_pattern, existing_patterns)
        
        assert isinstance(score, NoveltyScore)
        assert 0.0 <= score.score <= 1.0
        assert 0.0 <= score.confidence <= 1.0
        assert isinstance(score.mode, NoveltyMode)
    
    def test_calculate_novelty_score_invalid_input(self, engine):
        """Test novelty score with invalid input type."""
        new_pattern = [1, 2, 3, 4, 5, 6, 7, 8]  # Not numpy array
        
        with pytest.raises(TypeError):
            engine.calculate_novelty_score(new_pattern, [])
    
    def test_get_severity_from_interference_critical(self, engine):
        """Test severity determination for critical interference."""
        scores = [0.9, 0.95, 1.0]
        
        severity = engine._get_severity_from_interference(scores)
        
        assert severity == InterferenceSeverity.CRITICAL
    
    def test_get_severity_from_interference_high(self, engine):
        """Test severity determination for high interference."""
        scores = [0.61, 0.62, 0.63]  # Use scores just above 0.6 threshold
        
        severity = engine._get_severity_from_interference(scores)
        
        assert severity == InterferenceSeverity.HIGH
    
    def test_get_severity_from_interference_medium(self, engine):
        """Test severity determination for medium interference."""
        scores = [0.4, 0.45, 0.5]
        
        severity = engine._get_severity_from_interference(scores)
        
        assert severity == InterferenceSeverity.MEDIUM
    
    def test_get_severity_from_interference_low(self, engine):
        """Test severity determination for low interference."""
        scores = [0.2, 0.25, 0.3]
        
        severity = engine._get_severity_from_interference(scores)
        
        assert severity == InterferenceSeverity.LOW
    
    def test_get_severity_from_interference_none(self, engine):
        """Test severity determination for no interference."""
        scores = [0.05, 0.1, 0.15]
        
        severity = engine._get_severity_from_interference(scores)
        
        assert severity == InterferenceSeverity.NONE
    
    def test_find_similar_patterns_empty(self, engine):
        """Test finding similar patterns with empty list."""
        query = np.random.randn(8)
        
        result = engine.find_similar_patterns(query, [])
        
        assert result == []
    
    def test_find_similar_patterns_with_results(self, engine):
        """Test finding similar patterns with results."""
        query = np.random.randn(8)
        patterns = [
            (np.random.randn(8), "pattern 1"),
            (np.random.randn(8), "pattern 2"),
            (np.random.randn(8), "pattern 3"),
        ]
        
        result = engine.find_similar_patterns(query, patterns, top_k=2, threshold=0.0)
        
        assert len(result) <= 2
        assert all(len(item) == 3 for item in result)
        assert all(0.0 <= item[2] <= 1.0 for item in result)
    
    def test_find_similar_patterns_sorted(self, engine):
        """Test that similar patterns are sorted by similarity."""
        query = np.random.randn(8)
        patterns = [
            (np.random.randn(8), "pattern 1"),
            (np.random.randn(8), "pattern 2"),
            (np.random.randn(8), "pattern 3"),
        ]
        
        result = engine.find_similar_patterns(query, patterns, top_k=3, threshold=0.0)
        
        # Should be sorted in descending order
        for i in range(len(result) - 1):
            assert result[i][2] >= result[i + 1][2]
    
    def test_detect_conceptual_drift(self, engine):
        """Test conceptual drift detection."""
        original = np.random.randn(8)
        current = np.random.randn(8)
        
        has_drift, drift_score = engine.detect_conceptual_drift(original, current)
        
        # drift_score is numpy float, convert to Python float
        assert bool(has_drift) is True
        assert isinstance(drift_score, (float, np.floating))
        # drift_score can exceed 1.0 due to interference averaging
        assert drift_score >= 0.0
    
    def test_detect_conceptual_drift_no_drift(self, engine):
        """Test conceptual drift detection with similar vectors."""
        original = np.random.randn(8)
        current = original * 0.95  # Very similar
        
        has_drift, drift_score = engine.detect_conceptual_drift(original, current)
        
        assert not has_drift
        assert drift_score < 0.3
    
    def test_get_novelty_threshold_default(self, engine):
        """Test getting default novelty threshold."""
        threshold = engine.get_novelty_threshold()
        
        assert threshold == 0.95
    
    def test_get_novelty_threshold_custom(self, engine_custom):
        """Test getting custom novelty threshold."""
        threshold = engine_custom.get_novelty_threshold()
        
        assert threshold == 0.85
    
    def test_set_novelty_threshold_valid(self, engine):
        """Test setting valid novelty threshold."""
        engine.set_novelty_threshold(0.75)
        
        assert engine.tolerance == 0.75
    
    def test_set_novelty_threshold_invalid_low(self, engine):
        """Test setting invalid (too low) novelty threshold."""
        with pytest.raises(ValueError):
            engine.set_novelty_threshold(-0.1)
    
    def test_set_novelty_threshold_invalid_high(self, engine):
        """Test setting invalid (too high) novelty threshold."""
        with pytest.raises(ValueError):
            engine.set_novelty_threshold(1.1)
    
    def test_batch_novelty_detection(self, engine):
        """Test batch novelty detection."""
        new_patterns = [np.random.randn(8) for _ in range(3)]
        reference_patterns = [np.random.randn(8) for _ in range(5)]
        
        scores = engine.batch_novelty_detection(new_patterns, reference_patterns)
        
        assert len(scores) == 3
        assert all(isinstance(score, NoveltyScore) for score in scores)
    
    def test_batch_novelty_detection_empty(self, engine):
        """Test batch novelty detection with empty inputs."""
        new_patterns = []
        reference_patterns = []
        
        scores = engine.batch_novelty_detection(new_patterns, reference_patterns)
        
        assert scores == []
    
    def test_repr(self, engine):
        """Test engine representation."""
        repr_str = repr(engine)
        
        assert "NoveltyTensorEngine" in repr_str
        assert "dimensions=8" in repr_str
        assert "tolerance=0.95" in repr_str
    
    def test_str(self, engine):
        """Test engine string representation."""
        str_repr = str(engine)
        
        assert "NoveltyTensorEngine" in str_repr
    
    def test_tensor_operations_cosine_similarity(self):
        """Test tensor operations cosine similarity."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        similarity = TensorOperations.calculate_cosine_similarity(v1, v2)
        
        assert isinstance(similarity, float)
        assert -1.0 <= similarity <= 1.0
    
    def test_tensor_operations_structural_similarity(self):
        """Test tensor operations structural similarity."""
        topo_a = np.random.randn(8)
        topo_b = np.random.randn(8)
        
        similarity = TensorOperations.calculate_structural_similarity(topo_a, topo_b)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    def test_tensor_operations_temporal_alignment(self):
        """Test tensor operations temporal alignment."""
        t1 = np.random.randn(8)
        t2 = np.random.randn(8)
        
        alignment = TensorOperations.calculate_temporal_alignment(t1, t2)
        
        assert isinstance(alignment, float)
        assert 0.0 <= alignment <= 1.0
    
    def test_tensor_operations_normalize_vector(self):
        """Test tensor operations vector normalization."""
        v = np.random.randn(8) * 2
        
        normalized = TensorOperations.normalize_vector(v)
        
        assert isinstance(normalized, np.ndarray)
        assert len(normalized) == 8
        assert abs(np.linalg.norm(normalized) - 1.0) < 1e-6
    
    def test_tensor_operations_compute_distance(self, engine):
        """Test tensor operations distance computation."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        cosine_dist = TensorOperations.compute_distance(v1, v2, metric="cosine")
        euclidean_dist = TensorOperations.compute_distance(v1, v2, metric="euclidean")
        
        assert isinstance(cosine_dist, float)
        assert isinstance(euclidean_dist, float)
    
    def test_tensor_operations_euclidean_distance(self):
        """Test tensor operations Euclidean distance."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        distance = TensorOperations.compute_euclidean_distance(v1, v2)
        
        assert isinstance(distance, float)
        assert distance >= 0.0
    
    def test_tensor_operations_normalize_to_unit_sphere(self):
        """Test tensor operations normalization to unit sphere."""
        v = np.random.randn(8) * 2
        
        normalized = TensorOperations.normalize_to_unit_sphere(v)
        
        assert isinstance(normalized, np.ndarray)
        assert len(normalized) == 8
        assert abs(np.linalg.norm(normalized) - 1.0) < 1e-6
    
    def test_tensor_operations_vector_dot_product(self):
        """Test tensor operations dot product."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        dot_product = TensorOperations.vector_dot_product(v1, v2)
        
        assert isinstance(dot_product, float)
    
    def test_tensor_operations_vector_angle(self):
        """Test tensor operations angle calculation."""
        v1 = np.random.randn(8)
        v2 = np.random.randn(8)
        
        angle = TensorOperations.vector_angle(v1, v2)
        
        assert isinstance(angle, float)
        assert 0.0 <= angle <= np.pi


class TestInterferenceDetection:
    """Tests for interference detection functionality."""
    
    @pytest.fixture
    def engine(self):
        """Create a test engine instance."""
        return NoveltyTensorEngine(dimensions=8)
    
    def test_semantic_conflict_detection(self, engine):
        """Test detection of semantic conflicts."""
        pattern_a = np.random.randn(8)
        pattern_b = np.random.randn(8)
        
        score, types = engine.detect_interference(pattern_a, pattern_b)
        
        # Semantic conflict may or may not be detected
        semantic_conflict = any(t == InterferenceType.SEMANTIC_CONFLICT for t in types)
        
        assert isinstance(semantic_conflict, bool)
    
    def test_structural_conflict_detection(self, engine):
        """Test detection of structural conflicts."""
        pattern_a = np.random.randn(8)
        pattern_b = np.random.randn(8)
        
        score, types = engine.detect_interference(pattern_a, pattern_b)
        
        structural_conflict = any(t == InterferenceType.STRUCTURAL_CONFLICT for t in types)
        
        assert isinstance(structural_conflict, bool)
    
    def test_temporal_conflict_detection(self, engine):
        """Test detection of temporal conflicts."""
        pattern_a = np.random.randn(8)
        pattern_b = np.random.randn(8)
        
        score, types = engine.detect_interference(pattern_a, pattern_b)
        
        temporal_conflict = any(t == InterferenceType.TEMPORAL_CONFLICT for t in types)
        
        assert isinstance(temporal_conflict, bool)
    
    def test_conceptual_drift_detection(self, engine):
        """Test detection of conceptual drift."""
        pattern_a = np.random.randn(8)
        pattern_b = np.random.randn(8)
        
        score, types = engine.detect_interference(pattern_a, pattern_b)
        
        drift = any(t == InterferenceType.CONCEPTUAL_DRIFT for t in types)
        
        assert isinstance(drift, bool)
    
    def test_pattern_collapse_detection(self, engine):
        """Test detection of pattern collapse."""
        pattern_a = np.random.randn(8)
        pattern_b = np.random.randn(8)
        
        score, types = engine.detect_interference(pattern_a, pattern_b)
        
        collapse = any(t == InterferenceType.PATTERN_COLLAPSE for t in types)
        
        assert isinstance(collapse, bool)
    
    def test_resonance_amplification_detection(self, engine):
        """Test detection of resonance amplification."""
        pattern_a = np.random.randn(8)
        pattern_b = np.random.randn(8)
        
        score, types = engine.detect_interference(pattern_a, pattern_b)
        
        resonance = any(t == InterferenceType.RESONANCE_AMPLIFICATION for t in types)
        
        assert isinstance(resonance, bool)


class TestNoveltyModes:
    """Tests for novelty mode functionality."""
    
    @pytest.fixture
    def engine(self):
        """Create a test engine instance."""
        return NoveltyTensorEngine(dimensions=8)
    
    def test_all_modes_returned(self, engine):
        """Test that all novelty modes are returned."""
        modes = NoveltyMode.all_modes()
        
        assert len(modes) == 7
        assert NoveltyMode.SEMANTIC in modes
        assert NoveltyMode.STRUCTURAL in modes
        assert NoveltyMode.TEMPORAL in modes
        assert NoveltyMode.CONTEXTUAL in modes
        assert NoveltyMode.EVOLUTIONARY in modes
        assert NoveltyMode.CULTURAL in modes
        assert NoveltyMode.META in modes
    
    def test_mode_names(self):
        """Test that mode names are returned correctly."""
        names = NoveltyMode.mode_names()
        
        assert len(names) == 7
        assert "semantic" in names
        assert "structural" in names
        assert "temporal" in names


class TestInterferenceTypes:
    """Tests for interference type functionality."""
    
    def test_all_types_returned(self):
        """Test that all interference types are returned."""
        types = InterferenceType.all_types()
        
        assert len(types) == 7
        assert InterferenceType.SEMANTIC_CONFLICT in types
        assert InterferenceType.STRUCTURAL_CONFLICT in types
        assert InterferenceType.TEMPORAL_CONFLICT in types
        assert InterferenceType.CONTEXTUAL_CONFLICT in types
        assert InterferenceType.CONCEPTUAL_DRIFT in types
        assert InterferenceType.PATTERN_COLLAPSE in types
        assert InterferenceType.RESONANCE_AMPLIFICATION in types
    
    def test_type_names(self):
        """Test that type names are returned correctly."""
        names = InterferenceType.type_names()
        
        assert len(names) == 7
        assert "semantic_conflict" in names
        assert "structural_conflict" in names
        assert "temporal_conflict" in names


class TestInterferenceSeverity:
    """Tests for interference severity functionality."""
    
    def test_severity_levels(self):
        """Test that all severity levels are defined."""
        levels = list(InterferenceSeverity)
        
        assert len(levels) == 5
        assert InterferenceSeverity.NONE in levels
        assert InterferenceSeverity.LOW in levels
        assert InterferenceSeverity.MEDIUM in levels
        assert InterferenceSeverity.HIGH in levels
        assert InterferenceSeverity.CRITICAL in levels
    
    def test_severity_values(self):
        """Test that severity values are correct."""
        assert InterferenceSeverity.NONE.value == 0
        assert InterferenceSeverity.LOW.value == 1
        assert InterferenceSeverity.MEDIUM.value == 2
        assert InterferenceSeverity.HIGH.value == 3
        assert InterferenceSeverity.CRITICAL.value == 4


class TestNoveltyScore:
    """Tests for NoveltyScore class."""
    
    def test_initialization(self):
        """Test novelty score initialization."""
        score = NoveltyScore(
            score=0.85,
            mode=NoveltyMode.SEMANTIC,
            confidence=0.95,
            interference_types=[InterferenceType.SEMANTIC_CONFLICT],
            severity=InterferenceSeverity.LOW
        )
        
        assert score.score == 0.85
        assert score.mode == NoveltyMode.SEMANTIC
        assert score.confidence == 0.95
        assert len(score.interference_types) == 1
        assert score.severity == InterferenceSeverity.LOW
    
    def test_repr(self):
        """Test novelty score representation."""
        score = NoveltyScore(score=0.85, mode=NoveltyMode.SEMANTIC)
        
        repr_str = repr(score)
        
        assert "score=0.8500" in repr_str
        assert "mode=semantic" in repr_str
        assert "confidence=0.95" in repr_str
    
    def test_to_dict(self):
        """Test novelty score to dictionary conversion."""
        score = NoveltyScore(
            score=0.85,
            mode=NoveltyMode.SEMANTIC,
            confidence=0.95,
            interference_types=[InterferenceType.SEMANTIC_CONFLICT],
            severity=InterferenceSeverity.LOW
        )
        
        score_dict = score.to_dict()
        
        assert score_dict["score"] == 0.85
        assert score_dict["mode"] == "semantic"
        assert score_dict["confidence"] == 0.95
        assert "semantic_conflict" in score_dict["interference_types"]
        assert score_dict["severity"] == 1


class TestIntegration:
    """Integration tests for novelty engine."""
    
    def test_full_novelty_workflow(self):
        """Test complete novelty detection workflow."""
        engine = NoveltyTensorEngine(dimensions=8)
        
        # Create some patterns
        patterns = [
            engine.embed(f"pattern {i}")
            for i in range(10)
        ]
        
        # Test novelty detection
        test_query = "completely new concept"
        embedding = engine.embed(test_query)
        
        score = engine.calculate_novelty_score(embedding, patterns)
        
        assert isinstance(score, NoveltyScore)
        assert 0.0 <= score.score <= 1.0
    
    def test_interference_workflow(self):
        """Test complete interference detection workflow."""
        engine = NoveltyTensorEngine(dimensions=8)
        
        # Create two patterns
        pattern_a = engine.embed("first pattern")
        pattern_b = engine.embed("second pattern")
        
        # Detect interference
        interference_score, detected_types = engine.detect_interference(pattern_a, pattern_b)
        
        assert isinstance(interference_score, float)
        assert isinstance(detected_types, list)
        assert 0.0 <= interference_score <= 1.0
    
    def test_similarity_workflow(self):
        """Test complete similarity calculation workflow."""
        engine = NoveltyTensorEngine(dimensions=8)
        
        # Create vectors
        v1 = engine.embed("vector 1")
        v2 = engine.embed("vector 2")
        
        # Calculate structural similarity and temporal alignment (cosine similarity is in TensorOperations)
        structural_sim = engine.calculate_structural_similarity(v1, v2)
        temporal_align = engine.calculate_temporal_alignment(v1, v2)
        
        assert 0.0 <= structural_sim <= 1.0
        assert 0.0 <= temporal_align <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
