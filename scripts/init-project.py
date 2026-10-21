#!/usr/bin/env python3
"""
Project Initialization Script for 8D Unified Intelligence Architecture
Creates the base project structure for Sprint 0
"""

import os
import sys
import shutil
from pathlib import Path


def create_directory(path: str) -> None:
    """Create directory if it doesn't exist"""
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True)
        print(f"✓ Created directory: {path}")


def create_file(path: str, content: str = "") -> None:
    """Create file with optional content"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✓ Created file: {path}")


def create_empty_file(path: str) -> None:
    """Create empty file"""
    create_file(path)


def main():
    """Initialize project structure"""
    
    print("\n" + "=" * 60)
    print("🚀 8D Unified Intelligence - Project Initialization")
    print("=" * 60)
    print()
    
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print(f"Project Root: {project_root}")
    print()
    
    # Create src directory structure
    print("Creating src/ directory structure...")
    print("-" * 60)
    
    src_dir = project_root / "src"
    create_directory(src_dir)
    
    # novelty_engine
    novelty_engine_dir = src_dir / "novelty_engine"
    create_directory(novelty_engine_dir)
    create_file(novelty_engine_dir / "__init__.py")
    create_file(novelty_engine_dir / "novelty_tensor_engine.py")
    create_file(novelty_engine_dir / "tensor_operations.py")
    create_file(novelty_engine_dir / "novelty_types.py")
    print("✓ novelty_engine/")
    
    # pattern_space
    pattern_space_dir = src_dir / "pattern_space"
    create_directory(pattern_space_dir)
    create_file(pattern_space_dir / "__init__.py")
    create_file(pattern_space_dir / "pattern_space_manager.py")
    create_file(pattern_space_dir / "pattern.py")
    print("✓ pattern_space/")
    
    # dimensions
    dimensions_dir = src_dir / "dimensions"
    create_directory(dimensions_dir)
    create_file(dimensions_dir / "__init__.py")
    dimensions = [
        "input_sensory.py",
        "internal_state.py",
        "conceptual.py",
        "temporal.py",
        "social.py",
        "uncertainty.py",
        "evaluation.py",
        "action_output.py"
    ]
    for dim_file in dimensions:
        create_file(dimensions_dir / dim_file)
    print("✓ dimensions/")
    
    # meta_compass
    meta_compass_dir = src_dir / "meta_compass"
    create_directory(meta_compass_dir)
    create_file(meta_compass_dir / "__init__.py")
    create_file(meta_compass_dir / "perspective_shift.py")
    create_file(meta_compass_dir / "self_monitoring.py")
    print("✓ meta_compass/")
    
    # logic_layers
    logic_layers_dir = src_dir / "logic_layers"
    create_directory(logic_layers_dir)
    create_file(logic_layers_dir / "__init__.py")
    create_file(logic_layers_dir / "toolkit.py")
    create_file(logic_layers_dir / "socratic.py")
    create_file(logic_layers_dir / "first_principles.py")
    create_file(logic_layers_dir / "systems_thinking.py")
    create_file(logic_layers_dir / "five_whys.py")
    create_file(logic_layers_dir / "argument_mapping.py")
    print("✓ logic_layers/")
    
    # orchestrator
    orchestrator_dir = src_dir / "orchestrator"
    create_directory(orchestrator_dir)
    create_file(orchestrator_dir / "__init__.py")
    create_file(orchestrator_dir / "unified_intelligence_system.py")
    print("✓ orchestrator/")
    
    # utils
    utils_dir = src_dir / "utils"
    create_directory(utils_dir)
    create_file(utils_dir / "__init__.py")
    create_file(utils_dir / "embeddings.py")
    create_file(utils_dir / "helpers.py")
    print("✓ utils/")
    
    # tests directory structure
    print("\nCreating tests/ directory structure...")
    print("-" * 60)
    
    tests_dir = project_root / "tests"
    create_directory(tests_dir)
    
    # unit tests
    unit_dir = tests_dir / "unit"
    create_directory(unit_dir)
    create_empty_file(unit_dir / "__init__.py")
    print("✓ tests/unit/")
    
    # integration tests
    integration_dir = tests_dir / "integration"
    create_directory(integration_dir)
    create_empty_file(integration_dir / "__init__.py")
    print("✓ tests/integration/")
    
    # performance tests
    performance_dir = tests_dir / "performance"
    create_directory(performance_dir)
    create_empty_file(performance_dir / "__init__.py")
    print("✓ tests/performance/")
    
    # Create conftest.py
    create_file(tests_dir / "conftest.py", """
