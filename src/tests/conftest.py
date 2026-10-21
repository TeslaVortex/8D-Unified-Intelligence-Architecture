"""
Pytest configuration and fixtures for 8D Unified Intelligence Architecture.
"""

import pytest
import sys
import os

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, src_path)


@pytest.fixture
def sample_embedding():
    """Sample 8D embedding vector."""
    return [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]


@pytest.fixture
def sample_pattern(sample_embedding):
    """Sample pattern with embedding."""
    class Pattern:
        def __init__(self, embedding):
            self.embedding = embedding
            self.pattern_id = "P_test_001"
            self.metadata = {}
            self.activation_count = 0
            self.last_accessed = None
            self.tags = []
            self.dimensions = {}
        
        def activate(self):
            self.activation_count += 1
    
    return Pattern(sample_embedding)


@pytest.fixture
def pattern_a(sample_embedding):
    """Pattern A for interference detection."""
    return sample_pattern


@pytest.fixture
def pattern_b(sample_embedding):
    """Pattern B for interference detection."""
    class Pattern:
        def __init__(self):
            self.embedding = [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]
            self.pattern_id = "P_test_002"
            self.metadata = {}
            self.activation_count = 0
            self.last_accessed = None
            self.tags = []
            self.dimensions = {}
        
        def activate(self):
            self.activation_count += 1
    
    return Pattern()
