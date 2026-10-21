"""
Integration Tests for 8D Unified Intelligence System

Tests for component integration and end-to-end flows.
"""

import pytest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.orchestrator.unified_intelligence_system import UnifiedIntelligenceSystem


class TestSystemIntegration:
    """Integration tests for the complete system."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.system = UnifiedIntelligenceSystem()
        self.system.initialize()
    
    def test_full_cycle_processing(self):
        """Test complete query processing cycle."""
        query = "What is the meaning of artificial intelligence?"
        result = self.system.process_query(query)
        
        assert result is not None
        assert result["status"] == "completed"
        assert "trace_id" in result
        assert "response" in result
        assert "processing_time" in result
    
    def test_multiple_queries(self):
        """Test processing multiple queries."""
        queries = [
            "What is AI?",
            "How does machine learning work?",
            "Why is deep learning important?",
        ]
        
        for query in queries:
            result = self.system.process_query(query)
            assert result is not None
            assert result["status"] == "completed"
    
    def test_health_check_integration(self):
        """Test health check with all components."""
        result = self.system.health_check()
        
        assert result["status"] == "healthy"
        components = result["components"]
        
        # Verify all components are active
        assert components["novelty_engine"] == "active"
        assert components["pattern_space"] == "active"
        assert components["dimensional_core"] == "active"
        assert components["perspective_shift"] == "active"
        assert components["self_monitor"] == "active"
        assert components["logic_toolkit"] == "active"
    
    def test_trace_id_consistency(self):
        """Test that trace IDs are consistent."""
        result1 = self.system.process_query("Test query 1")
        result2 = self.system.process_query("Test query 2")
        
        # Each query should have its own trace ID
        assert result1["trace_id"] != result2["trace_id"]
    
    def test_embedding_integration(self):
        """Test embedding integration in processing."""
        query = "Test query with some words"
        result = self.system.process_query(query)
        
        # Should have generated embeddings
        assert result is not None
        assert "trace_id" in result
    
    def test_novelty_detection_integration(self):
        """Test novelty detection integration."""
        query = "What is a novel approach to AI?"
        result = self.system.process_query(query)
        
        assert result is not None
        assert "novelty_score" in result
        assert "novelty_detected" in result
    
    def test_meta_compass_integration(self):
        """Test meta-compass integration."""
        query = "Analyze this from multiple perspectives"
        result = self.system.process_query(query)
        
        assert result is not None
        assert "meta_compass_score" in result
    
    def test_dimensional_processing_integration(self):
        """Test dimensional processing integration."""
        query = "Process through all dimensions"
        result = self.system.process_query(query)
        
        assert result is not None
        assert "processing_time" in result
    
    def test_response_generation(self):
        """Test response generation."""
        query = "What is the capital of France?"
        result = self.system.process_query(query)
        
        assert result is not None
        assert "response" in result
        assert len(result["response"]) > 0
    
    def test_performance_baseline(self):
        """Test baseline performance."""
        import time
        
        query = "What is artificial intelligence and how does it work?"
        iterations = 10
        
        start = time.time()
        for _ in range(iterations):
            self.system.process_query(query)
        end = time.time()
        
        avg_time = (end - start) / iterations
        
        # Should complete within reasonable time
        assert avg_time < 2.0, f"Average processing time {avg_time}s exceeds 2s"
    
    def test_context_handling(self):
        """Test context handling in queries."""
        query = "What is Python?"
        context = {
            "user_id": "test_user",
            "session_id": "test_session",
            "language": "en",
        }
        
        result = self.system.process_query(query, context)
        
        assert result is not None
        assert result["status"] == "completed"
    
    def test_complex_query_processing(self):
        """Test processing of complex queries."""
        query = """
        What are the philosophical implications of artificial intelligence?
        Consider ethical concerns, future scenarios, and societal impacts.
        Also analyze from multiple perspectives including economic, social,
        and political dimensions.
        """
        result = self.system.process_query(query)
        
        assert result is not None
        assert result["status"] == "completed"
        assert result["insights_count"] >= 0
    
    def test_error_recovery(self):
        """Test error recovery mechanisms."""
        # Process many queries to potentially stress the system
        queries = ["Query " + str(i) for i in range(100)]
        
        for query in queries:
            result = self.system.process_query(query)
            assert result is not None
            assert "status" in result
    
    def test_system_shutdown(self):
        """Test system shutdown."""
        self.system.shutdown()
        assert self.system._initialized is False


class TestComponentInteractions:
    """Tests for component interactions."""
    
    def test_novelty_pattern_interaction(self):
        """Test novelty and pattern space interaction."""
        system = UnifiedIntelligenceSystem()
        system.initialize()
        
        query = "Test pattern"
        result = system.process_query(query)
        
        assert result is not None
        assert result["status"] == "completed"
    
    def test_dimension_logic_interaction(self):
        """Test dimensional core and logic layers interaction."""
        system = UnifiedIntelligenceSystem()
        system.initialize()
        
        query = "Analyze this"
        result = system.process_query(query)
        
        assert result is not None
    
    def test_meta_compass_oversight(self):
        """Test meta-compass oversight functionality."""
        system = UnifiedIntelligenceSystem()
        system.initialize()
        
        query = "Self-reflect on this query"
        result = system.process_query(query)
        
        assert result is not None
        assert "meta_compass_score" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
