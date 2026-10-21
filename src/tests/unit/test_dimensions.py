"""
Unit Tests for Dimensional Processing Core

Tests all 8 dimensions and the DimensionalProcessingCore orchestrator.
"""

import pytest
import numpy as np
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dimensions.dimensional_core import DimensionalProcessingCore, BranchType
from dimensions.dimensions.input_sensory import InputSensoryDimension
from dimensions.dimensions.internal_state import InternalStateDimension
from dimensions.dimensions.conceptual import ConceptualDimension
from dimensions.dimensions.temporal import TemporalDimension
from dimensions.dimensions.social import SocialDimension
from dimensions.dimensions.uncertainty import UncertaintyDimension
from dimensions.dimensions.evaluation import EvaluationDimension
from dimensions.dimensions.action_output import ActionOutputDimension, ActionPriority


# ============================================================================
# Input Sensory Dimension Tests (α)
# ============================================================================

class TestInputSensoryDimension:
    """Tests for Input Sensory Dimension (α)."""
    
    def test_init(self):
        """Test initialization."""
        dimension = InputSensoryDimension(sensitivity=0.5)
        assert dimension.sensitivity == 0.5
        assert dimension._embedding is None
    
    def test_process_input_with_strings(self):
        """Test processing string stimuli."""
        dimension = InputSensoryDimension()
        stimuli = ["hello", "world", "test"]
        result = dimension.process_input(stimuli, {"source": "test"})
        
        assert "embedding" in result
        assert "entropy" in result
        assert "features" in result
        assert isinstance(result["embedding"], list)
        assert len(result["embedding"]) == 8
    
    def test_process_input_with_numbers(self):
        """Test processing numeric stimuli."""
        dimension = InputSensoryDimension()
        stimuli = [10.0, 20.0, 30.0]
        result = dimension.process_input(stimuli, {"source": "test"})
        
        assert "embedding" in result
        assert "entropy" in result
        assert "features" in result
    
    def test_empty_stimuli(self):
        """Test processing empty stimuli."""
        dimension = InputSensoryDimension()
        result = dimension.process_input([], {})
        
        assert "embedding" in result
        assert len(result["embedding"]) == 8
    
    def test_embedding_normalization(self):
        """Test that embedding is normalized."""
        dimension = InputSensoryDimension()
        stimuli = ["test", "stimuli"]
        result = dimension.process_input(stimuli, {})
        
        embedding = np.array(result["embedding"])
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 0.01


# ============================================================================
# Internal State Dimension Tests (β)
# ============================================================================

class TestInternalStateDimension:
    """Tests for Internal State Dimension (β)."""
    
    def test_init(self):
        """Test initialization."""
        dimension = InternalStateDimension(state_capacity=1.0)
        assert dimension.state_capacity == 1.0
        assert dimension._current_load == 0.0
    
    def test_update_state(self):
        """Test state update."""
        dimension = InternalStateDimension()
        result = dimension.update_state(
            cognitive_load=0.5,
            attention_allocation={"domain1": 0.3, "domain2": 0.7},
            resource_usage={"cpu": 0.4, "memory": 0.6}
        )
        
        assert "embedding" in result
        assert result["cognitive_load"] == 0.5
        assert len(result["embedding"]) == 8
    
    def test_state_embedding(self):
        """Test state embedding creation."""
        dimension = InternalStateDimension()
        result = dimension.update_state(
            cognitive_load=0.8,
            attention_allocation={"a": 0.5, "b": 0.5},
            resource_usage={"r1": 0.3, "r2": 0.7}
        )
        
        embedding = np.array(result["embedding"])
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 0.01
    
    def test_optimize_attention_allocation(self):
        """Test attention optimization."""
        dimension = InternalStateDimension()
        current = {"domain1": 0.5, "domain2": 0.5}
        target = ["domain1", "domain3"]
        
        optimized = dimension.optimize_attention_allocation(current, target)
        
        assert "domain1" in optimized
        assert "domain3" in optimized
        assert sum(optimized.values()) == 1.0
    
    def test_get_state(self):
        """Test state retrieval."""
        dimension = InternalStateDimension()
        dimension.update_state(0.5, {}, {})
        
        state = dimension.get_state()
        
        assert "cognitive_load" in state
        assert state["cognitive_load"] == 0.5