"""pytest configuration for 8D Unified Intelligence"""

import pytest

# Add src to path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Global fixtures
@pytest.fixture
def test_pattern():
    """Test pattern fixture"""
    return type('Pattern', (), {
        'embedding': [1.0] * 8,
        'id': 'test_pattern'
    })()
""")
    print("✓ tests/conftest.py")
    
    # Create requirements.txt
    print("\nCreating requirements.txt...")
    print("-" * 60)
    
    requirements = """# 8D Unified Intelligence Architecture
# Core dependencies
numpy>=1.24.0
pandas>=2.0.0

# ML/Vector Operations
scikit-learn>=1.3.0
faiss-cpu>=1.7.0

# Serverless
aws-lambda-powertools>=2.0.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-benchmark>=4.0.0

# Utilities
python-dateutil>=2.8.0
tqdm>=4.66.0

# Type checking
mypy>=1.0.0
types-requests>=2.28.0

# Code quality
flake8>=6.0.0
black>=23.1.0
isort>=5.12.0
"""
    create_file(project_root / "requirements.txt", requirements)
    print("✓ requirements.txt")
    
    # Create serverless.yml
    print("\nCreating serverless.yml...")
    print("-" * 60)
    
    serverless_config = """# Serverless configuration for 8D Unified Intelligence
# Deploy to AWS Lambda

service: unified-intelligence

frameworkVersion: "3"

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  environment:
    NODE_ENV: production
    CACHE_ENABLED: true
    MAX_WORKERS: 8
    VECTOR_DB_PATH: /tmp/novelty_vectors
  memorySize: 2048  # 2GB
  timeout: 30
  iam:
    role: arn:aws:iam::123456789012:role/lambda-execution-role
  logs:
    reportStyle: Tail

functions:
  handler:
    handler: main.handler
    environment:
      - NODE_ENV=production
      - CACHE_ENABLED=true
      - MAX_WORKERS=8
      - VECTOR_DB_PATH=/tmp/novelty_vectors
    memorySize: 2048
    timeout: 30
    events:
      - http:
          path: /{path+}
          method: GET,POST
    layers:
      - arn:aws:lambda:us-east-1:123456789012:layer:python-extensions:1
    cold_start_optimization:
      lazy_loading: true
      warm_pool:
        size: 10
        type: provisioned_concurrency

resources:
  DescribeFunctions:
    - handler
  DescribeEvents:
    - handler

plugins:
  - serverless-powertools

custom:
  powertools:
    metrics:
      namespace: UnifiedIntelligence
      dimensions:
        - operation
        - dimension
"""
    create_file(project_root / "serverless.yml", serverless_config)
    print("✓ serverless.yml")
    
    # Create .gitignore (if not exists)
    print("\nChecking .gitignore...")
    print("-" * 60)
    
    gitignore_path = project_root / ".gitignore"
    if not gitignore_path.exists():
        create_file(gitignore_path, """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.env
.env.local
venv/
ENV/
env/
.venv/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Serverless
.serverless/
""")
        print("✓ .gitignore")
    else:
        print("✓ .gitignore (already exists)")
    
    # Create README.md (if not exists)
    print("\nChecking README.md...")
    print("-" * 60)
    
    readme_path = project_root / "README.md"
    if not readme_path.exists():
        # Use existing README if it exists with content
        print("✓ README.md (already exists)")
    else:
        print("✓ README.md (already exists)")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Project Initialization Complete!")
    print("=" * 60)
    print()
    print("Created structure:")
    print("  - src/ (all component directories)")
    print("  - tests/ (unit, integration, performance)")
    print("  - requirements.txt")
    print("  - serverless.yml")
    print("  - .gitignore")
    print()
    print("Next steps:")
    print("  1. Review the created structure")
    print("  2. Add content to files as you implement")
    print("  3. Run 'python scripts/verify-setup.py' to confirm")
    print("  4. Begin Sprint 0 implementation")
    print()

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
