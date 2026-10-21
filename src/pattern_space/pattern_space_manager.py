"""
Pattern Space Manager Module

Manages pattern storage and retrieval in the 8D space.
"""

import json
import os
import threading
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple

import lancedb
import lancedb.expr as lancedb_expr
import numpy as np
import pyarrow as pa

from .pattern import Pattern

# Define LanceDB schema manually since Pattern is a dataclass
# PyArrow schema definition for LanceDB
# Note: metadata and dimensions are stored as JSON strings
_PATTERN_SCHEMA = pa.schema([
    ("pattern_id", pa.string()),
    ("embedding", pa.list_(pa.float64(), 8)),
    ("metadata", pa.string()),
    ("activation_count", pa.int32()),
    ("last_accessed", pa.string()),
    ("tags", pa.list_(pa.string())),
    ("dimensions", pa.string()),
])


class PatternSpaceManager:
    """
    Manager for pattern storage and retrieval.
    
    Provides CRUD operations for patterns, similarity search,
    and cache management using LanceDB as the vector database.
    
    Attributes:
        db_path: Path to LanceDB database
        cache_ttl: Cache time-to-live in seconds
        max_cache_size: Maximum number of cached patterns
    """
    
    def __init__(
        self,
        db_path: Optional[str] = None,
        cache_ttl: int = 3600,
        max_cache_size: int = 1000,
    ):
        """
        Initialize the pattern space manager.
        
        Args:
            db_path: Path to LanceDB database (default: /tmp/lancedb)
            cache_ttl: Cache time-to-live in seconds (default: 3600)
            max_cache_size: Maximum cached patterns (default: 1000)
        """
        self.db_path = db_path or "/tmp/lancedb"
        self.cache_ttl = cache_ttl
        self.max_cache_size = max_cache_size
        
        # Ensure directory exists
        os.makedirs(self.db_path, exist_ok=True)
        
        # Initialize cache
        self._cache: Dict[str, Pattern] = {}
        
        # Initialize database
        self._db = None
        self._table = None
        self._lock = threading.Lock()
        self._initialized = False
        
        self._connect()
    
    def _connect(self) -> None:
        """Connect to the LanceDB database."""
        try:
            self._db = lancedb.connect(self.db_path)
            self._table = self._db.create_table(
                "patterns",
                schema=_PATTERN_SCHEMA,
            )
            # Create vector index for similarity search
            # Use cosine distance for the embedding column
            try:
                # LanceDB 0.39+ uses different API for index creation
                # Try the new API first
                self._table.create_index(
                    name="embedding_idx",
                    metric="COSINE"
                )
            except TypeError:
                # Fallback to old API for older versions
                self._table.create_index(
                    column="embedding",
                    index_type="AUTO",
                    metric="COSINE"
                )
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Index creation failed: {e}, will use brute-force search")
            
            self._initialized = True
        except Exception as e:
            # Fallback to in-memory if connection fails
            self._db = None
            self._table = None
            self._initialized = False
            # Log but don't raise - allow system to continue
            import logging
            logging.getLogger(__name__).warning(f"LanceDB connection failed: {e}, using in-memory storage")
    
    def _disconnect(self) -> None:
        """Disconnect from the LanceDB database."""
        if self._db is not None:
            self._db.close()
            self._db = None
            self._table = None
            self._initialized = False
            self._cache.clear()
    
    def register_pattern(
        self,
        pattern: Pattern,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Register a new pattern in the space.
        
        Args:
            pattern: Pattern to register
            metadata: Additional metadata
        
        Returns:
            Pattern ID
        """
        with self._lock:
            # Ensure pattern is initialized
            if pattern.last_accessed is None:
                pattern.last_accessed = datetime.now()
            
            # Convert pattern to LanceDB-compatible format
            pattern_data = self._pattern_to_lancedb(pattern)
            
            # Add to database if connected
            if self._table is not None:
                self._table.add([pattern_data])
            
            # Update cache
            self._cache[pattern.pattern_id] = pattern
            
            # Update pattern metadata
            if metadata:
                pattern.update_metadata("registered_at", datetime.now().isoformat())
                for key, value in metadata.items():
                    pattern.update_metadata(key, value)
            
            return pattern.pattern_id
    
    def _pattern_to_lancedb(self, pattern: Pattern) -> Dict[str, Any]:
        """
        Convert a Pattern to LanceDB-compatible dictionary format.
        
        Args:
            pattern: Pattern to convert
        
        Returns:
            Dictionary compatible with LanceDB schema
        """
        return {
            "pattern_id": pattern.pattern_id,
            "embedding": pattern.embedding,
            "metadata": json.dumps(pattern.metadata),
            "activation_count": pattern.activation_count,
            "last_accessed": pattern.last_accessed.isoformat() if pattern.last_accessed else None,
            "tags": pattern.tags,
            "dimensions": json.dumps(pattern.dimensions),
        }
    
    def _lancedb_to_pattern(self, data: Dict[str, Any]) -> Pattern:
        """
        Convert LanceDB dictionary to Pattern.
        
        Args:
            data: Dictionary from LanceDB (single row)
        
        Returns:
            Pattern instance
        """
        last_accessed = None
        if data.get("last_accessed"):
            last_accessed = datetime.fromisoformat(data["last_accessed"])
        
        # Handle list wrapping that can happen with arrow data
        def extract_value(val):
            if isinstance(val, list):
                if len(val) > 0:
                    # Check if it's a list of lists (arrow format)
                    if isinstance(val[0], list):
                        return val[0]
                return val
            return val
        
        # Handle PyArrow scalar values
        def handle_pyarrow_scalar(val):
            if hasattr(val, 'as_py'):
                return val.as_py()
            return val
        
        return Pattern(
            pattern_id=handle_pyarrow_scalar(data["pattern_id"]),
            embedding=handle_pyarrow_scalar(data["embedding"]),
            metadata=json.loads(handle_pyarrow_scalar(data.get("metadata", "{}"))),
            activation_count=int(handle_pyarrow_scalar(data.get("activation_count", 0))),
            last_accessed=last_accessed,
            tags=handle_pyarrow_scalar(data.get("tags", [])),
            dimensions=json.loads(handle_pyarrow_scalar(data.get("dimensions", "{}"))),
        )
    
    def get_pattern(self, pattern_id: str) -> Optional[Pattern]:
        """
        Retrieve a pattern by ID.
        
        Args:
            pattern_id: Pattern identifier
        
        Returns:
            Pattern or None if not found
        """
        with self._lock:
            # Check cache first
            if pattern_id in self._cache:
                pattern = self._cache[pattern_id]
                pattern.activate()
                
                # Refresh from database if expired
                if self._table is not None:
                    cached_time = pattern.last_accessed
                    if cached_time and (datetime.now() - cached_time).total_seconds() > self.cache_ttl:
                        # Search by pattern_id in database using filter
                        try:
                            query = self._table.search([[]]).filter(f'pattern_id == "{pattern_id}"').limit(1)
                            arrow_table = query.to_arrow()
                            if arrow_table.num_rows > 0:
                                row = arrow_table.slice(0, 1).to_pydict()
                                pattern = self._lancedb_to_pattern(row)
                                self._cache[pattern_id] = pattern
                            else:
                                del self._cache[pattern_id]
                        except Exception:
                            del self._cache[pattern_id]
                
                return pattern
            
            # Query database (pattern not in cache)
            # Use filter to find by pattern_id
            if self._table is not None:
                try:
                    # Use filter to find by pattern_id (exact match)
                    query = self._table.search([[]]).filter(f'pattern_id == "{pattern_id}"').limit(1)
                    arrow_table = query.to_arrow()
                    if arrow_table.num_rows > 0:
                        row = arrow_table.slice(0, 1).to_pydict()
                        pattern = self._lancedb_to_pattern(row)
                        self._cache[pattern_id] = pattern
                        return pattern
                except Exception as e:
                    # If filter doesn't work, fall back to full scan
                    import logging
                    logging.getLogger(__name__).debug(f"Filter query failed: {e}")
                    pass
            
            return None
    
    def find_similar_patterns(
        self,
        embedding: List[float],
        top_k: int = 5,
        threshold: float = 0.8,
    ) -> List[Tuple[Pattern, float]]:
        """
        Find patterns similar to an embedding.
        
        Args:
            embedding: Query embedding
            top_k: Number of results to return
            threshold: Minimum similarity threshold
        
        Returns:
            List of (pattern, similarity) tuples
        """
        results = []
        
        with self._lock:
            if self._table is not None:
                try:
                    # Query LanceDB using cosine distance
                    # Use numpy array for better compatibility
                    import numpy as np
                    query_vector = np.array(embedding, dtype=np.float64)
                    
                    # Perform vector search
                    query = self._table.search(query_vector).limit(top_k).metric("COSINE")
                    arrow_table = query.to_arrow()
                    
                    if arrow_table.num_rows > 0:
                        for i in range(arrow_table.num_rows):
                            row = arrow_table.slice(i, 1).to_pydict()
                            pattern = self._lancedb_to_pattern(row)
                            
                            # Calculate similarity
                            similarity = self._calculate_similarity(embedding, pattern.embedding)
                            
                            if similarity >= threshold:
                                results.append((pattern, similarity))
                            
                            # Early exit if we have enough results above threshold
                            if len(results) >= top_k:
                                break
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).debug(f"Similarity search failed: {e}")
                    # Fallback to brute-force search through cache
                    import numpy as np
                    for pattern_id, pattern in self._cache.items():
                        similarity = self._calculate_similarity(embedding, pattern.embedding)
                        if similarity >= threshold:
                            results.append((pattern, similarity))
        
        # Sort by similarity
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_k]
    
    def _calculate_similarity(
        self,
        v1: List[float],
        v2: List[float],
    ) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            v1: First vector
            v2: Second vector
        
        Returns:
            Similarity score (0-1)
        """
        import numpy as np
        
        v1_np = np.array(v1, dtype=np.float64)
        v2_np = np.array(v2, dtype=np.float64)
        
        norm1 = np.linalg.norm(v1_np)
        norm2 = np.linalg.norm(v2_np)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = np.dot(v1_np, v2_np) / (norm1 * norm2)
        return float(np.clip(similarity, 0.0, 1.0))
    
    def delete_pattern(self, pattern_id: str) -> bool:
        """
        Delete a pattern from the space.
        
        Args:
            pattern_id: Pattern identifier
        
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            # Check if pattern exists in cache before deletion
            existed_in_cache = pattern_id in self._cache
            
            # Remove from cache
            if pattern_id in self._cache:
                del self._cache[pattern_id]
            
            # Remove from database if connected
            if self._table is not None:
                try:
                    # Delete by pattern_id using LanceDB's expr module
                    self._table.delete(lancedb_expr.col("pattern_id").eq(pattern_id))
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).debug(f"Delete failed: {e}")
            
            # Return True only if pattern was actually deleted
            return existed_in_cache
    
    def update_pattern(self, pattern_id: str, embedding: List[float]) -> bool:
        """
        Update a pattern's embedding.
        
        Args:
            pattern_id: Pattern identifier
            embedding: New embedding
        
        Returns:
            True if updated, False if not found
        """
        # Get existing pattern
        pattern = self.get_pattern(pattern_id)
        if pattern is None:
            return False
        
        # Update embedding
        pattern.embedding = embedding
        
        # Update in database
        if self._table is not None:
            try:
                pattern_data = self._pattern_to_lancedb(pattern)
                # Delete and re-add the pattern
                self._table.delete(lancedb_expr.col("pattern_id").eq(pattern_id))
                self._table.add([pattern_data])
            except Exception as e:
                import logging
                logging.getLogger(__name__).debug(f"Update failed: {e}")
                return False
        
        return True
    
    def get_active_patterns(self, min_activations: int = 1) -> List[Pattern]:
        """
        Get patterns with minimum activation count.
        
        Args:
            min_activations: Minimum activation count
        
        Returns:
            List of active patterns
        """
        with self._lock:
            return [
                pattern for pattern in self._cache.values()
                if pattern.activation_count >= min_activations
            ]
    
    def clear_cache(self) -> None:
        """Clear the pattern cache."""
        with self._lock:
            self._cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        with self._lock:
            total = len(self._cache)
            active = sum(1 for p in self._cache.values() if p.activation_count > 0)
            
            return {
                "total_patterns": total,
                "active_patterns": active,
                "cache_ttl_seconds": self.cache_ttl,
                "max_cache_size": self.max_cache_size,
            }
    
    def persist(self) -> None:
        """Force persist all patterns to disk."""
        if self._table is not None:
            try:
                # Clear all patterns from database
                self._table.delete([])
                
                # Re-add all patterns from cache
                for pattern in self._cache.values():
                    pattern_data = self._pattern_to_lancedb(pattern)
                    self._table.add([pattern_data])
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Persist failed: {e}")
                # Fallback: just add without clearing
                for pattern in self._cache.values():
                    pattern_data = self._pattern_to_lancedb(pattern)
                    self._table.add([pattern_data])
    
    def get_registered_patterns(self, limit: int = 100) -> List[Pattern]:
        """
        Get all registered patterns.
        
        Args:
            limit: Maximum number of patterns to return
        
        Returns:
            List of patterns
        """
        with self._lock:
            return list(self._cache.values())[:limit]
    
    def close(self) -> None:
        """Close the database connection."""
        with self._lock:
            # Clear cache first
            self._cache.clear()
            
            # Close database connection
            if self._db is not None:
                # LanceDB uses context manager, close the connection properly
                import gc
                self._db = None
                self._table = None
                self._initialized = False
            
            # Force garbage collection
            gc.collect()
    
    @property
    def cache(self) -> Dict[str, Pattern]:
        """Get the pattern cache."""
        return self._cache
    
    @cache.setter
    def cache(self, value: Dict[str, Pattern]) -> None:
        """Set the pattern cache."""
        self._cache = value
    
    def __len__(self) -> int:
        """Return number of cached patterns."""
        return len(self._cache)
    
    def __repr__(self) -> str:
        return f"PatternSpaceManager(db_path={self.db_path}, cache_size={len(self._cache)}, cache_ttl={self.cache_ttl}s)"
    
    def __str__(self) -> str:
        return self.__repr__()


# Global singleton instance
_pattern_space_manager: Optional[PatternSpaceManager] = None

def get_pattern_space_manager() -> PatternSpaceManager:
    """Get the global pattern space manager instance."""
    global _pattern_space_manager
    if _pattern_space_manager is None:
        _pattern_space_manager = PatternSpaceManager()
    return _pattern_space_manager
