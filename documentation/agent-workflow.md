# 🧠 Agent Workflow Guide: 8D Unified Intelligence Architecture

## Purpose

This document provides the agent with all necessary context to work on the 8D Unified Intelligence Architecture project **without needing to search through the entire codebase** each session.

**Last Updated**: 2026-09-25  
**Version**: 1.0.0

---

## 📁 Project Structure Overview

```
8D-Unified-Intelligence-Architecture/
├── src/                          # Source code (to be created in Sprint 0)
│   ├── novelty_engine/           # Core novelty detection
│   │   ├── __init__.py
│   │   ├── novelty_tensor_engine.py    # NoveltyTensorEngine class
│   │   ├── tensor_operations.py        # 8D tensor operations
│   │   └── novelty_types.py            # 7 novelty modes
│   ├── pattern_space/            # Pattern storage & retrieval
│   │   ├── __init__.py
│   │   ├── pattern_space_manager.py    # PatternSpaceManager class
│   │   └── pattern.py                 # Pattern data structure
│   ├── dimensions/               # 8D processing core
│   │   ├── __init__.py
│   │   ├── dimensional_core.py        # DimensionalProcessingCore class
│   │   └── dimensions/                # Individual dimension modules
│   │       ├── input_sensory.py       # α dimension
│   │       ├── internal_state.py      # β dimension
│   │       ├── conceptual.py          # γ dimension
│   │       ├── temporal.py            # δ dimension
│   │       ├── social.py              # ζ dimension
│   │       ├── uncertainty.py         # η dimension
│   │       ├── evaluation.py          # λ dimension
│   │       └── action_output.py       # θ dimension
│   ├── meta_compass/             # Meta-cognition & oversight
│   │   ├── __init__.py
│   │   ├── perspective_shift.py       # PerspectiveShiftCore class
│   │   └── self_monitoring.py         # Self-monitoring logic
│   ├── logic_layers/             # Reasoning frameworks
│   │   ├── __init__.py
│   │   ├── toolkit.py                 # LogicLayersToolkit class
│   │   ├── socratic.py                # Socratic Decomposition
│   │   ├── first_principles.py        # First Principles Abduction
│   │   ├── systems_thinking.py        # Systems Thinking
│   │   ├── five_whys.py               # 5 Whys Root Cause
│   │   └── argument_mapping.py        # Argument Mapping
│   ├── orchestrator/             # Main system integration
│   │   ├── __init__.py
│   │   └── unified_intelligence_system.py  # UnifiedIntelligenceSystem class
│   ├── utils/                    # Helper utilities
│   │   ├── __init__.py
│   │   ├── embeddings.py              # Embedding functions
│   │   └── helpers.py                 # Utility helpers
│   └── tests/                    # Test suite
│       ├── __init__.py
│       ├── unit/                  # Unit tests
│       ├── integration/           # Integration tests
│       └── performance/           # Performance benchmarks
├── docs/                         # Documentation (for reference)
│   └── architecture.md
├── documentation/                # Project documentation
│   ├── 8D-Unified-Intelligence-Architecture.md    # Architecture docs
│   ├── Implementation_plan.md                      # Sprint roadmap
│   ├── zed-rules.md                                # Coding standards
│   ├── progress.md                                 # Progress tracking
│   └── STATUS.md                                   # Current status
├── scripts/                      # Automation scripts
│   ├── verify-sprint.sh          # Sprint verification script
│   ├── cost_analysis.py          # Cost analysis tool
│   ├── generate_progress.py      # Progress report generator
│   └── verify-setup.py           # Setup verification (just created)
├── serverless.yml                # AWS Lambda deployment config
├── requirements.txt              # Python dependencies
├── README.md                     # Project overview
└── .gitignore                    # Git ignore rules
```

---

## 📖 Key Documentation Files

| File | Purpose | When to Reference |
|------|---------|-------------------|
| **documentation/8D-Unified-Intelligence-Architecture.md** | Complete system architecture | Understanding system design, component interfaces |
| **documentation/Implementation_plan.md** | Sprint-by-sprint breakdown | Planning tasks, estimating effort |
| **documentation/zed-rules.md** | Coding standards & rules | Writing code, code reviews, testing |
| **documentation/progress.md** | Sprint progress tracking | Status updates, verification results |
| **documentation/STATUS.md** | Current project status | Quick status check, next actions |

