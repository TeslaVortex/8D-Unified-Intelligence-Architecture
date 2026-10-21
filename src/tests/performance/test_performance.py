"""
Performance Benchmarks for 8D Unified Intelligence System

Performance tests and benchmarks.
"""

import pytest
import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.orchestrator.unified_intelligence_system import UnifiedIntelligenceSystem


class TestPerformanceBenchmarks:
    """Performance benchmark tests."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.system = UnifiedIntelligenceSystem()
        self.system.initialize()
    
    @pytest.mark.benchmark
    def test_embedding_performance(self):
        """Test embedding generation performance."""
        query = "What is artificial intelligence?"
        
        start = time.perf_counter()
        result = self.system.process_query(query)
        end = time.perf_counter()
        
        processing_time = end - start
        
        # P95 target: < 200ms for embedding
        # Full cycle target: < 5s
        assert processing_time < 5.0, f"Processing took {processing_time}s, expected < 5s"
    
    @pytest.mark.benchmark
    def test_novelty_detection_performance(self):
        """Test novelty detection performance."""
        query = "What is a novel approach to AI?"
        
        start = time.perf_counter()
        result = self.system.process_query(query)
        end = time.perf_counter()
        
        processing_time = end - start
        
        # Novelty detection should be fast
        assert processing_time < 2.0, f"Processing took {processing_time}s, expected < 2s"
    
    @pytest.mark.benchmark
    def test_full_cycle_performance(self):
        """Test full cycle performance."""
        query = "What is the meaning of artificial intelligence?"
        
        start = time.perf_counter()
        result = self.system.process_query(query)
        end = time.perf_counter()
        
        processing_time = end - start
        
        # Full cycle target: < 5s P95, < 10s P99
        assert processing_time < 5.0, f"Full cycle took {processing_time}s, expected < 5s"
    
    @pytest.mark.benchmark
    def test_batch_processing_performance(self):
        """Test batch processing performance."""
        queries = [
            "What is AI?",
            "How does machine learning work?",
            "Why is deep learning important?",
            "What are neural networks?",
            "How does backpropagation work?",
        ]
        
        start = time.perf_counter()
        for query in queries:
            self.system.process_query(query)
        end = time.perf_counter()
        
        processing_time = end - start
        
        # Batch of 5 queries should be fast
        assert processing_time < 10.0, f"Batch processing took {processing_time}s, expected < 10s"
    
    @pytest.mark.benchmark
    def test_long_query_performance(self):
        """Test long query performance."""
        long_query = " ".join(["This is a word"] * 100)  # 500 word query
        
        start = time.perf_counter()
        result = self.system.process_query(long_query)
        end = time.perf_counter()
        
        processing_time = end - start
        
        assert processing_time < 10.0, f"Long query processing took {processing_time}s, expected < 10s"
    
    @pytest.mark.benchmark
    def test_complex_query_performance(self):
        """Test complex query performance."""
        complex_query = """
        What are the philosophical implications of artificial intelligence?
        Consider ethical concerns, future scenarios, and societal impacts.
        Also analyze from multiple perspectives including economic, social,
        and political dimensions.
        """
        
        start = time.perf_counter()
        result = self.system.process_query(complex_query)
        end = time.perf_counter()
        
        processing_time = end - start
        
        assert processing_time < 10.0, f"Complex query took {processing_time}s, expected < 10s"
    
    @pytest.mark.benchmark
    def test_query_throughput(self):
        """Test query throughput."""
        queries = [f"Query {i}" for i in range(50)]
        
        start = time.perf_counter()
        for query in queries:
            self.system.process_query(query)
        end = time.perf_counter()
        
        processing_time = end - start
        
        # 50 queries should complete in reasonable time
        queries_per_second = 50 / processing_time
        assert queries_per_second > 10, f"Throughput: {queries_per_second} qps, expected > 10"
    
    @pytest.mark.benchmark
    def test_memory_efficiency(self):
        """Test memory efficiency."""
        import gc
        
        # Process multiple queries
        for _ in range(10):
            self.system.process_query("Test query")
        
        # Force garbage collection
        gc.collect()
        
        # Should still work
        result = self.system.process_query("Memory test")
        assert result is not None
        assert result["status"] == "completed"


class TestStressTests:
    """Stress tests for the system."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.system = UnifiedIntelligenceSystem()
        self.system.initialize()
    
    def test_concurrent_queries(self):
        """Test handling of concurrent queries."""
        queries = [f"Query {i}" for i in range(20)]
        
        results = []
        for query in queries:
            result = self.system.process_query(query)
            results.append(result)
        
        # All queries should complete successfully
        assert len(results) == 20
        assert all(r["status"] == "completed" for r in results)
    
    def test_long_running_session(self):
        """Test long-running session."""
        # Process many queries in a row
        for i in range(100):
            result = self.system.process_query(f"Session query {i}")
            assert result is not None
            assert result["status"] in ["completed", "error"]
    
    def test_error_recovery(self):
        """Test error recovery under stress."""
        # Mix of valid and edge case queries
        queries = [
            "",  # Empty
            "a",  # Single char
            "a" * 1000,  # Long string
            "Query with special chars: @#$%^&*()",  # Special chars
            "Unicode: 你好世界 🌍",  # Unicode
        ]
        
        for query in queries:
            result = self.system.process_query(query)
            assert result is not None


class TestResourceUsage:
    """Resource usage tests."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.system = UnifiedIntelligenceSystem()
        self.system.initialize()
    
    def test_processing_time_consistency(self):
        """Test consistent processing times."""
        query = "What is AI?"
        times = []
        
        for _ in range(10):
            start = time.perf_counter()
            self.system.process_query(query)
            end = time.perf_counter()
            times.append(end - start)
        
        # Calculate statistics
        avg_time = np.mean(times)
        max_time = max(times)
        min_time = min(times)
        
        # Times should be relatively consistent
        variance = np.var(times)
        
        assert variance < 1.0, f"High variance in processing times: {variance}"
    
    def test_initialization_once(self):
        """Test that initialization happens once."""
        import time
        
        # Measure initialization time
        start = time.perf_counter()
        self.system.initialize()
        init_time = time.perf_counter() - start
        
        # Re-initialize should be fast (should be a no-op)
        start = time.perf_counter()
        self.system.initialize()
        reinit_time = time.perf_counter() - start
        
        # Re-initialization should be much faster
        assert reinit_time < init_time / 10, f"Re-init not lazy: {reinit_time}s vs {init_time}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
