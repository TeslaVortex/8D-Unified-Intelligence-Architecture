"""
Temporal Context Dimension (δ) Module

Processes temporal context and sequence analysis.
"""

import numpy as np
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
from scipy.signal import find_peaks


class TemporalDimension:
    """
    Delta dimension - Temporal Context Processing.
    
    Handles temporal analysis, sequence patterns,
    and time-based contextual understanding.
    
    Attributes:
        time_window: Analysis time window in seconds
    """
    
    def __init__(self, time_window: int = 3600):
        """
        Initialize the temporal dimension.
        
        Args:
            time_window: Analysis window in seconds (default: 1 hour)
        """
        self.time_window = time_window
        self._temporal_embedding: Optional[np.ndarray] = None
        self._event_sequence: List[Tuple[datetime, str]] = []
        self._temporal_patterns: List[Dict[str, Any]] = []
    
    def analyze_sequence(
        self,
        events: List[Tuple[datetime, str]],
    ) -> Dict[str, Any]:
        """
        Analyze a sequence of events.
        
        Args:
            events: List of (timestamp, event) tuples
        
        Returns:
            Dictionary with temporal analysis
        """
        if not events:
            return {
                "embedding": np.zeros(8).tolist(),
                "metrics": {},
            }
        
        # Sort events by time
        sorted_events = sorted(events, key=lambda x: x[0])
        
        # Create temporal embedding
        embedding = self._create_temporal_embedding(sorted_events)
        
        # Calculate temporal metrics
        metrics = self._calculate_temporal_metrics(sorted_events)
        
        # Detect temporal patterns
        patterns = self._detect_temporal_patterns(sorted_events)
        
        return {
            "embedding": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
            "metrics": metrics,
            "patterns": patterns,
        }
    
    def _create_temporal_embedding(
        self,
        events: List[Tuple[datetime, str]],
    ) -> np.ndarray:
        """
        Create temporal embedding from event sequence.
        
        Args:
            events: Sorted event list
        
        Returns:
            8D temporal embedding
        """
        if not events:
            return np.zeros(8)
        
        embedding = np.zeros(8)
        
        # Event density (dimension 0)
        time_span = (events[-1][0] - events[0][0]).total_seconds()
        if time_span > 0:
            density = len(events) / time_span
            embedding[0] = min(1.0, density * 100)
        
        # Sequence regularity (dimension 1)
        intervals = []
        for i in range(1, len(events)):
            interval = (events[i][0] - events[i-1][0]).total_seconds()
            intervals.append(interval)
        
        if intervals:
            mean_interval = np.mean(intervals)
            std_interval = np.std(intervals)
            regularity = 1.0 - (std_interval / (mean_interval + 1))
            embedding[1] = max(0.0, min(1.0, regularity))
        
        # Recency bias (dimension 2)
        if events:
            recent_weight = len(events) / max(len(events), 1)
            embedding[2] = recent_weight
        
        # Temporal distribution (dimensions 3-7)
        if events and time_span > 0:
            normalized_times = []
            for event in events:
                delta = (event[0] - events[0][0]).total_seconds()
                normalized_times.append(delta / time_span)
            
            # Create histogram bins
            bins = np.linspace(0, 1, 5)
            hist, _ = np.histogram(normalized_times, bins=bins)
            
            # Normalize histogram
            if hist.max() > 0:
                hist = hist / hist.max()
            
            # Take first 4 values for dimensions 3-7
            embedding[3:7] = hist[:4]
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def _calculate_temporal_metrics(
        self,
        events: List[Tuple[datetime, str]],
    ) -> Dict[str, float]:
        """
        Calculate temporal metrics.
        
        Args:
            events: Event sequence
        
        Returns:
            Dictionary of metrics
        """
        if not events:
            return {}
        
        metrics = {}
        
        # Event count
        metrics["event_count"] = float(len(events))
        
        # Time span
        time_span = (events[-1][0] - events[0][0]).total_seconds()
        metrics["time_span_seconds"] = float(time_span)
        
        # Event rate
        if time_span > 0:
            metrics["event_rate"] = float(len(events) / time_span)
        
        # Average interval
        intervals = []
        for i in range(1, len(events)):
            interval = (events[i][0] - events[i-1][0]).total_seconds()
            intervals.append(interval)
        
        if intervals:
            metrics["avg_interval"] = float(np.mean(intervals))
            metrics["std_interval"] = float(np.std(intervals))
        
        # Event duration (placeholder)
        metrics["analysis_duration"] = float(time_span)
        
        return metrics
    
    def _detect_temporal_patterns(
        self,
        events: List[Tuple[datetime, str]],
    ) -> List[Dict[str, Any]]:
        """
        Detect temporal patterns in event sequence.
        
        Args:
            events: Event sequence
        
        Returns:
            List of detected patterns
        """
        patterns = []
        
        if len(events) < 2:
            return patterns
        
        # Calculate intervals
        intervals = []
        for i in range(1, len(events)):
            interval = (events[i][0] - events[i-1][0]).total_seconds()
            intervals.append(interval)
        
        if not intervals:
            return patterns
        
        # Detect peaks in intervals (burst patterns)
        peaks, _ = find_peaks(intervals, height=np.mean(intervals) * 0.5)
        
        if len(peaks) > 0:
            patterns.append({
                "type": "burst",
                "count": len(peaks),
                "peak_intervals": [intervals[i] for i in peaks],
            })
        
        # Detect periodicity (placeholder)
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        
        if std_interval < mean_interval * 0.5:
            patterns.append({
                "type": "periodic",
                "period": float(mean_interval),
                "regularity": float(1.0 - std_interval / mean_interval),
            })
        
        return patterns
    
    def update_sequence(
        self,
        event: Tuple[datetime, str],
    ) -> None:
        """
        Update the event sequence with a new event.
        
        Args:
            event: (timestamp, event) tuple
        """
        self._event_sequence.append(event)
    
    def get_temporal_embedding(self) -> Optional[np.ndarray]:
        """
        Get current temporal embedding.
        
        Returns:
            Temporal embedding or None
        """
        return self._temporal_embedding
    
    def set_embedding(self, embedding: np.ndarray) -> None:
        """
        Set temporal embedding.
        
        Args:
            embedding: New embedding
        """
        self._temporal_embedding = embedding
    
    def normalize(self) -> None:
        """Normalize current temporal embedding."""
        if self._temporal_embedding is not None:
            norm = np.linalg.norm(self._temporal_embedding)
            if norm > 0:
                self._temporal_embedding = self._temporal_embedding / norm
    
    def get_sequence(self) -> List[Tuple[datetime, str]]:
        """
        Get current event sequence.
        
        Returns:
            List of events
        """
        return self._event_sequence.copy()
    
    def clear_sequence(self) -> None:
        """Clear the event sequence."""
        self._event_sequence.clear()
    
    def __repr__(self) -> str:
        return f"TemporalDimension(time_window={self.time_window}s)"
    
    def __str__(self) -> str:
        return self.__repr__()