---

## 🎯 Coding Rules (Zed Rules Summary)

### 1. Code Quality Standards
- **PEP 8**: All code must follow PEP 8 style
- **Line Length**: Max 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Type Hints**: Required for all functions
- **Docstrings**: Required for all public APIs

### 2. Naming Conventions
```python
# Classes - PascalCase
class NoveltyTensorEngine:
    pass

# Functions - snake_case
def detect_interference(self, pattern_a, pattern_b):
    pass

# Constants - UPPER_SNAKE_CASE
MAX_COMPUTATION_TIME = 30
NOVELTY_MIN_SCORE = 0.3

# Variables - snake_case
embedding_vector = np.zeros(8)
```

### 3. Component Separation
- **Novelty Engine**: Pure tensor operations, stateless
- **Pattern Space**: Storage & retrieval, cache management
- **Dimensional Core**: 8D processing, branching logic
- **Meta-Compass**: Oversight, bias detection
- **Orchestrator**: Integration, execution flow

### 4. Testing Requirements
- **Novelty Engine**: 90% coverage
- **Pattern Space**: 90% coverage
- **Dimensional Core**: 85% coverage
- **Meta-Compass**: 85% coverage
- **Orchestrator**: 80% coverage

### 5. Performance Targets
| Operation | P95 Target | P99 Target |
|-----------|------------|------------|
| Embedding | <200ms | <500ms |
| Novelty Detection | <1s | <2s |
| Full Cycle | <5s | <10s |

### 6. Cost Constraints
- Embedding: <$0.001
- Novelty Detection: <$0.005
- Full Cycle: <$0.008
- Optimized Target: <$0.0003

---

## 🚀 Sprint Workflow

### Pre-Sprint Checklist (Before Starting)

1. ✅ Read `documentation/8D-Unified-Intelligence-Architecture.md` for context
2. ✅ Read `documentation/zed-rules.md` for coding standards
3. ✅ Read `documentation/Implementation_plan.md` for sprint tasks
4. ✅ Check `documentation/progress.md` for current status
5. ✅ Run `python scripts/verify-setup.py` to confirm setup

### During Sprint

1. **Plan Tasks**
   - Review sprint tasks in Implementation_plan.md
   - Break down into smaller actionable items
   - Estimate effort in hours

2. **Implement**
   - Follow zed-rules.md coding standards
   - Write code with type hints and docstrings
   - Test as you go

3. **Test**
   - Write unit tests for each component
   - Run `pytest tests/unit/`
   - Ensure all tests pass

4. **Verify**
   - Run `bash scripts/verify-sprint.sh`
   - Check all verification phases pass
   - Review cost analysis with `python scripts/cost_analysis.py`

5. **Document**
   - Update `documentation/progress.md` with notes
   - Add any new documentation needed
   - Update README.md if API changed

### Post-Sprint Checklist (After Completion)

- [ ] All tasks completed
- [ ] All tests passing
- [ ] Code coverage meets threshold
- [ ] Performance benchmarks passed
- [ ] Documentation updated
- [ ] `bash scripts/verify-sprint.sh` passed
- [ ] `documentation/progress.md` updated with:
  - Verification date
  - Verification status
  - Metrics achieved
  - Issues encountered
  - Technical decisions

---

## 🧪 Verification Process

### After Each Sprint, Run:

```bash
# 1. Full verification
bash scripts/verify-sprint.sh

# 2. Cost analysis
python scripts/cost_analysis.py

# 3. Generate progress report
python scripts/generate_progress.py
```

### Verification Phases:

1. **Phase 1: Code Quality**
   - Repository structure
   - Python files present
   - Type hints present
   - Docstrings present

2. **Phase 2: Unit Tests**
   - Test files exist
   - Tests pass
   - Coverage check

3. **Phase 3: Integration Tests**
   - Integration tests exist
   - Tests pass

4. **Phase 4: Performance Benchmarks**
   - Performance tests exist
   - Benchmarks pass
   - Targets met

5. **Phase 5: Documentation**
   - README.md exists
   - Architecture docs exist
   - Implementation plan exists
   - Zed rules exist
   - Progress tracking exists

