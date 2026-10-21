"""
Novelty Tensor Engine Module

Main novelty detection engine for 8D intelligence system.
"""

import numpy as np
from typing import Optional, List, Dict, Any, Tuple
from scipy.spatial.distance import cdist

from .novelty_types import NoveltyMode, InterferenceType, InterferenceSeverity, NoveltyScore
from .tensor_operations import TensorOperations


class NoveltyTensorEngine:
    """
    Core novelty detection engine using 8D tensor analysis.
    
    This engine detects novelty by analyzing interference patterns
    between new inputs and existing patterns in the 8-dimensional space.
    
    Attributes:
        dimensions: Number of dimensions (fixed at 8)
        tolerance: Threshold for considering vectors similar
    """
    
    def __init__(self, dimensions: int = 8, tolerance: float = 0.95):
        """
        Initialize the novelty tensor engine.
        
        Args:
            dimensions: Dimensionality of the tensor space (default: 8)
            tolerance: Similarity threshold for novelty detection (default: 0.95)
        """
        self.dimensions = dimensions
        self.tolerance = tolerance
        self._operations = TensorOperations()
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the engine with any required resources."""
        if not self._initialized:
            self._initialized = True
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate an embedding from text.
        
        Alias for embed method for API consistency.
        
        Args:
            text: Input text to embed
        
        Returns:
            numpy.ndarray: 8D embedding vector
        """
        return self.embed(text)
    
    def embed(self, text: str) -> np.ndarray:
        """
        Create an 8D embedding from text.
        
        Args:
            text: Input text to embed
        
        Returns:
            numpy.ndarray: 8D embedding vector
        """
        return self._operations.embed(text, embedding_dim=self.dimensions)
    
    def extract_novelty(self, content: Dict[str, Any]) -> List[str]:
        """
        Extract novel insights from content.
        
        Args:
            content: Content dictionary with insights (can be list of lists)
        
        Returns:
            List of novel insights
        """
        novel_insights = []
        
        # Handle nested list structure (branches have insights as list of lists)
        insights = content.get("insights", [])
        if isinstance(insights, list) and len(insights) > 0 and isinstance(insights[0], list):
            # Flatten nested lists from branches
            all_insights = []
            for insight_group in insights:
                if isinstance(insight_group, list):
                    all_insights.extend(insight_group)
            insights = all_insights
        
        # Track seen paths for novelty detection
        seen_paths = set()
        
        for insight in insights:
            # Get the path for this insight
            insight_path = insight.get("path", "") if isinstance(insight, dict) else ""
            
            # Simple novelty heuristic: insights with unique paths are novel
            if insight_path not in seen_paths:
                seen_paths.add(insight_path)
                novel_insights.append(insight)
        
        return novel_insights
    
    def detect_novelty(
        self,
        content: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Detect novelty in content and return novelty score.
        
        Args:
            content: Content to analyze (branch, insight, etc.)
        
        Returns:
            Dictionary with novelty score and metadata
        """
        # Generate embedding for the content
        text = ""
        if isinstance(content, dict):
            if "query" in content:
                text = content["query"]
            elif "response" in content:
                text = content["response"]
            elif "insights" in content and isinstance(content["insights"], list):
                # Handle nested list structure
                all_insights = []
                for insight_group in content["insights"]:
                    if isinstance(insight_group, list):
                        all_insights.extend(insight_group)
                text = " ".join(str(i) for i in all_insights[:5])
            else:
                text = str(content)
        else:
            text = str(content)
        
        # Generate embedding
        embedding = self.generate_embedding(text)
        
        # Calculate novelty score
        novelty_score = self.calculate_novelty_score(
            embedding,
            [],  # No existing patterns for this method
        )
        
        # Convert severity to string for JSON serialization
        severity_str = None
        if novelty_score.severity:
            severity_str = novelty_score.severity.value
        
        return {
            "score": float(novelty_score.score),
            "confidence": float(novelty_score.confidence),
            "mode": novelty_score.mode.value,
            "interference_types": novelty_score.interference_types,
            "severity": severity_str,
        }
    
    def detect_interference(
        self,
        pattern_a: np.ndarray,
        pattern_b: np.ndarray,
    ) -> Tuple[float, List[InterferenceType]]:
        """
        Detect interference between two patterns.
        
        Args:
            pattern_a: First pattern embedding
            pattern_b: Second pattern embedding
        
        Returns:
            Tuple of (interference_score, detected_interference_types)
        """
        if not isinstance(pattern_a, np.ndarray) or not isinstance(pattern_b, np.ndarray):
            raise TypeError("Both patterns must be numpy arrays")
        
        if pattern_a.shape != pattern_b.shape:
            raise ValueError(f"Shape mismatch: {pattern_a.shape} vs {pattern_b.shape}")
        
        # Calculate interference across all novelty modes
        interference_scores = {}
        detected_types = []
        
        # Semantic interference (cosine similarity)
        semantic_sim = self._operations.calculate_cosine_similarity(pattern_a, pattern_b)
        semantic_interference = 1.0 - semantic_sim
        
        if semantic_interference > 0.1:
            interference_scores["semantic"] = semantic_interference
            detected_types.append(InterferenceType.SEMANTIC_CONFLICT)
        
        # Structural interference (Jaccard similarity)
        structural_sim = self._operations.calculate_structural_similarity(
            pattern_a, pattern_b
        )
        structural_interference = 1.0 - structural_sim
        
        if structural_interference > 0.1:
            interference_scores["structural"] = structural_interference
            detected_types.append(InterferenceType.STRUCTURAL_CONFLICT)
        
        # Temporal interference
        temporal_sim = self._operations.calculate_temporal_alignment(pattern_a, pattern_b)
        temporal_interference = 1.0 - temporal_sim
        
        if temporal_interference > 0.1:
            interference_scores["temporal"] = temporal_interference
            detected_types.append(InterferenceType.TEMPORAL_CONFLICT)
        
        # Calculate overall interference score
        overall_interference = np.mean(list(interference_scores.values())) if interference_scores else 0.0
        
        return overall_interference, detected_types
    
    def calculate_semantic_distance(
        self,
        v1: np.ndarray,
        v2: np.ndarray,
    ) -> float:
        """
        Calculate semantic distance between two vectors.
        
        Args:
            v1: First vector
            v2: Second vector
        
        Returns:
            float: Semantic distance (higher = more different)
        """
        similarity = self._operations.calculate_cosine_similarity(v1, v2)
        return 1.0 - similarity
    
    def calculate_structural_similarity(
        self,
        topo_a: np.ndarray,
        topo_b: np.ndarray,
    ) -> float:
        """
        Calculate structural similarity between two topological representations.
        
        Args:
            topo_a: First topological representation
            topo_b: Second topological representation
        
        Returns:
            float: Structural similarity score (0-1)
        """
        return self._operations.calculate_structural_similarity(topo_a, topo_b)
    
    def calculate_temporal_alignment(
        self,
        t1: np.ndarray,
        t2: np.ndarray,
    ) -> float:
        """
        Calculate temporal alignment between two temporal representations.
        
        Args:
            t1: First temporal representation
            t2: Second temporal representation
        
        Returns:
            float: Temporal alignment score (0-1)
        """
        return self._operations.calculate_temporal_alignment(t1, t2)
    
    def calculate_novelty_score(
        self,
        new_pattern: np.ndarray,
        existing_patterns: List[np.ndarray],
        mode: Optional[NoveltyMode] = None,
    ) -> NoveltyScore:
        """
        Calculate novelty score for a new pattern against existing patterns.
        
        Args:
            new_pattern: New pattern to evaluate
            existing_patterns: List of existing patterns to compare against
            mode: Novelty mode to use (defaults to all modes)
        
        Returns:
            NoveltyScore with score, confidence, and interference details
        """
        if not isinstance(new_pattern, np.ndarray):
            raise TypeError("new_pattern must be a numpy array")
        
        if not existing_patterns:
            # If no existing patterns, assume completely novel
            return NoveltyScore(
                score=1.0,
                mode=mode or NoveltyMode.SEMANTIC,
                confidence=1.0,
            )
        
        scores_by_mode = {}
        interference_types = set()
        severities = []
        
        # Calculate novelty for each mode
        if mode is None:
            modes = NoveltyMode.all_modes()
        else:
            modes = [mode]
        
        for mode in modes:
            # Calculate interference with all existing patterns
            interference_scores = []
            detected_types = []
            
            for existing in existing_patterns:
                interference, types = self.detect_interference(
                    new_pattern, existing
                )
                interference_scores.append(interference)
                detected_types.extend(types)
            
            avg_interference = np.mean(interference_scores) if interference_scores else 0.0
            
            # Novelty score is inverse of interference
            novelty = 1.0 - avg_interference
            novelty = np.clip(novelty, 0.0, 1.0)
            
            scores_by_mode[mode] = novelty
            
            for t in detected_types:
                interference_types.add(t)
            
            if interference_scores:
                max_severity = self._get_severity_from_interference(interference_scores)
                severities.append(max_severity)
        
        # Calculate overall novelty score (average across modes)
        if scores_by_mode:
            overall_score = np.mean(list(scores_by_mode.values()))
        else:
            overall_score = 0.0
        
        # Determine overall severity
        severity = None
        if severities:
            severity = max(severities, key=lambda s: s.value)
        
        # Calculate confidence based on number of patterns analyzed
        confidence = min(1.0, len(existing_patterns) / 10.0)
        
        return NoveltyScore(
            score=overall_score,
            mode=modes[0] if modes else NoveltyMode.SEMANTIC,
            confidence=confidence,
            interference_types=list(interference_types),
            severity=severity,
        )
    
    def _get_severity_from_interference(
        self,
        interference_scores: List[float],
    ) -> InterferenceSeverity:
        """
        Determine interference severity from scores.
        
        Args:
            interference_scores: List of interference scores
        
        Returns:
            InterferenceSeverity level
        """
        max_score = max(interference_scores)
        
        if max_score >= 0.8:
            return InterferenceSeverity.CRITICAL
        elif max_score >= 0.6:
            return InterferenceSeverity.HIGH
        elif max_score >= 0.4:
            return InterferenceSeverity.MEDIUM
        elif max_score >= 0.2:
            return InterferenceSeverity.LOW
        else:
            return InterferenceSeverity.NONE
    
    def find_similar_patterns(
        self,
        query: np.ndarray,
        patterns: List[Tuple[np.ndarray, str]],
        top_k: int = 5,
        threshold: float = 0.8,
    ) -> List[Tuple[np.ndarray, str, float]]:
        """
        Find patterns similar to a query.
        
        Args:
            query: Query pattern
            patterns: List of (pattern, label) tuples
            top_k: Number of results to return
            threshold: Minimum similarity threshold
        
        Returns:
            List of (pattern, label, similarity) tuples
        """
        if not patterns:
            return []
        
        similarities = []
        
        for pattern, label in patterns:
            if isinstance(query, np.ndarray) and isinstance(pattern, np.ndarray):
                similarity = self._operations.calculate_cosine_similarity(query, pattern)
                
                if similarity >= threshold:
                    similarities.append((pattern, label, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[2], reverse=True)
        
        return similarities[:top_k]
    
    def detect_conceptual_drift(
        self,
        original: np.ndarray,
        current: np.ndarray,
    ) -> Tuple[bool, float]:
        """
        Detect if a concept has drifted from its original form.
        
        Args:
            original: Original pattern
            current: Current pattern
        
        Returns:
            Tuple of (has_drift, drift_score)
        """
        drift = self.detect_interference(original, current)
        interference_score, _ = drift
        
        has_drift = interference_score > 0.3
        return has_drift, interference_score
    
    def get_novelty_threshold(self) -> float:
        """
        Get the current novelty detection threshold.
        
        Returns:
            float: Threshold value (0-1)
        """
        return self.tolerance
    
    def set_novelty_threshold(self, threshold: float) -> None:
        """
        Set the novelty detection threshold.
        
        Args:
            threshold: New threshold value (0-1)
        """
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between 0 and 1")
        
        self.tolerance = threshold
    
    def batch_novelty_detection(
        self,
        new_patterns: List[np.ndarray],
        reference_patterns: List[np.ndarray],
    ) -> List[NoveltyScore]:
        """
        Perform batch novelty detection.
        
        Args:
            new_patterns: List of new patterns to evaluate
            reference_patterns: List of reference patterns
        
        Returns:
            List of NoveltyScore objects
        """
        scores = []
        
        for new_pattern in new_patterns:
            if isinstance(new_pattern, np.ndarray):
                score = self.calculate_novelty_score(
                    new_pattern, reference_patterns
                )
                scores.append(score)
        
        return scores
    
    def get_novelty_threshold(self) -> float:
        """
        Get the current novelty detection threshold.
        
        Returns:
            float: Threshold value (0-1)
        """
        return self.tolerance
    
    def set_novelty_threshold(self, threshold: float) -> None:
        """
        Set the novelty detection threshold.
        
        Args:
            threshold: New threshold value (0-1)
        """
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between 0 and 1")
        
        self.tolerance = threshold
    
    def batch_novelty_detection(
        self,
        new_patterns: List[np.ndarray],
        reference_patterns: List[np.ndarray],
    ) -> List[NoveltyScore]:
        """
        Perform batch novelty detection.
        
        Args:
            new_patterns: List of new patterns to evaluate
            reference_patterns: List of reference patterns
        
        Returns:
            List of NoveltyScore objects
        """
        scores = []
        
        for new_pattern in new_patterns:
            if isinstance(new_pattern, np.ndarray):
                score = self.calculate_novelty_score(
                    new_pattern, reference_patterns
                )
                scores.append(score)
        
        return scores
    
    def __repr__(self) -> str:
        return (
            f"NoveltyTensorEngine("
            f"dimensions={self.dimensions}, "
            f"tolerance={self.tolerance})"
        )
    
    def __str__(self) -> str:
        return self.__repr__()
