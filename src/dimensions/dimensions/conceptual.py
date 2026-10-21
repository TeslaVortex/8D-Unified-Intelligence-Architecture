"""
Conceptual Abstraction Dimension (γ) Module

Handles conceptual abstraction and pattern recognition.
"""

import numpy as np
from typing import Optional, Dict, Any, List, Set
from collections import Counter


class ConceptualDimension:
    """
    Gamma dimension - Conceptual Abstraction Processing.
    
    Manages conceptual abstraction, pattern recognition,
    and hierarchical understanding.
    
    Attributes:
        abstraction_level: Current level of abstraction
    """
    
    def __init__(self, abstraction_level: int = 3):
        """
        Initialize the conceptual dimension.
        
        Args:
            abstraction_level: Current abstraction level (1-10)
        """
        self.abstraction_level = abstraction_level
        self._concept_embedding: Optional[np.ndarray] = None
        self._active_concepts: Set[str] = set()
        self._concept_hierarchy: Dict[str, List[str]] = {}
    
    def process_concepts(
        self,
        inputs: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Process input concepts and extract abstractions.
        
        Args:
            inputs: Input concepts or text
            context: Additional context
        
        Returns:
            Dictionary with processed concepts
        """
        # Extract concepts from inputs
        extracted_concepts = self._extract_concepts(inputs)
        
        # Update active concepts
        self._active_concepts.update(extracted_concepts)
        
        # Create concept embedding
        embedding = self._create_concept_embedding(extracted_concepts)
        
        # Calculate abstraction metrics
        metrics = self._calculate_abstraction_metrics(extracted_concepts)
        
        # Update hierarchy if needed
        self._update_hierarchy(extracted_concepts)
        
        return {
            "embedding": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
            "concepts": extracted_concepts,
            "abstraction_level": self.abstraction_level,
            "metrics": metrics,
        }
    
    def _extract_concepts(
        self,
        inputs: List[str],
    ) -> List[str]:
        """
        Extract concepts from input strings.
        
        Args:
            inputs: List of input strings
        
        Returns:
            List of extracted concepts
        """
        concepts = []
        
        for text in inputs:
            # Simple concept extraction (placeholder)
            # In production, use NLP libraries
            words = text.lower().split()
            for word in words:
                if len(word) > 3:  # Minimum word length
                    # Check if already extracted
                    if word not in concepts:
                        concepts.append(word)
        
        return concepts
    
    def _create_concept_embedding(
        self,
        concepts: List[str],
    ) -> np.ndarray:
        """
        Create embedding from concepts.
        
        Args:
            concepts: List of concepts
        
        Returns:
            8D concept embedding
        """
        # Create concept vector
        concept_vector = np.zeros(8)
        
        # Use concept frequency and diversity
        if concepts:
            # Concept diversity
            diversity = len(concepts) / max(len(concepts) * 2, 1)
            concept_vector[0] = diversity
            
            # Concept frequency distribution
            concept_counts = Counter(concepts)
            total = sum(concept_counts.values())
            
            # Top concept frequency
            if concept_counts:
                top_count = max(concept_counts.values())
                concept_vector[1] = top_count / max(total, 1)
            
            # Concept age (placeholder)
            concept_vector[2] = 0.5
            
            # Remaining dimensions
            for i in range(3, 8):
                concept_vector[i] = np.random.random()
        
        # Normalize
        norm = np.linalg.norm(concept_vector)
        if norm > 0:
            concept_vector = concept_vector / norm
        
        return concept_vector
    
    def _calculate_abstraction_metrics(
        self,
        concepts: List[str],
    ) -> Dict[str, float]:
        """
        Calculate abstraction metrics.
        
        Args:
            concepts: Extracted concepts
        
        Returns:
            Dictionary of metrics
        """
        metrics = {}
        
        # Concept count
        metrics["concept_count"] = float(len(concepts))
        
        # Concept diversity
        if concepts:
            unique_concepts = len(set(concepts))
            metrics["diversity"] = float(unique_concepts / len(concepts))
        
        # Abstraction ratio
        metrics["abstraction_ratio"] = float(self.abstraction_level / 10.0)
        
        # Concept density
        metrics["density"] = float(len(concepts) / 100.0)
        
        return metrics
    
    def _update_hierarchy(
        self,
        new_concepts: List[str],
    ) -> None:
        """
        Update concept hierarchy with new concepts.
        
        Args:
            new_concepts: New concepts to add
        """
        for concept in new_concepts:
            if concept not in self._concept_hierarchy:
                self._concept_hierarchy[concept] = []
    
    def get_abstraction_level(self) -> int:
        """
        Get current abstraction level.
        
        Returns:
            Abstraction level
        """
        return self.abstraction_level
    
    def set_abstraction_level(self, level: int) -> None:
        """
        Set abstraction level.
        
        Args:
            level: New abstraction level (1-10)
        """
        self.abstraction_level = max(1, min(10, level))
    
    def get_embedding(self) -> Optional[np.ndarray]:
        """
        Get current concept embedding.
        
        Returns:
            Concept embedding or None
        """
        return self._concept_embedding
    
    def set_embedding(self, embedding: np.ndarray) -> None:
        """
        Set concept embedding.
        
        Args:
            embedding: New embedding
        """
        self._concept_embedding = embedding
    
    def normalize(self) -> None:
        """Normalize current concept embedding."""
        if self._concept_embedding is not None:
            norm = np.linalg.norm(self._concept_embedding)
            if norm > 0:
                self._concept_embedding = self._concept_embedding / norm
    
    def get_active_concepts(self) -> Set[str]:
        """
        Get active concepts.
        
        Returns:
            Set of active concept strings
        """
        return self._active_concepts.copy()
    
    def clear_concepts(self) -> None:
        """Clear all active concepts."""
        self._active_concepts.clear()
    
    def __repr__(self) -> str:
        return f"ConceptualDimension(abstraction_level={self.abstraction_level})"
    
    def __str__(self) -> str:
        return self.__repr__()