# ============================================================================
# Conceptual Dimension Tests (γ)
# ============================================================================

class TestConceptualDimension:
    """Tests for Conceptual Abstraction Dimension (γ)."""
    
    def test_init(self):
        """Test initialization."""
        dimension = ConceptualDimension(abstraction_level=3)
        assert dimension.abstraction_level == 3
        assert dimension._concept_embedding is None
    
    def test_process_concepts(self):
        """Test concept processing."""
        dimension = ConceptualDimension()
        inputs = ["machine learning", "artificial intelligence", "neural networks"]
        result = dimension.process_concepts(inputs, {"context": "tech"})
        
        assert "embedding" in result
        assert "concepts" in result
        assert "abstraction_level" in result
        assert "metrics" in result
    
    def test_concept_extraction(self):
        """Test concept extraction."""
        dimension = ConceptualDimension()
        inputs = ["hello world test"]
        result = dimension.process_concepts(inputs, {})
        
        concepts = result["concepts"]
        assert len(concepts) > 0
    
    def test_embedding_normalization(self):
        """Test embedding normalization."""
        dimension = ConceptualDimension()
        inputs = ["test concept"]
        result = dimension.process_concepts(inputs, {})
        
        embedding = np.array(result["embedding"])
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 0.01
    
    def test_abstraction_level_bounds(self):
        """Test abstraction level is bounded."""
        dimension = ConceptualDimension()
        dimension.set_abstraction_level(15)
        assert dimension.abstraction_level == 10
        
        dimension.set_abstraction_level(0)
        assert dimension.abstraction_level == 1


# ============================================================================
# Temporal Dimension Tests (δ)
# ============================================================================

class TestTemporalDimension:
    """Tests for Temporal Context Dimension (δ)."""
    
    def test_init(self):
        """Test initialization."""
        dimension = TemporalDimension(time_window=3600)
        assert dimension.time_window == 3600
        assert dimension._temporal_embedding is None
    
    def test_analyze_sequence(self):
        """Test sequence analysis."""
        dimension = TemporalDimension()
        events = [
            (datetime.now() - timedelta(minutes=1), "event1"),
            (datetime.now() - timedelta(minutes=2), "event2"),
            (datetime.now() - timedelta(minutes=3), "event3"),
        ]
        result = dimension.analyze_sequence(events)
        
        assert "embedding" in result
        assert "metrics" in result
        assert len(result["embedding"]) == 8
    
    def test_empty_sequence(self):
        """Test empty sequence handling."""
        dimension = TemporalDimension()
        result = dimension.analyze_sequence([])
        
        assert "embedding" in result
        assert len(result["embedding"]) == 8
    
    def test_temporal_embedding(self):
        """Test temporal embedding creation."""
        dimension = TemporalDimension()
        events = [
            (datetime.now(), "event1"),
            (datetime.now(), "event2"),
        ]
        result = dimension.analyze_sequence(events)
        
        embedding = np.array(result["embedding"])
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 0.01
    
    def test_update_sequence(self):
        """Test sequence update."""
        dimension = TemporalDimension()
        event = (datetime.now(), "new_event")
        dimension.update_sequence(event)
        
        sequence = dimension.get_sequence()
        assert len(sequence) == 1


# ============================================================================
# Social Dimension Tests (ζ)
# ============================================================================

