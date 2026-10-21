# 📋 Zed Rules: 8D Unified Intelligence Architecture

## Coding Standards & Guidelines

This document defines the coding standards, best practices, and quality gates for the 8D Unified Intelligence Architecture project.

---

## 1. Code Quality Standards

### 1.1 Python Style Guide

| Rule | Standard | Description |
|------|----------|-------------|
| **PEP 8** | Required | All code must follow PEP 8 style guidelines |
| **Line Length** | 100 chars | Maximum line length for readability |
| **Indentation** | 4 spaces | No tabs allowed |
| **Imports** | Ordered | Standard library → third-party → local |
| **Type Hints** | Required | All function parameters and return types |
| **Docstrings** | Required | All public classes, functions, and methods |

### 1.2 Naming Conventions

```python
# Classes - PascalCase
class NoveltyTensorEngine:
    pass

# Functions/Methods - snake_case
def detect_interference(self, pattern_a, pattern_b):
    pass

# Private methods - single underscore prefix
def _generate_response(self, evaluation):
    pass

# Constants - UPPER_SNAKE_CASE
MAX_COMPUTATION_TIME = 30
NOVELTY_MIN_SCORE = 0.3

# Variables - snake_case
embedding_vector = np.zeros(8)
pattern_id = "P_αβγδζηλθ"

# Module files - snake_case
novelty_engine.py
pattern_space_manager.py
```

### 1.3 Tensor & Mathematical Notation

```python
# Use clear variable names for tensors
# ❌ Bad
def compute(x, y):
    return x @ y

# ✅ Good
def dot_product(tensor_a, tensor_b):
    return np.dot(tensor_a, tensor_b)

# Use descriptive names for operations
def calculate_semantic_distance(v1, v2) -> float:
    """Calculate cosine distance between two 8D vectors."""
    pass

def calculate_structural_similarity(topo_a, topo_b) -> float:
    """Calculate Jaccard similarity on pattern topology."""
    pass
```

---

## 2. Architecture Rules

### 2.1 Component Separation

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPONENT RULES                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Novelty Engine    - Pure tensor operations             │
│     - No external dependencies                              │
│     - Stateless                                             │
│                                                             │
│  2. Pattern Space     - Storage & retrieval                │
│     - CRUD operations                                       │
│     - Cache management                                      │
│                                                             │
│  3. Dimensional Core  - 8D processing                      │
│     - Dimension-specific operations                         │
│     - Branching logic                                       │
│                                                             │
│  4. Meta-Compass      - Oversight & reasoning              │
│     - Self-monitoring                                       │
│     - Bias detection                                        │
│                                                             │
│  5. Orchestrator      - Integration layer                  │
│     - Coordinates all components                            │
│     - Manages execution flow                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Dependency Rules

- **No circular imports** between components
- **Single responsibility** - Each module does one thing well
- **Dependency injection** - Pass dependencies as parameters
- **Interface segregation** - Define clear interfaces

```python
# ✅ Good - Clear dependency injection
class UnifiedIntelligenceSystem:
    def __init__(
        self,
        meta_compass: MetaCompass,
        dimension_core: DimensionalCore,
        novelty_engine: NoveltyEngine
    ):
        self.meta_compass = meta_compass
        self.dimension_core = dimension_core
        self.novelty_engine = novelty_engine
```

---

## 3. Testing Requirements

### 3.1 Test Coverage Thresholds

| Component | Min Coverage | Priority |
|-----------|--------------|----------|
| Novelty Engine | 90% | P0 |
| Pattern Space | 90% | P0 |
| Dimensional Core | 85% | P0 |
| Meta-Compass | 85% | P0 |
| Orchestrator | 80% | P0 |
| Utils | 80% | P1 |

### 3.2 Test Categories

```
tests/
├── unit/              # Individual component tests
│   ├── novelty_engine/
│   ├── pattern_space/
│   ├── dimensions/
│   └── meta_compass/
├── integration/       # Component interaction tests
│   ├── pipeline/
│   └── end_to_end/
└── performance/       # Load and stress tests
    ├── latency/
    └── cost/
```

### 3.3 Test Naming Conventions

```python
# Test files - test_<module>.py
# Test functions - test_<function>_<scenario>()

# ✅ Good
def test_detect_interference_returns_float():
    pass

def test_register_pattern_stores_embedding():
    pass

def test_process_query_returns_reponse_and_trace():
    pass

def test_high_dimensionality_does_not_increase_cost():
    pass
```

### 3.4 Test Data Requirements

- **Test patterns** must represent real-world scenarios
- **Edge cases** must be covered (empty input, invalid data, etc.)
- **Performance tests** must measure cost and latency
- **Integration tests** must exercise full intelligence cycle

---

## 4. Performance Requirements

### 4.1 Latency Targets

| Operation | P50 | P95 | P99 |
|-----------|-----|-----|-----|
| Embedding | <100ms | <200ms | <500ms |
| Novelty Detection | <500ms | <1s | <2s |
| Full Cycle | <3s | <5s | <10s |

### 4.2 Cost Constraints

```python
# Cost per operation targets
MAX_EMBEDDING_COST = 0.001      # $0.001
MAX_NOVELTY_COST = 0.005        # $0.005
MAX_FULL_CYCLE_COST = 0.008     # $0.008
TARGET_OPTIMIZED_COST = 0.0003  # $0.0003 (96% reduction)
```

### 4.3 Scalability Requirements

- **Linear scaling**: O(n) cost, not O(n²)
- **Batch processing**: Support vectorized operations
- **Memory efficient**: <2GB per Lambda invocation
- **Cold start**: <10s for first invocation

