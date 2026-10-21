"""
Evaluation Dimension (λ) Module

Handles evaluation and quality assessment.
"""

import numpy as np
from typing import Optional, Dict, Any, List


class EvaluationDimension:
    """
    Lambda dimension - Evaluation Processing.
    
    Manages quality evaluation, scoring, and assessment criteria.
    
    Attributes:
        evaluation_criteria: Dictionary of evaluation criteria
    """
    
    def __init__(self, evaluation_criteria: Optional[Dict[str, float]] = None):
        """
        Initialize the evaluation dimension.
        
        Args:
            evaluation_criteria: Weights for evaluation criteria
        """
        self.evaluation_criteria = evaluation_criteria or {
            "accuracy": 1.0,
            "efficiency": 1.0,
            "novelty": 1.0,
            "robustness": 1.0,
        }
        self._evaluation_embedding: Optional[np.ndarray] = None
    
    def evaluate(self,
        item: Dict[str, Any],
        criteria: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate an item against criteria.
        
        Args:
            item: Item to evaluate
            criteria: Optional custom criteria
        
        Returns:
            Dictionary with evaluation results
        """
        # Use provided criteria or default
        effective_criteria = criteria or self.evaluation_criteria
        
        # Create evaluation embedding
        embedding = self._create_evaluation_embedding(item, effective_criteria)
        
        # Calculate scores
        scores = self._calculate_scores(item, effective_criteria)
        
        return {
            "embedding": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
            "scores": scores,
            "overall_score": float(np.mean(list(scores.values()))),
        }
    
    def _create_evaluation_embedding(
        self,
        item: Dict[str, Any],
        criteria: Dict[str, float],
    ) -> np.ndarray:
        """
        Create embedding from evaluation data.
        
        Args:
            item: Item data
            criteria: Evaluation criteria
        
        Returns:
            8D evaluation embedding
        """
        embedding = np.zeros(8)
        
        # Criterion weights (dimensions 0-3)
        criterion_names = list(criteria.keys())[:4]
        for i, name in enumerate(criterion_names):
            embedding[i] = criteria[name]
        
        # Item scores (dimensions 4-7)
        item_scores = []
        for name in criterion_names:
            score = item.get(name, 0.5)
            item_scores.append(score)
        
        embedding[4:8] = np.array(item_scores)
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def _calculate_scores(
        self,
        item: Dict[str, Any],
        criteria: Dict[str, float],
    ) -> Dict[str, float]:
        """
        Calculate evaluation scores.
        
        Args:
            item: Item data
            criteria: Evaluation criteria
        
        Returns:
            Dictionary of scores
        """
        scores = {}
        
        for name, weight in criteria.items():
            score = item.get(name, 0.5)
            scores[name] = float(score)
        
        return scores
    
    def compare_items(
        self,
        item_a: Dict[str, Any],
        item_b: Dict[str, Any],
    ) -> Dict[str, float]:
        """
        Compare two items.
        
        Args:
            item_a: First item
            item_b: Second item
        
        Returns:
            Dictionary with comparison scores
        """
        # Evaluate both items
        eval_a = self.evaluate(item_a)
        eval_b = self.evaluate(item_b)
        
        # Calculate differences
        differences = {}
        for criterion in self.evaluation_criteria:
            score_a = eval_a["scores"].get(criterion, 0)
            score_b = eval_b["scores"].get(criterion, 0)
            differences[f"{criterion}_diff"] = float(abs(score_a - score_b))
        
        return differences
    

    
    def get_embedding(self) -> Optional[np.ndarray]:
        """
        Get current evaluation embedding.
        
        Returns:
            Evaluation embedding or None
        """
        return self._evaluation_embedding
    
    def set_embedding(self, embedding: np.ndarray) -> None:
        """
        Set evaluation embedding.
        
        Args:
            embedding: New embedding
        """
        self._evaluation_embedding = embedding
    
    def normalize(self) -> None:
        """Normalize current evaluation embedding."""
        if self._evaluation_embedding is not None:
            norm = np.linalg.norm(self._evaluation_embedding)
            if norm > 0:
                self._evaluation_embedding = self._evaluation_embedding / norm
    
    def __repr__(self) -> str:
        return f"EvaluationDimension(criteria={len(self.evaluation_criteria)})"
    
    def __str__(self) -> str:
        return self.__repr__()
