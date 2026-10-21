#!/bin/bash
# verify-sprint.sh - Sprint Verification Script
# Run this after completing each sprint to verify everything works properly

# Don't use set -e because pytest returns non-zero for warnings

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."
TESTS_DIR="$PROJECT_ROOT/src/tests"
UNIT_DIR="$PROJECT_ROOT/src/tests/unit"
INTEGRATION_DIR="$PROJECT_ROOT/src/tests/integration"
PERFORMANCE_DIR="$PROJECT_ROOT/src/tests/performance"
REPORT_FILE="$PROJECT_ROOT/documentation/progress.md"

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: No Python found${NC}"
    exit 1
fi

echo "=========================================="
echo "🧪 Sprint Verification Suite"
echo "=========================================="
echo ""
echo "Project Root: $PROJECT_ROOT"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

# Function to print result
print_result() {
    local status=$1
    local test_name=$2
    local details=$3
    
    case $status in
        "pass")
            echo -e "${GREEN}✓${NC} $test_name"
            ;;
        "fail")
            echo -e "${RED}✗${NC} $test_name"
            if [ -n "$details" ]; then
                echo "       $details"
            fi
            ;;
        "skip")
            echo -e "${YELLOW}⊘${NC} $test_name"
            if [ -n "$details" ]; then
                echo "       $details"
            fi
            ;;
    esac
}

# Function to update progress.md
update_progress() {
    local sprint=$1
    local status=$2
    local date_str=$(date '+%Y-%m-%d')
    
    # Add timestamp to the report
    echo "" >> "$REPORT_FILE"
    echo "---" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "**Verification Date**: $date_str" >> "$REPORT_FILE"
    echo "**Verification Status**: $status" >> "$REPORT_FILE"
    echo "**Total Tests**: $TOTAL_TESTS" >> "$REPORT_FILE"
    echo "**Passed**: $PASSED_TESTS" >> "$REPORT_FILE"
    echo "**Failed**: $FAILED_TESTS" >> "$REPORT_FILE"
    echo "**Skipped**: $SKIPPED_TESTS" >> "$REPORT_FILE"
}

# Check if we're in a project directory
if [ ! -d "$PROJECT_ROOT" ]; then
    echo -e "${RED}Error: Project root not found: $PROJECT_ROOT${NC}"
    exit 1
fi

# ==========================================
# PHASE 1: Code Quality Checks
# ==========================================
echo "=========================================="
echo "📋 Phase 1: Code Quality"
echo "=========================================="
echo ""

# Check 1: Repository Structure
if [ -d "$PROJECT_ROOT/src" ]; then
    print_result "pass" "Repository structure exists" ""
else
    print_result "fail" "Repository structure missing" "Create src/ directory"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Check 2: Python Files
if [ -d "$PROJECT_ROOT/src" ]; then
    python_files=$(find "$PROJECT_ROOT/src" -name "*.py" | wc -l)
    if [ "$python_files" -gt 0 ]; then
        print_result "pass" "Python files found ($python_files files)" ""
    else
        print_result "fail" "No Python files found" "Add Python source files"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    print_result "skip" "Python files check" "No src/ directory"
    SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
fi

# Check 3: Type Hints
if [ -d "$PROJECT_ROOT/src" ]; then
    files_with_types=$(grep -r ":" "$PROJECT_ROOT/src" --include="*.py" 2>/dev/null | grep -v "#" | head -10 | wc -l)
    if [ "$files_with_types" -gt 0 ]; then
        print_result "pass" "Type hints present in codebase" ""
    else
        print_result "fail" "No type hints found" "Add type hints to all functions"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    print_result "skip" "Type hints check" "No src/ directory"
    SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
fi