class TestSocialDimension:
    """Tests for Social/Cultural Dimension (ζ)."""
    
    def test_init(self):
        """Test initialization."""
        dimension = SocialDimension(cultural_sensitivity=0.7)
        assert dimension.cultural_sensitivity == 0.7
        assert dimension._social_embedding is None
    
    def test_analyze_social_context(self):
        """Test social context analysis."""
        dimension = SocialDimension()
        interactions = [
            {"trust": 0.8, "complexity": 0.5},
            {"trust": 0.9, "complexity": 0.7},
        ]
        result = dimension.analyze_social_context(interactions, {"cultures": ["en", "es"]})
        
        assert "embedding" in result
        assert "metrics" in result
        assert len(result["embedding"]) == 8
    
    def test_empty_interactions(self):
        """Test empty interactions handling."""
        dimension = SocialDimension()
        result = dimension.analyze_social_context([], {})
        
        assert "embedding" in result
        assert len(result["embedding"]) == 8
    
    def test_social_embedding_normalization(self):
        """Test embedding normalization."""
        dimension = SocialDimension()
        interactions = [{"trust": 0.5}]
        result = dimension.analyze_social_context(interactions, {})
        
        embedding = np.array(result["embedding"])
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 0.01


# ============================================================================
# Uncertainty Dimension Tests (η)
# ============================================================================

class TestUncertaintyDimension:
    """Tests for Uncertainty Dimension (η)."""
    
    def test_init(self):
        """Test initialization."""
        dimension = UncertaintyDimension(confidence_threshold=0.6)
        assert dimension.confidence_threshold == 0.6
        assert dimension._uncertainty_embedding is None
    
    def test_quantify_uncertainty(self):
        """Test uncertainty quantification."""
        dimension = UncertaintyDimension()
        predictions = [
            {"confidence": 0.9, "outcome": "A"},
            {"confidence": 0.7, "outcome": "B"},
        ]
        result = dimension.quantify_uncertainty(predictions, [])
        
        assert "embedding" in result
        assert "metrics" in result
        assert len(result["embedding"]) == 8
    
    def test_empty_predictions(self):
        """Test empty predictions handling."""
        dimension = UncertaintyDimension()
        result = dimension.quantify_uncertainty([], [])
        
        assert "embedding" in result
        assert len(result["embedding"]) == 8
    
    def test_confidence_assessment(self):
        """Test confidence assessment."""
        dimension = UncertaintyDimension(confidence_threshold=0.5)
        prediction = {"confidence": 0.8}
        
        confidence = dimension.assess_confidence(prediction)
        assert confidence == 0.8
    
    def test_uncertainty_embedding_normalization(self):
        """Test embedding normalization."""
        dimension = UncertaintyDimension()
        predictions = [{"confidence": 0.5}]
        result = dimension.quantify_uncertainty(predictions, [])
        
        embedding = np.array(result["embedding"])
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 0.01


# ============================================================================
# Evaluation Dimension Tests (λ)
# ============================================================================

class TestEvaluationDimension:
    """Tests for Evaluation Dimension (λ)."""
    
    def test_init(self):
        """Test initialization."""
        dimension = EvaluationDimension()
        assert len(dimension.evaluation_criteria) == 4
        assert dimension._evaluation_embedding is None
    
    def test_init_with_custom_criteria(self):
        """Test initialization with custom criteria."""
        custom = {"accuracy": 2.0, "speed": 1.5}
        dimension = EvaluationDimension(evaluation_criteria=custom)
        
        assert dimension.evaluation_criteria == custom
    
    def test_evaluate(self):
        """Test item evaluation."""
        dimension = EvaluationDimension()
        item = {"accuracy": 0.9, "efficiency": 0.8, "novelty": 0.7}
        result = dimension.evaluate(item)
        
        assert "embedding" in result
        assert "scores" in result
        assert "overall_score" in result
        assert len(result["embedding"]) == 8
    
    def test_empty_item(self):
        """Test empty item evaluation."""
        dimension = EvaluationDimension()
        result = dimension.evaluate({})
        
        assert "embedding" in result
        assert len(result["embedding"]) == 8
    
    def test_embedding_normalization(self):
        """Test embedding normalization."""
        dimension = EvaluationDimension()
        item = {"accuracy": 0.5}
        result = dimension.evaluate(item)
        
        embedding = np.array(result["embedding"])
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 0.01
    
    def test_compare_items(self):
        """Test item comparison."""
        dimension = EvaluationDimension()
        item_a = {"accuracy": 0.9}
        item_b = {"accuracy": 0.7}
        
        differences = dimension.compare_items(item_a, item_b)
        
        assert "accuracy_diff" in differences
        assert abs(differences["accuracy_diff"] - 0.2) < 0.001


