"""
Dimensional Processing Core Module

Main orchestrator for 8D dimensional processing.
"""

import numpy as np
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum

from .dimensions.input_sensory import InputSensoryDimension
from .dimensions.internal_state import InternalStateDimension
from .dimensions.conceptual import ConceptualDimension
from .dimensions.temporal import TemporalDimension
from .dimensions.social import SocialDimension
from .dimensions.uncertainty import UncertaintyDimension
from .dimensions.evaluation import EvaluationDimension
from .dimensions.action_output import ActionOutputDimension, ActionPriority


class BranchType(Enum):
    """Types of dimensional branches."""
    DEEPEN = "deepen"
    BROADEN = "broaden"
    REFINE = "refine"
    EXPLORE = "explore"


class DimensionalProcessingCore:
    """
    Core 8D dimensional processing engine.
    
    Orchestrates processing across all 8 dimensions,
    manages dimensional branching, and coordinates
    the intelligence cycle.
    
    Attributes:
        dimensions: List of dimension processors
    """
    
    def __init__(self):
        """Initialize the dimensional processing core."""
        self._dimensions = [
            InputSensoryDimension(),
            InternalStateDimension(),
            ConceptualDimension(),
            TemporalDimension(),
            SocialDimension(),
            UncertaintyDimension(),
            EvaluationDimension(),
            ActionOutputDimension(),
        ]
        self._current_embedding: Optional[np.ndarray] = None
        self._branch_history: List[Dict[str, Any]] = []
    
    def process_perception(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process perception data through all dimensions.
        
        Args:
            perception: Perception data with query, embedding, features
        
        Returns:
            Dictionary with dimension processing results
        """
        # Prepare input data for dimensions
        input_data = {
            "query": perception.get("query") or "",
            "embedding": perception.get("embedding", np.zeros(8)),
            "features": perception.get("features", {}),
            "context": perception.get("context", {}),
            "metadata": perception.get("metadata", {}),
            "cognitive_load": 0.5,
            "attention_allocation": {},
            "resource_usage": {},
            "concepts": perception.get("concepts", []),
            "events": perception.get("events", []),
            "interactions": perception.get("interactions", []),
            "cultural_context": perception.get("cultural_context", {}),
            "predictions": perception.get("predictions", []),
            "observations": perception.get("observations", []),
            "priority": ActionPriority.MEDIUM,
        }
        
        # Process all dimensions
        return self.process_all_dimensions(input_data)
    
    def process_dimension(self, dimension_idx: int, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input through a specific dimension.
        
        Args:
            dimension_idx: Dimension index (0-7)
            input_data: Input data for processing
        
        Returns:
            Dictionary with dimension processing results
        """
        if dimension_idx < 0 or dimension_idx >= len(self._dimensions):
            raise ValueError(f"Invalid dimension index: {dimension_idx}")
        
        dimension = self._dimensions[dimension_idx]
        
        # Process based on dimension type
        if isinstance(dimension, InputSensoryDimension):
            result = dimension.process_input(
                list(input_data.values()),
                input_data.get("metadata", {}),
            )
        elif isinstance(dimension, InternalStateDimension):
            result = dimension.update_state(
                input_data.get("cognitive_load", 0.5),
                input_data.get("attention_allocation", {}),
                input_data.get("resource_usage", {}),
            )
        elif isinstance(dimension, ConceptualDimension):
            result = dimension.process_concepts(
                list(input_data.get("concepts", [])),
                input_data.get("context", {}),
            )
        elif isinstance(dimension, TemporalDimension):
            events = input_data.get("events", [])
            result = dimension.analyze_sequence(events)
        elif isinstance(dimension, SocialDimension):
            result = dimension.analyze_social_context(
                input_data.get("interactions", []),
                input_data.get("cultural_context", {}),
            )
        elif isinstance(dimension, UncertaintyDimension):
            result = dimension.quantify_uncertainty(
                input_data.get("predictions", []),
                input_data.get("observations", []),
            )
        elif isinstance(dimension, EvaluationDimension):
            result = dimension.evaluate(input_data)
        elif isinstance(dimension, ActionOutputDimension):
            priority = input_data.get("priority", ActionPriority.MEDIUM)
            result = dimension.generate_action(input_data, priority)
        else:
            raise ValueError(f"Unknown dimension type: {type(dimension)}")
        
        return result
    
    def process_all_dimensions(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input through all 8 dimensions.
        
        Args:
            input_data: Input data for processing
        
        Returns:
            Dictionary with all dimension results
        """
        results = {}
        embeddings = []
        
        for idx, dimension in enumerate(self._dimensions):
            result = self.process_dimension(idx, input_data)
            results[f"dimension_{idx}"] = result
            
            if "embedding" in result:
                embeddings.append(result["embedding"])
        
        # Aggregate embeddings
        if embeddings:
            aggregated = self._aggregate_embeddings(embeddings)
            self._current_embedding = aggregated
        
        return {
            "all_results": results,
            "aggregated_embedding": aggregated.tolist() if isinstance(aggregated, np.ndarray) else aggregated,
        }
    
    def _aggregate_embeddings(self, embeddings: List[np.ndarray]) -> np.ndarray:
        """
        Aggregate multiple embeddings.
        
        Args:
            embeddings: List of embeddings
        
        Returns:
            Aggregated embedding
        """
        if not embeddings:
            return np.zeros(8)
        
        # Average embeddings
        aggregated = np.mean(embeddings, axis=0)
        
        # Normalize
        norm = np.linalg.norm(aggregated)
        if norm > 0:
            aggregated = aggregated / norm
        
        return aggregated
    
    def branch_exploration(
        self,
        current_state: Dict[str, Any],
        branch_type: BranchType = BranchType.EXPLORE,
    ) -> List[Dict[str, Any]]:
        """
        Generate dimensional branches for exploration.
        
        Args:
            current_state: Current processing state
            branch_type: Type of branching
        
        Returns:
            List of branch options
        """
        branches = []
        
        for i, dimension in enumerate(self._dimensions):
            branch = {
                "dimension": i,
                "type": branch_type.value,
                "modification": self._generate_dimension_modification(
                    dimension, current_state, branch_type
                ),
            }
            branches.append(branch)
        
        return branches
    
    def _generate_dimension_modification(
        self,
        dimension,
        current_state: Dict[str, Any],
        branch_type: BranchType,
    ) -> Dict[str, Any]:
        """
        Generate a modification for a dimension.
        
        Args:
            dimension: Dimension processor
            current_state: Current state
            branch_type: Branch type
        
        Returns:
            Modification dictionary
        """
        if branch_type == BranchType.DEEPEN:
            return {"strategy": "increase_precision", "parameters": {"threshold": 0.8}}
        elif branch_type == BranchType.BROADEN:
            return {"strategy": "increase_diversity", "parameters": {"threshold": 0.3}}
        elif branch_type == BranchType.REFINE:
            return {"strategy": "optimize_clarity", "parameters": {"weight": 1.5}}
        else:
            return {"strategy": "explore_variants", "parameters": {"count": 3}}
    
    def get_current_embedding(self) -> Optional[np.ndarray]:
        """
        Get current aggregated embedding.
        
        Returns:
            Current embedding or None
        """
        return self._current_embedding
    
    def set_embedding(self, embedding: np.ndarray) -> None:
        """
        Set current embedding.
        
        Args:
            embedding: New embedding
        """
        self._current_embedding = embedding
    
    def normalize(self) -> None:
        """Normalize current embedding."""
        if self._current_embedding is not None:
            norm = np.linalg.norm(self._current_embedding)
            if norm > 0:
                self._current_embedding = self._current_embedding / norm
    
    def get_dimension_states(self) -> List[Dict[str, Any]]:
        """
        Get states of all dimensions.
        
        Returns:
            List of dimension states
        """
        states = []
        
        for dimension in self._dimensions:
            state = {}
            
            if isinstance(dimension, InputSensoryDimension):
                state = {"type": "input_sensory", "sensitivity": dimension.sensitivity}
            elif isinstance(dimension, InternalStateDimension):
                state = dimension.get_state()
            elif isinstance(dimension, ConceptualDimension):
                state = {"type": "conceptual", "abstraction_level": dimension.abstraction_level}
            elif isinstance(dimension, TemporalDimension):
                state = {"type": "temporal", "time_window": dimension.time_window}
            elif isinstance(dimension, SocialDimension):
                state = {"type": "social", "sensitivity": dimension.cultural_sensitivity}
            elif isinstance(dimension, UncertaintyDimension):
                state = {"type": "uncertainty", "threshold": dimension.confidence_threshold}
            elif isinstance(dimension, EvaluationDimension):
                state = {"type": "evaluation", "criteria_count": len(dimension.evaluation_criteria)}
            elif isinstance(dimension, ActionOutputDimension):
                state = {"type": "action_output", "priority": dimension.default_priority.value}
            
            states.append(state)
        
        return states
    
    def process_perception(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process perception data through all dimensions.
        
        Args:
            perception: Perception data with query, embedding, features
        
        Returns:
            Dictionary with dimension processing results
        """
        # Prepare input data for dimensions
        input_data = {
            "query": perception.get("query") or "",
            "embedding": perception.get("embedding", np.zeros(8)),
            "features": perception.get("features", {}),
            "context": perception.get("context", {}),
            "metadata": perception.get("metadata", {}),
            "cognitive_load": 0.5,
            "attention_allocation": {},
            "resource_usage": {},
            "concepts": perception.get("concepts", []),
            "events": perception.get("events", []),
            "interactions": perception.get("interactions", []),
            "cultural_context": perception.get("cultural_context", {}),
            "predictions": perception.get("predictions", []),
            "observations": perception.get("observations", []),
            "priority": ActionPriority.MEDIUM,
        }
        
        # Process all dimensions
        return self.process_all_dimensions(input_data)
    
    def __repr__(self) -> str:
        return "DimensionalProcessingCore(8_dimensions)"
    
    def __str__(self) -> str:
        return self.__repr__()