---

## 5. Security Guidelines

### 5.1 Input Validation

```python
# All inputs must be validated
def process_query(self, query: str, context: Optional[dict] = None) -> dict:
    # Validate query
    if not query or len(query) < 1 or len(query) > 10000:
        raise ValueError("Query must be 1-10000 characters")
    
    # Validate context
    if context is not None:
        if not isinstance(context, dict):
            raise TypeError("Context must be a dictionary")
        if len(context) > 100:
            raise ValueError("Context too large")
```

### 5.2 Sensitive Data

- **No PII** in pattern embeddings
- **Data sanitization** before storage
- **Logging** without sensitive information

### 5.3 Error Handling

```python
# All exceptions must be handled gracefully
def detect_interference(self, pattern_a: Pattern, pattern_b: Pattern) -> float:
    try:
        # Compute novelty score
        return self._calculate_novelty(pattern_a, pattern_b)
    except ValueError as e:
        logger.warning(f"Invalid pattern: {e}")
        return 0.0  # Return safe default
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 0.0
```

---

## 6. Documentation Requirements

### 6.1 Docstring Format

```python
def function_name(self, param1, param2) -> ReturnType:
    """
    Brief description of what the function does.
    
    Args:
        param1 (type): Description of parameter 1
        param2 (type): Description of parameter 2
    
    Returns:
        ReturnType: Description of return value
    
    Raises:
        ExceptionType: When and why this exception is raised
    
    Example:
        >>> result = function_name(arg1, arg2)
        >>> print(result)
    """
    pass
```

### 6.2 Class Docstrings

```python
class ClassName:
    """
    Class-level description explaining the component's purpose.
    
    Attributes:
        attribute1 (type): Description
        attribute2 (type): Description
    
    Example Usage:
        >>> obj = ClassName()
        >>> result = obj.method()
    """
    pass
```

---

## 7. CI/CD Pipeline Rules

### 7.1 Pre-Commit Hooks

```bash
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.0
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
```

### 7.2 Pre-Merge Checklist

- [ ] All tests pass
- [ ] Code coverage >= 80%
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Performance benchmarks met
- [ ] Security review complete

### 7.3 Automated Checks

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=src --cov-report=html
      - name: Check coverage
        run: |
          coverage report
          if [ $(coverage report | grep "TOTAL" | awk '{print $3}') -lt 80 ]; then
            exit 1
          fi
      - name: Lint
        run: flake8 src/
      - name: Type check
        run: mypy src/
```

---

## 8. Sprint Quality Gates

### 8.1 Sprint Completion Checklist

Before marking a sprint as complete:

- [ ] All planned tasks completed
- [ ] All tests passing
- [ ] Code coverage meets threshold
- [ ] Performance benchmarks passed
- [ ] Documentation updated
- [ ] No critical bugs
- [ ] Progress.md updated with notes

### 8.2 Quality Verification Process

```bash
# Run verification after each sprint
./scripts/verify-sprint.sh

# This script runs:
# 1. Unit tests
# 2. Integration tests
# 3. Performance benchmarks
# 4. Cost analysis
# 5. Generate progress.md update
```

### 8.3 Verification Commands

```bash
# Full verification suite
pytest --cov=src --cov-report=term-missing

# Performance benchmarks
pytest tests/performance/ --benchmark-only

# Cost analysis
python scripts/cost_analysis.py

# Generate progress report
python scripts/generate_progress.py
```

---

## 9. Code Review Guidelines

### 9.1 Review Checklist

- [ ] Follows PEP 8 style
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Tests written
- [ ] Error handling appropriate
- [ ] Performance considerations addressed
- [ ] Security concerns addressed
- [ ] Dependencies justified

### 9.2 Review Comments Format

```python
# ❌ Bad review comment
# "This is wrong. Fix it."

# ✅ Good review comment
# "Consider adding a type hint for the return value.
#  This will help with static analysis and IDE support."
```

---

## 10. Progress Tracking

### 10.1 Progress.md Format

```markdown
# Progress Report - Sprint X

**Date**: YYYY-MM-DD
**Sprint Goal**: [Goal description]

## ✅ Completed Tasks

- [Task description]
- [Task description]

## ⚠️ Issues Encountered

| Issue | Impact | Resolution |
|-------|--------|------------|
| Description | High/Medium/Low | Resolution notes |

## 📊 Metrics

- **Test Coverage**: XX%
- **Performance**: XX ms (target: YY ms)
- **Cost per Query**: $0.XX (target: $0.XX)

## 📝 Notes

- Important observations
- Technical decisions
- Future considerations
```

### 10.2 Progress Tracking Template

See `progress.md` in the root directory for the current sprint progress.

---

## Appendix A: Quick Reference

### Common Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/novelty_engine/

# Run with coverage
pytest --cov=src --cov-report=html

# Check code style
flake8 src/

# Type check
mypy src/

# Run benchmarks
pytest tests/performance/ --benchmark-only

# Generate progress report
python scripts/generate_progress.py
```

### Project Structure Quick Reference

```
src/
├── novelty_engine/      # Core novelty detection
├── pattern_space/       # Pattern storage
├── dimensions/          # 8D processing
├── meta_compass/        # Oversight
├── logic_layers/        # Reasoning frameworks
└── orchestrator/        # Main system

tests/
├── unit/                # Component tests
├── integration/         # End-to-end tests
└── performance/         # Load tests
```

---

**Last Updated**: 2026-09-25  
**Version**: 1.0.0