# ============================================================================
# Action Output Dimension Tests (θ)
# ============================================================================

class TestActionOutputDimension:
    """Tests for Action/Output Dimension (θ)."""
    
    def test_init(self):
        """Test initialization."""
        dimension = ActionOutputDimension(default_priority=ActionPriority.MEDIUM)
        assert dimension.default_priority == ActionPriority.MEDIUM
        assert dimension._action_embedding is None
    
    def test_init_with_high_priority(self):
        """Test initialization with high priority."""
        dimension = ActionOutputDimension(default_priority=ActionPriority.HIGH)
        assert dimension.default_priority == ActionPriority.HIGH
    
    def test_generate_action(self):
        """Test action generation."""
        dimension = ActionOutputDimension()
        context = {"query": "test", "priority": ActionPriority.HIGH}
        result = dimension.generate_action(context, ActionPriority.HIGH)
        
        assert "embedding" in result
        assert "action" in result
        assert result["action"]["priority"] == 3
        assert len(result["embedding"]) == 8
    
    def test_format_output_json(self):
        """Test JSON output formatting."""
        dimension = ActionOutputDimension()
        data = {"key": "value", "number": 42}
        
        output = dimension.format_output(data, "json")
        
        assert isinstance(output, str)
        assert "key" in output
    
    def test_format_output_text(self):
        """Test text output formatting."""
        dimension = ActionOutputDimension()
        data = {"key": "value"}
        
        output = dimension.format_output(data, "text")
        
        assert isinstance(output, str)
        assert "key" in output


# ============================================================================
# DimensionalProcessingCore Tests
# ============================================================================

class TestDimensionalProcessingCore:
    """Tests for DimensionalProcessingCore."""
    
    def test_init(self):
        """Test initialization."""
        core = DimensionalProcessingCore()
        
        assert len(core._dimensions) == 8
        assert core._current_embedding is None
        assert len(core._branch_history) == 0
    
    def test_process_perception(self):
        """Test perception processing."""
        core = DimensionalProcessingCore()
        perception = {
            "query": "test query",
            "embedding": np.zeros(8).tolist(),
            "features": {"count": 1},
        }
        
        result = core.process_perception(perception)
        
        assert "all_results" in result
        assert "aggregated_embedding" in result
        assert len(result["aggregated_embedding"]) == 8
    
    def test_process_all_dimensions(self):
        """Test processing all dimensions."""
        core = DimensionalProcessingCore()
        input_data = {
            "query": "test",
            "embedding": np.zeros(8),
            "concepts": ["test"],
            "events": [],
        }
        
        result = core.process_all_dimensions(input_data)
        
        assert "all_results" in result
        assert "aggregated_embedding" in result
    
    def test_process_single_dimension(self):
        """Test processing a single dimension."""
        core = DimensionalProcessingCore()
        input_data = {
            "query": "test",
            "embedding": np.zeros(8),
            "concepts": [],
            "events": [],
        }
        
        result = core.process_dimension(0, input_data)
        
        assert "embedding" in result
    
    def test_branch_exploration(self):
        """Test branch exploration."""
        core = DimensionalProcessingCore()
        current_state = {"embedding": np.zeros(8).tolist()}
        
        branches = core.branch_exploration(current_state, BranchType.EXPLORE)
        
        assert len(branches) == 8
        assert all("dimension" in b for b in branches)
        assert all("type" in b for b in branches)
    
    def test_branch_types(self):
        """Test different branch types."""
        core = DimensionalProcessingCore()
        state = {"embedding": np.zeros(8).tolist()}
        
        for branch_type in BranchType:
            branches = core.branch_exploration(state, branch_type)
            assert len(branches) == 8
    
    def test_get_current_embedding(self):
        """Test embedding retrieval."""
        core = DimensionalProcessingCore()
        core.set_embedding(np.ones(8) / np.linalg.norm(np.ones(8)))
        
        embedding = core.get_current_embedding()
        assert embedding is not None
        assert len(embedding) == 8
    
    def test_normalize(self):
        """Test embedding normalization."""
        core = DimensionalProcessingCore()
        core.set_embedding(np.ones(8) * 2)
        core.normalize()
        
        embedding = core.get_current_embedding()
        assert embedding is not None
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 0.01
    
    def test_get_dimension_states(self):
        """Test dimension state retrieval."""
        core = DimensionalProcessingCore()
        states = core.get_dimension_states()
        
        assert len(states) == 8
        assert all("type" in s for s in states)


