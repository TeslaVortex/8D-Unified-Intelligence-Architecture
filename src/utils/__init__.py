"""
Utils Module

Helper utilities and embeddings.
"""

from .embeddings import (
    EmbeddingFunction,
    normalize_vector,
    validate_embedding,
    cosine_similarity,
)
from .helpers import (
    clamp,
    generate_id,
    timestamp_now,
    safe_divide,
    interpolate,
    weighted_average,
    normalize_list,
    batch_process,
    merge_dicts,
    deep_copy,
    ensure_list,
    format_duration,
    truncate_string,
    create_trace,
    log_trace,
    measure_time,
    retry_operation,
    batch_size,
    dict_to_tensor,
    tensor_to_dict,
)

__all__ = [
    "EmbeddingFunction",
    "validate_embedding",
    "normalize_vector",
    "clamp_value",
    "cosine_similarity",
    "generate_id",
    "timestamp_now",
    "safe_divide",
    "interpolate",
    "weighted_average",
    "normalize_list",
    "batch_process",
    "merge_dicts",
    "deep_copy",
    "ensure_list",
    "format_duration",
    "truncate_string",
    "create_trace",
    "log_trace",
    "measure_time",
    "retry_operation",
    "batch_size",
    "dict_to_tensor",
    "tensor_to_dict",
]
