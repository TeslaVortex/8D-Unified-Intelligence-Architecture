"""
Pattern Data Structure Module

Data structures for pattern storage and management.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import json


@dataclass
class Pattern:
    """
    Data structure representing a pattern in the 8D space.
    
    Attributes:
        pattern_id: Unique identifier for the pattern
        embedding: 8D embedding vector
        metadata: Additional metadata about the pattern
        activation_count: Number of times this pattern has been activated
        last_accessed: Timestamp of last access
        tags: List of tags for pattern retrieval
        dimensions: Dictionary of dimension-specific data
    """
    
    pattern_id: str
    embedding: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    activation_count: int = 0
    last_accessed: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    dimensions: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.last_accessed is None:
            self.last_accessed = datetime.now()
    
    @classmethod
    def create(
        cls,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        dimensions: Optional[Dict[str, Any]] = None,
        activation_count: int = 0,
        last_accessed: Optional[datetime] = None,
    ) -> "Pattern":
        """
        Create a new pattern.
        
        Args:
            embedding: 8D embedding vector
            metadata: Pattern metadata
            tags: Pattern tags
            dimensions: Dimension-specific data
            activation_count: Initial activation count
            last_accessed: Initial last accessed timestamp
        
        Returns:
            Pattern instance
        """
        return cls(
            pattern_id=str(uuid.uuid4()),
            embedding=embedding,
            metadata=metadata or {},
            tags=tags or [],
            dimensions=dimensions or {},
            activation_count=activation_count,
            last_accessed=last_accessed,
        )
    
    def activate(self) -> None:
        """Increment activation count and update timestamp."""
        self.activation_count += 1
        self.last_accessed = datetime.now()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the pattern."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> bool:
        """
        Remove a tag from the pattern.
        
        Returns:
            bool: True if tag was removed, False if not found
        """
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update a metadata field."""
        self.metadata[key] = value
    
    def get_dimension_value(self, dimension: str) -> Optional[Any]:
        """
        Get a dimension-specific value.
        
        Args:
            dimension: Dimension identifier
        
        Returns:
            Dimension value or None if not found
        """
        return self.dimensions.get(dimension)
    
    def set_dimension_value(self, dimension: str, value: Any) -> None:
        """
        Set a dimension-specific value.
        
        Args:
            dimension: Dimension identifier
            value: Value to set
        """
        self.dimensions[dimension] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert pattern to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "pattern_id": self.pattern_id,
            "embedding": self.embedding,
            "metadata": self.metadata,
            "activation_count": self.activation_count,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "tags": self.tags,
            "dimensions": self.dimensions,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pattern":
        """
        Create pattern from dictionary.
        
        Args:
            data: Dictionary representation
        
        Returns:
            Pattern instance
        """
        last_accessed = None
        if data.get("last_accessed"):
            last_accessed = datetime.fromisoformat(data["last_accessed"])
        
        return cls(
            pattern_id=data["pattern_id"],
            embedding=data["embedding"],
            metadata=data.get("metadata", {}),
            activation_count=data.get("activation_count", 0),
            last_accessed=last_accessed,
            tags=data.get("tags", []),
            dimensions=data.get("dimensions", {}),
        )
    
    def __repr__(self) -> str:
        return (
            f"Pattern("
            f"id={self.pattern_id[:8]}..., "
            f"activations={self.activation_count}, "
            f"tags={self.tags})"
        )
    
    def __str__(self) -> str:
        return self.__repr__()


class PatternIDGenerator:
    """
    Generator for pattern IDs following the 8D format.
    
    Format: P_αβγδζηλθ
    Where each Greek letter represents a dimension value.
    """
    
    def __init__(self):
        """Initialize the ID generator."""
        self._counter = 0
    
    def generate(self, dimension_values: Optional[List[int]] = None) -> str:
        """
        Generate a pattern ID.
        
        Args:
            dimension_values: Optional dimension values (0-9)
        
        Returns:
            Pattern ID string
        """
        # Generate base ID
        base_id = f"P_{self._counter:04d}"
        self._counter += 1
        
        # If dimension values provided, append them
        if dimension_values and len(dimension_values) == 8:
            # Convert values to Greek letters (0-9 mapping)
            greek_mapping = {
                0: 'α', 1: 'β', 2: 'γ', 3: 'δ',
                4: 'ε', 5: 'ζ', 6: 'η', 7: 'θ',
                8: 'ι', 9: 'λ'
            }
            suffix = ''.join(greek_mapping.get(v, str(v)) for v in dimension_values)
            return f"{base_id}_{suffix}"
        
        return base_id
    
    def generate_from_pattern(self, pattern: Pattern) -> str:
        """
        Generate an ID from a pattern's dimension values.
        
        Args:
            pattern: Pattern to generate ID from
        
        Returns:
            Pattern ID string
        """
        dimension_values = []
        
        for dim_name in ['alpha', 'beta', 'gamma', 'delta', 
                        'zeta', 'eta', 'lambda', 'theta']:
            if dim_name in pattern.dimensions:
                value = pattern.dimensions[dim_name]
                if isinstance(value, (int, float)):
                    dimension_values.append(int(value))
                elif isinstance(value, str):
                    try:
                        dimension_values.append(int(value))
                    except ValueError:
                        dimension_values.append(0)
                else:
                    dimension_values.append(0)
            else:
                dimension_values.append(0)
        
        return self.generate(dimension_values)