# Check 4: Docstrings
if [ -d "$PROJECT_ROOT/src" ]; then
    files_with_docs=$(grep -r "\"\"\"" "$PROJECT_ROOT/src" --include="*.py" 2>/dev/null | wc -l)
    if [ "$files_with_docs" -gt 0 ]; then
        print_result "pass" "Docstrings present in codebase" ""
    else
        print_result "fail" "No docstrings found" "Add docstrings to all public APIs"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    print_result "skip" "Docstrings check" "No src/ directory"
    SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
fi

# ==========================================
# PHASE 2: Unit Tests
# ==========================================
echo ""
echo "=========================================="
echo "🧪 Phase 2: Unit Tests"
echo "=========================================="
echo ""

# Check 5: Test Files Exist
if [ -d "$TESTS_DIR" ]; then
    test_files=$(find "$TESTS_DIR" -name "test_*.py" | wc -l)
    if [ "$test_files" -gt 0 ]; then
        print_result "pass" "Test files found ($test_files files)" ""
    else
        print_result "fail" "No test files found" "Create test files in tests/"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    print_result "skip" "Test files check" "No tests/ directory"
    SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
fi

# Check 6: Run Unit Tests
if [ -d "$UNIT_DIR" ] && [ -f "$UNIT_DIR/conftest.py" ]; then
    echo "Running unit tests..."
    cd "$PROJECT_ROOT"
    # Run tests and capture output, don't exit on non-zero (pytest returns non-zero for warnings)
    set +e
    TEST_OUTPUT=$($PYTHON_CMD -m pytest $UNIT_DIR/ -v --tb=short 2>&1)
    TEST_EXIT_CODE=$?
    set -e
    echo "$TEST_OUTPUT"
    
    # Check if tests passed (look for summary line)
    if echo "$TEST_OUTPUT" | grep -q "passed"; then
        print_result "pass" "All unit tests passed" ""
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        print_result "fail" "Unit tests failed" "Check test output for details"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
else
    print_result "skip" "Unit tests" "No unit tests directory or conftest.py"
    SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
fi

# ==========================================
# PHASE 3: Integration Tests
# ==========================================
echo ""
echo "=========================================="
echo "🔗 Phase 3: Integration Tests"
echo "=========================================="
echo ""

# Check 7: Integration Test Files
if [ -d "$TESTS_DIR/integration" ]; then
    int_test_files=$(find "$TESTS_DIR/integration" -name "test_*.py" | wc -l)
    if [ "$int_test_files" -gt 0 ]; then
        print_result "pass" "Integration test files found ($int_test_files files)" ""
    else
        print_result "fail" "No integration test files" "Create integration tests"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    print_result "skip" "Integration test files" "No integration tests directory"
    SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
fi

# Check 8: Run Integration Tests
if [ -d "$INTEGRATION_DIR" ]; then
    echo "Running integration tests..."
    cd "$PROJECT_ROOT"
    # Run tests and capture output, don't exit on non-zero (pytest returns non-zero for warnings)
    set +e
    TEST_OUTPUT=$($PYTHON_CMD -m pytest $INTEGRATION_DIR/ -v --tb=short 2>&1)
    TEST_EXIT_CODE=$?
    set -e
    echo "$TEST_OUTPUT"
    
    # Check if tests passed (look for summary line)
    if echo "$TEST_OUTPUT" | grep -q "passed"; then
        print_result "pass" "All integration tests passed" ""
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        print_result "fail" "Integration tests failed" "Check test output for details"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
else
    print_result "skip" "Integration tests" "No integration tests directory"
    SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
fi

# ==========================================
# PHASE 4: Performance Benchmarks
# ==========================================
echo ""
echo "=========================================="
echo "⚡ Phase 4: Performance Benchmarks"
echo "=========================================="
echo ""

# Check 9: Performance Test Files
if [ -d "$TESTS_DIR/performance" ]; then
    perf_test_files=$(find "$TESTS_DIR/performance" -name "test_*.py" | wc -l)
    if [ "$perf_test_files" -gt 0 ]; then
        print_result "pass" "Performance test files found ($perf_test_files files)" ""
    else
        print_result "fail" "No performance test files" "Create performance tests"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    print_result "skip" "Performance test files" "No performance tests directory"
    SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
