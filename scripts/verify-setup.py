#!/usr/bin/env python3
"""
Simple Verification Script for 8D Unified Intelligence Architecture
Checks documentation and setup before starting sprints
"""

import os
import sys

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to project root
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DOCS_DIR = os.path.join(PROJECT_ROOT, 'documentation')

def check_file(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    return exists

def main():
    print("\n" + "=" * 60)
    print("🔍 Project Setup Verification")
    print("=" * 60)
    print()
    print(f"Project Root: {PROJECT_ROOT}")
    print()
    
    checks = [
        ("README.md", "README.md"),
        ("documentation/8D-Unified-Intelligence-Architecture.md", "Architecture Documentation"),
        ("documentation/Implementation_plan.md", "Implementation Plan"),
        ("documentation/zed-rules.md", "Zed Rules"),
        ("documentation/progress.md", "Progress Tracking"),
        ("scripts/verify-sprint.sh", "Verification Script"),
        ("scripts/cost_analysis.py", "Cost Analysis Script"),
        ("scripts/generate_progress.py", "Progress Generator"),
    ]
    
    results = []
    for filepath, description in checks:
        result = check_file(os.path.join(PROJECT_ROOT, filepath), description)
        results.append((description, result))
    
    print()
    print("=" * 60)
    print("📊 Verification Summary")
    print("=" * 60)
    print()
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"Total Checks: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print()
    
    if passed == total:
        print("✅ All checks passed! Project setup is complete.")
        print()
        print("Ready to proceed with Sprint 0:")
        print("  - Foundation & Infrastructure")
        print()
        print("Next Steps:")
        print("  1. Create src/ directory structure")
        print("  2. Set up development environment")
        print("  3. Configure AWS Lambda deployment")
        print("  4. Initialize vector database")
        return 0
    else:
        print("⚠️  Some checks failed. Please address before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