---

## 📊 Common Tasks & References

### Creating a New Component

1. **Reference**: `documentation/8D-Unified-Intelligence-Architecture.md`
2. **Follow**: `documentation/zed-rules.md` naming conventions
3. **Test**: Create tests in `tests/unit/<component>/`
4. **Document**: Add docstrings and class-level documentation

### Example Component Structure

```python
# src/<component>/module.py
from typing import Optional, List, Dict, Any
import numpy as np

class ComponentName:
    """
    Brief description of the component's purpose.
    
    Attributes:
        attribute1 (type): Description
        attribute2 (type): Description
    
    Example Usage:
        >>> obj = ComponentName()
        >>> result = obj.method()
    """
    
    def __init__(self, param1: int = 10, param2: str = "default"):
        """
        Initialize the component.
        
        Args:
            param1 (int): Description
            param2 (str): Description
        """
        self.param1 = param1
        self.param2 = param2
    
    def method_name(self, arg1: str) -> float:
        """
        Brief description of the method.
        
        Args:
            arg1 (str): Description
        
        Returns:
            float: Description of return value
        
        Raises:
            ValueError: When and why this exception is raised
        
        Example:
            >>> result = method_name("test")
            >>> print(result)
        """
        # Implementation
        pass
```

### Testing a New Component

```python
# tests/unit/<component>/test_module.py
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

class TestComponentName:
    """Tests for ComponentName"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.component = ComponentName()
    
    def test_initialization_with_defaults(self):
        """Test initialization with default values"""
        assert self.component.param1 == 10
        assert self.component.param2 == "default"
    
    def test_method_name_returns_float(self):
        """Test method returns float"""
        result = self.component.method_name("test")
        assert isinstance(result, float)
```

---

## 🔧 Development Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/novelty_engine/

# Check code style
flake8 src/

# Type check
mypy src/

# Run benchmarks
pytest tests/performance/ --benchmark-only

# Generate progress report
python scripts/generate_progress.py

# Run cost analysis
python scripts/cost_analysis.py
```

---

## 🚨 Common Issues & Solutions

### Issue: Import errors
**Solution**: Ensure `src/` is in Python path
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
```

### Issue: Type hints not working
**Solution**: Use Python 3.11+ and install `typing-extensions`

### Issue: Tests failing
**Solution**: 
1. Check `zed-rules.md` for coding standards
2. Run `flake8 src/` to check style
3. Run `mypy src/` to check types

### Issue: Performance too slow
**Solution**: 
1. Enable caching
2. Use vectorized operations
3. Review `cost_analysis.py` for optimization targets

---

## 📞 Quick Reference

### Key Files by Purpose

| Need | Reference File |
|------|----------------|
| System architecture | `documentation/8D-Unified-Intelligence-Architecture.md` |
| Sprint tasks | `documentation/Implementation_plan.md` |
| Coding rules | `documentation/zed-rules.md` |
| Progress tracking | `documentation/progress.md` |
| Current status | `documentation/STATUS.md` |
| Project overview | `README.md` |

### Key Scripts by Purpose

| Task | Script |
|------|--------|
| Sprint verification | `bash scripts/verify-sprint.sh` |
| Cost analysis | `python scripts/cost_analysis.py` |
| Progress report | `python scripts/generate_progress.py` |
| Setup verification | `python scripts/verify-setup.py` |

---

## 🎯 Sprint 0: Foundation & Infrastructure

**Current Status**: ✅ Ready to Begin

**Tasks**:
1. Create `src/` directory structure
2. Create `serverless.yml` for AWS Lambda
3. Initialize vector database (LanceDB)
4. Set up basic project structure

**Reference**: `documentation/Implementation_plan.md` - Sprint 0 section

---

## 📝 Notes for Agent

- **Always read** `documentation/zed-rules.md` before writing code
- **Always update** `documentation/progress.md` after completing tasks
- **Always run** `bash scripts/verify-sprint.sh` before marking sprint complete
- **Follow PEP 8** and type hints for all code
- **Write tests** as you implement features
- **Track metrics** in progress.md (coverage, performance, cost)

---

**This guide is your complete reference. No need to search the codebase - everything you need is documented here.**
