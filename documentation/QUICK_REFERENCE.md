# 📋 Quick Reference Card: 8D Unified Intelligence

## 🎯 One-Page Reference for Agents

**Keep this handy for instant access to critical project information**

---

## 📁 Project Structure

```
src/
├── novelty_engine/       # Core novelty detection (8D tensors)
│   ├── __init__.py
│   └── novelty_tensor_engine.py
├── pattern_space/        # Pattern storage & retrieval (LanceDB)
│   ├── __init__.py
│   ├── pattern_space_manager.py
│   └── pattern.py
├── dimensions/           # 8D processing (α through θ)
│   ├── __init__.py
│   ├── dimensional_processing_core.py
│   └── dimensions/
│       ├── input_sensory.py
│       ├── internal_state.py
│       ├── conceptual.py
│       ├── temporal.py
│       ├── social.py
│       ├── uncertainty.py
│       ├── evaluation.py
│       └── action_output.py
├── meta_compass/         # Meta-cognition & oversight
│   ├── __init__.py
│   ├── perspective_shift.py
│   └── self_monitor.py
├── logic_layers/         # Reasoning frameworks (5 tools)
│   ├── __init__.py
│   ├── logic_layers_toolkit.py
│   └── tools/
│       ├── socratic_decomposition.py
│       ├── first_principles.py
│       ├── systems_thinking.py
│       ├── five_whys.py
│       └── argument_mapping.py
├── orchestrator/         # Main system integration
│   ├── __init__.py
│   └── unified_intelligence_system.py
└── utils/                # Helper utilities
    ├── __init__.py
    ├── embeddings.py
    └── helpers.py
```

tests/
├── unit/                 # Component tests
├── integration/          # End-to-end tests
└── performance/          # Benchmarks
```

---

## 🏗️ System Architecture

```
Input → Embed → 8D Tensor → Interference Detection → Novelty →
→ Logic Application → Evaluation → Output → Feedback →
→ Pattern Update → 8D Tensor Update
```

**Core Equation:**
```
Output = MetaCompass(DimensionalProcessing(LogicLayers(NoveltyEngine(PatternSpace, Input))))
```

---

## 📐 8D Tensor Dimensions

| Symbol | Name | Purpose |
|--------|------|---------|
| α | Input Sensory | Perception quality |
| β | Internal State | Working memory load |
| γ | Conceptual Abstraction | Pattern recognition |
| δ | Temporal Context | Time horizon |
| ζ | Social/Cultural | Empathy/perspective |
| η | Uncertainty | Probability confidence |
| λ | Evaluation | Bias awareness |
| θ | Action/Output | Implementation readiness |

---

## ⚡ Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Embedding | <200ms | ✅ |
| Novelty Detection | <1s | ✅ |
| 8D Processing | <200ms | ✅ |
| Full Cycle | <3s | ✅ |
| Cost per Query | <$0.0003 | ✅ |
| Code Coverage | >80% | 100% |

---

## 🧪 Testing Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Sprint verification
bash scripts/verify-sprint.sh

# Cost analysis
python scripts/cost_analysis.py
```

---

## 📊 Documentation Files

| File | Purpose |
|------|---------|
| `documentation/8D-Unified-Intelligence-Architecture.md` | Architecture |
| `documentation/Implementation_plan.md` | Sprint roadmap |
| `documentation/zed-rules.md` | Coding standards |
| `documentation/progress.md` | Progress tracking |
| `documentation/STATUS.md` | Current status |
| `documentation/agent-workflow.md` | Agent workflow guide |

---

## 🚀 Sprint Workflow

### Pre-Sprint:
1. Read architecture docs
2. Read zed-rules.md
3. Check progress.md
4. Run `python scripts/verify-setup.py`

### During Sprint:
1. Plan tasks
2. Implement (follow zed-rules)
3. Write tests
4. Verify

### Post-Sprint:
1. Run `bash scripts/verify-sprint.sh`
2. Update `documentation/progress.md`
3. Mark sprint complete if all checks pass

---

## 🎯 Sprint 0: Foundation

**Status**: ✅ Ready to Begin

**Tasks**:
- [ ] Create src/ structure
- [ ] Setup serverless.yml
- [ ] Initialize LanceDB
- [ ] Create base project structure

**Reference**: `documentation/Implementation_plan.md` → Sprint 0

---

## 📝 Coding Rules (Zed Rules)

### Naming:
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

### Requirements:
- Type hints: ✅ Required
- Docstrings: ✅ Required
- PEP 8: ✅ Required
- Line length: ≤100 chars

### Testing:
- Unit tests: ✅ Required
- Integration tests: ✅ Required
- Coverage: >80%

---

## 💰 Cost Model

**Monthly (10M queries)**: ~$55
- Compute: $40
- Vector DB: $0
- Embedding API: $10
- Storage: $5

**Per Query**: $0.0000055

---

## 🔧 Useful Commands

```bash
# Verify setup
python scripts/verify-setup.py

# Run tests
pytest

# Check coverage
pytest --cov=src

# Sprint verification
bash scripts/verify-sprint.sh

# Cost analysis
python scripts/cost_analysis.py

# Generate progress
python scripts/generate_progress.py
```

---

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| Import error | Add `src/` to path |
| Tests failing | Check zed-rules.md, run flake8 |
| Slow performance | Enable caching, use vectorized ops |
| Type hints error | Use Python 3.11+ |

---

## 📞 Quick Links

- **Architecture**: `documentation/8D-Unified-Intelligence-Architecture.md`
- **Rules**: `documentation/zed-rules.md`
- **Sprints**: `documentation/Implementation_plan.md`
- **Progress**: `documentation/progress.md`
- **Status**: `documentation/STATUS.md`
- **Workflow**: `documentation/agent-workflow.md`

---

**🎯 Pro Tip**: Before starting any task, check `documentation/STATUS.md` for current sprint status!
