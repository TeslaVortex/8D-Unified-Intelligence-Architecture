"""
Helper Utilities Module

Provides utility functions for the 8D intelligence system.
"""

import numpy as np
from typing import Optional, List, Dict, Any, Tuple
import time
import json
import logging
from datetime import datetime


# Set up logging
logger = logging.getLogger(__name__)


def generate_id(prefix: str = "id") -> str:
    """
    Generate a unique identifier.
    
    Args:
        prefix: ID prefix
        
    Returns:
        Unique identifier string
    """
    timestamp = int(time.time() * 1000000)
    random_part = np.random.randint(0, 2**24)
    return f"{prefix}_{timestamp}_{random_part}"


def timestamp_now() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        ISO format timestamp string
    """
    return datetime.utcnow().isoformat() + "Z"


def parse_timestamp(ts: str) -> datetime:
    """
    Parse ISO format timestamp.
    
    Args:
        ts: ISO format timestamp string
        
    Returns:
        datetime object
    """
    # Handle both with and without 'Z' suffix
    if ts.endswith('Z'):
        ts = ts[:-1] + '+00:00'
    return datetime.fromisoformat(ts)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division fails
        
    Returns:
        Result of division or default value
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ZeroDivisionError):
        return default


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value to a range.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def interpolate(
    start: float,
    end: float,
    alpha: float,
    clamp_result: bool = True
) -> float:
    """
    Linear interpolation between two values.
    
    Args:
        start: Starting value
        end: Ending value
        alpha: Interpolation factor (0 to 1)
        clamp_result: Whether to clamp result
        
    Returns:
        Interpolated value
    """
    result = start + alpha * (end - start)
    if clamp_result:
        result = clamp(result, start, end)
    return result


def weighted_average(values: List[float], weights: List[float]) -> float:
    """
    Calculate weighted average.
    
    Args:
        values: List of values
        weights: List of weights
        
    Returns:
        Weighted average
    """
    if not values or not weights:
        return 0.0
    
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.0
    return sum(v * w for v, w in zip(values, weights)) / total_weight


def normalize_list(values: List[float], min_val: Optional[float] = None, 
                  max_val: Optional[float] = None) -> List[float]:
    """
    Normalize a list of values to [0, 1] range.
    
    Args:
        values: List of values
        min_val: Minimum value (auto-calculated if None)
        max_val: Maximum value (auto-calculated if None)
        
    Returns:
        Normalized values
    """
    if not values:
        return []
    
    if min_val is None or max_val is None:
        min_val = min(values)
        max_val = max(values)
    
    range_val = max_val - min_val
    if range_val == 0:
        return [0.0] * len(values)
    
    normalized = [(v - min_val) / range_val for v in values]
    return normalized


def batch_process(items: List[Any], processor) -> List[Any]:
    """
    Process a batch of items.
    
    Args:
        items: List of items to process
        processor: Function to apply to each item
        
    Returns:
        List of processed items
    """
    return [processor(item) for item in items]


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries.
    
    Args:
        dicts: Multiple dictionaries to merge
        
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def deep_copy(obj: Any) -> Any:
    """
    Deep copy an object.
    
    Args:
        obj: Object to copy
        
    Returns:
        Deep copy of object
    """
    return json.loads(json.dumps(obj))


def ensure_list(obj: Any) -> List:
    """
    Ensure an object is a list.
    
    Args:
        obj: Object to convert
        
    Returns:
        List containing object or object as list
    """
    if isinstance(obj, list):
        return obj
    return [obj]


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 1:
        return f"{seconds * 1000:.1f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"


def truncate_string(s: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate a string to maximum length.
    
    Args:
        s: Input string
        max_length: Maximum length
        suffix: Suffix to append
        
    Returns:
        Truncated string
    """
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix


def create_trace(id_: str, operation: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Create a trace entry for logging/debugging.
    
    Args:
        id_: Trace ID
        operation: Operation name
        metadata: Additional metadata
        
    Returns:
        Trace entry dictionary
    """
    return {
        "id": id_,
        "operation": operation,
        "timestamp": timestamp_now(),
        "metadata": metadata or {},
    }


def log_trace(trace: Dict[str, Any], level: str = "info") -> None:
    """
    Log a trace entry.
    
    Args:
        trace: Trace entry
        level: Log level
    """
    log_method = getattr(logger, level)
    # Convert numpy types to native Python types for JSON serialization
    def convert_numpy(obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(i) for i in obj]
        return obj
    
    safe_metadata = convert_numpy(trace['metadata'])
    log_method(f"[{trace['id']}] {trace['operation']}: {json.dumps(safe_metadata)}")


def measure_time(func, *args, **kwargs) -> Tuple[float, Any]:
    """
    Measure execution time of a function.
    
    Args:
        func: Function to execute
        args: Function arguments
        kwargs: Function keyword arguments
        
    Returns:
        Tuple of (execution_time, result)
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    return end - start, result


def retry_operation(func, max_retries: int = 3, backoff: float = 0.1) -> Any:
    """
    Retry an operation with exponential backoff.
    
    Args:
        func: Function to execute
        max_retries: Maximum number of retries
        backoff: Initial backoff time
        
    Returns:
        Function result
        
    Raises:
        Exception: If all retries fail
    """
    last_error = None
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(backoff * (2 ** attempt))
    
    raise last_error


def batch_size(items: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Split items into batches.
    
    Args:
        items: List of items
        batch_size: Size of each batch
        
    Returns:
        List of batches
    """
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]


def dict_to_tensor(data: Dict[str, Any], dim: int = 768) -> np.ndarray:
    """
    Convert dictionary to numpy tensor.
    
    Args:
        data: Dictionary with 'embedding' key
        dim: Target dimension
        
    Returns:
        Numpy array
    """
    if 'embedding' in data:
        vec = np.array(data['embedding'])
        if vec.shape[0] != dim:
            vec = np.pad(vec, (0, dim - vec.shape[0]), constant_values=0.0)
        return vec
    return np.zeros(dim)


def tensor_to_dict(tensor: np.ndarray) -> Dict[str, Any]:
    """
    Convert numpy tensor to dictionary.
    
    Args:
        tensor: Numpy array
        
    Returns:
        Dictionary with 'embedding' key
    """
    return {
        "embedding": tensor.tolist(),
        "dimension": int(tensor.shape[0]),
    }