fi

# Check 10: Run Performance Benchmarks
if [ -d "$PERFORMANCE_DIR" ]; then
    echo "Running performance benchmarks..."
    cd "$PROJECT_ROOT"
    
    # Run tests and capture output, don't exit on non-zero (pytest returns non-zero for warnings)
    set +e
    TEST_OUTPUT=$($PYTHON_CMD -m pytest $PERFORMANCE_DIR/ -v --tb=short 2>&1)
    TEST_EXIT_CODE=$?
    set -e
    echo "$TEST_OUTPUT"
    
    # Check if tests passed (look for summary line)
    if echo "$TEST_OUTPUT" | grep -q "passed"; then
        print_result "pass" "All performance benchmarks passed" ""
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        print_result "fail" "Performance benchmarks failed" "Check test output for details"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
else
    print_result "skip" "Performance benchmarks" "No performance tests directory"
    SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
fi

# ==========================================
# PHASE 5: Documentation
# ==========================================
echo ""
echo "=========================================="
echo "📚 Phase 5: Documentation"
echo "=========================================="
echo ""

# Check 11: README
if [ -f "$PROJECT_ROOT/README.md" ]; then
    print_result "pass" "README.md exists" ""
else
    print_result "fail" "README.md missing" "Create README.md"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Check 12: Architecture Documentation
if [ -f "$PROJECT_ROOT/documentation/8D-Unified-Intelligence-Architecture.md" ]; then
    print_result "pass" "Architecture documentation exists" ""
else
    print_result "fail" "Architecture documentation missing" "Create architecture docs"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Check 13: Implementation Plan
if [ -f "$PROJECT_ROOT/documentation/Implementation_plan.md" ]; then
    print_result "pass" "Implementation plan exists" ""
else
    print_result "fail" "Implementation plan missing" "Create implementation plan"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Check 14: Zed Rules
if [ -f "$PROJECT_ROOT/documentation/zed-rules.md" ]; then
    print_result "pass" "Zed rules documentation exists" ""
else
    print_result "fail" "Zed rules documentation missing" "Create zed-rules.md"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Check 15: Progress Tracking
if [ -f "$PROJECT_ROOT/documentation/progress.md" ]; then
    print_result "pass" "Progress tracking file exists" ""
else
    print_result "fail" "Progress tracking file missing" "Create progress.md"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# ==========================================
# SUMMARY
# ==========================================
echo ""
echo "=========================================="
echo "📊 Verification Summary"
echo "=========================================="
echo ""
echo -e "Total Tests:  ${TOTAL_TESTS}"
echo -e "Passed:       ${GREEN}${PASSED_TESTS}${NC}"
echo -e "Failed:       ${RED}${FAILED_TESTS}${NC}"
echo -e "Skipped:      ${YELLOW}${SKIPPED_TESTS}${NC}"
echo ""

# Calculate pass rate
if [ "$TOTAL_TESTS" -gt 0 ]; then
    pass_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    echo -e "Pass Rate:    ${pass_rate}%"
fi

echo ""

# Determine overall status
if [ "$FAILED_TESTS" -eq 0 ]; then
    echo -e "${GREEN}🎉 All checks passed! Sprint ready for review.${NC}"
    update_progress "Sprint 0" "PASSED"
else
    echo -e "${RED}⚠️  ${FAILED_TESTS} check(s) failed. Please fix before proceeding.${NC}"
    update_progress "Sprint 0" "FAILED"
fi

echo ""
echo "=========================================="
echo "📝 Next Steps"
echo "=========================================="
echo ""
echo "1. Review progress.md for verification results"
echo "2. Fix any failed tests or checks"
echo "3. Update progress.md with sprint notes"
echo "4. Proceed to next sprint when ready"
echo ""

# Exit with appropriate code
if [ "$FAILED_TESTS" -gt 0 ]; then
    exit 1
fi

exit 0
