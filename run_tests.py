"""
Test Execution Launcher Script
Runs the Pytest suite and outputs test execution metrics and code coverage.
"""
import sys
import pytest


def main():
    print("=" * 60)
    print(" Executing E-Commerce Checkout Test Suite & Coverage Analysis")
    print("=" * 60)

    args = [
        "-v",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html:reports/coverage_html"
    ]

    exit_code = pytest.main(args)

    print("\n" + "=" * 60)
    if exit_code == 0:
        print(" SUCCESS: All tests passed with target code coverage!")
    else:
        print(f" FAILURE: Test suite exited with code {exit_code}")
    print("=" * 60)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