# ============================================================================
# Integration Tests
# ============================================================================

class TestDimensionalIntegration:
    """Integration tests for dimensional processing."""
    
    def test_full_pipeline(self):
        """Test full processing pipeline."""
        core = DimensionalProcessingCore()
        
        # Create test perception
        perception = {
            "query": "test intelligence processing",
            "embedding": np.random.randn(8).tolist(),
            "concepts": ["intelligence", "processing"],
            "events": [
                (datetime.now() - timedelta(minutes=1), "start"),
                (datetime.now() - timedelta(minutes=2), "process"),
            ],
            "interactions": [{"trust": 0.8}],
        }
        
        # Process through all dimensions
        result = core.process_perception(perception)
        
        # Verify results
        assert "all_results" in result
        assert "aggregated_embedding" in result
        assert len(result["aggregated_embedding"]) == 8
        
        # Verify all dimensions processed
        for i in range(8):
            assert f"dimension_{i}" in result["all_results"]
    
    def test_embedding_aggregation(self):
        """Test embedding aggregation and normalization."""
        core = DimensionalProcessingCore()
        input_data = {
            "embedding": np.ones(8),
            "concepts": [],
            "events": [],
        }
        
        result = core.process_all_dimensions(input_data)
        
        embedding = np.array(result["aggregated_embedding"])
        norm = np.linalg.norm(embedding)
        
        assert abs(norm - 1.0) < 0.01


# ============================================================================
# Edge Cases
# ============================================================================

class TestDimensionalEdgeCases:
    """Edge case tests."""
    
    def test_null_inputs(self):
        """Test handling of null/None inputs."""
        core = DimensionalProcessingCore()
        
        perception = {
            "query": None,
            "embedding": None,
            "features": None,
        }
        
        result = core.process_perception(perception)
        
        assert "all_results" in result
        assert "aggregated_embedding" in result
    
    def test_very_long_query(self):
        """Test handling of very long query."""
        core = DimensionalProcessingCore()
        
        perception = {
            "query": "a" * 10000,
            "embedding": np.zeros(8).tolist(),
        }
        
        result = core.process_perception(perception)
        
        assert "all_results" in result
    
    def test_very_short_query(self):
        """Test handling of very short query."""
        core = DimensionalProcessingCore()
        
        perception = {
            "query": "a",
            "embedding": np.zeros(8).tolist(),
        }
        
        result = core.process_perception(perception)
        
        assert "all_results" in result
    
    def test_empty_concepts(self):
        """Test empty concepts list."""
        core = DimensionalProcessingCore()
        
        perception = {
            "query": "test",
            "embedding": np.zeros(8).tolist(),
            "concepts": [],
        }
        
        result = core.process_perception(perception)
        
        assert "all_results" in result
    
    def test_no_events(self):
        """Test processing without events."""
        core = DimensionalProcessingCore()
        
        perception = {
            "query": "test",
            "embedding": np.zeros(8).tolist(),
            "events": [],
        }
        
        result = core.process_perception(perception)
        
        assert "all_results" in result
    
    def test_large_number_of_interactions(self):
        """Test processing with many interactions."""
        core = DimensionalProcessingCore()
        
        interactions = [{"trust": 0.5} for _ in range(100)]
        
        perception = {
            "query": "test",
            "embedding": np.zeros(8).tolist(),
            "interactions": interactions,
        }
        
        result = core.process_perception(perception)
        
        assert "all_results" in result
