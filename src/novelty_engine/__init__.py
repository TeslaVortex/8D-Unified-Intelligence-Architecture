"""
Novelty Engine Module

Core novelty detection functionality for the 8D intelligence system.
"""

from .novelty_tensor_engine import NoveltyTensorEngine
from .novelty_types import NoveltyMode, InterferenceType
from .tensor_operations import TensorOperations

__all__ = [
    "NoveltyTensorEngine",
    "NoveltyMode",
    "InterferenceType",
    "TensorOperations",
]
