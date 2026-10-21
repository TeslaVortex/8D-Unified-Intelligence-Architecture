"""
Novelty Types Module

Type definitions for novelty detection modes and interference types.
"""

from enum import Enum
from typing import Optional


class NoveltyMode(Enum):
    """
    Seven novelty detection modes for comprehensive analysis.
    
    Each mode provides a different perspective on novelty detection:
    - SEMANTIC: Semantic meaning and conceptual understanding
    - STRUCTURAL: Structural and topological similarity
    - TEMPORAL: Temporal alignment and sequence analysis
    - CONTEXTUAL: Contextual and situational factors
    - EVOLUTIONARY: Evolutionary and developmental trajectory
    - CULTURAL: Cultural and societal patterns
    - META: Meta-level abstraction and pattern recognition
    """
    
    SEMANTIC = "semantic"
    STRUCTURAL = "structural"
    TEMPORAL = "temporal"
    CONTEXTUAL = "contextual"
    EVOLUTIONARY = "evolutionary"
    CULTURAL = "cultural"
    META = "meta"
    
    @classmethod
    def all_modes(cls) -> list["NoveltyMode"]:
        """Return all available novelty modes."""
        return list(cls)
    
    @classmethod
    def mode_names(cls) -> list[str]:
        """Return all mode names as strings."""
        return [mode.value for mode in cls]


class InterferenceType(Enum):
    """
    Types of interference detected between patterns.
    
    Interference occurs when two patterns overlap in ways that
    create computational or conceptual conflicts.
    """
    
    SEMANTIC_CONFLICT = "semantic_conflict"
    STRUCTURAL_CONFLICT = "structural_conflict"
    TEMPORAL_CONFLICT = "temporal_conflict"
    CONTEXTUAL_CONFLICT = "contextual_conflict"
    CONCEPTUAL_DRIFT = "conceptual_drift"
    PATTERN_COLLAPSE = "pattern_collapse"
    RESONANCE_AMPLIFICATION = "resonance_amplification"
    
    @classmethod
    def all_types(cls) -> list["InterferenceType"]:
        """Return all interference types."""
        return list(cls)
    
    @classmethod
    def type_names(cls) -> list[str]:
        """Return all type names as strings."""
        return [t.value for t in cls]


class InterferenceSeverity(Enum):
    """
    Severity levels for detected interference.
    """
    
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class NoveltyScore:
    """
    Container for novelty score and metadata.
    
    Attributes:
        score: Novelty score between 0 and 1
        mode: Novelty mode used for detection
        confidence: Confidence in the score
        interference_types: List of detected interference types
        severity: Severity of any interference
    """
    
    def __init__(
        self,
        score: float,
        mode: NoveltyMode,
        confidence: float = 0.95,
        interference_types: Optional[list[InterferenceType]] = None,
        severity: Optional[InterferenceSeverity] = None,
    ):
        self.score = score
        self.mode = mode
        self.confidence = confidence
        self.interference_types = interference_types or []
        self.severity = severity
    
    def __repr__(self) -> str:
        return (
            f"NoveltyScore("
            f"score={self.score:.4f}, "
            f"mode={self.mode.value}, "
            f"confidence={self.confidence:.2f})"
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "score": self.score,
            "mode": self.mode.value,
            "confidence": self.confidence,
            "interference_types": [t.value for t in self.interference_types],
            "severity": self.severity.value if self.severity else None,
        }
