# Mutation Testing Tool

A Python-based mutation testing tool that helps evaluate the effectiveness of test suites by systematically introducing faults (mutations) into the code and checking if the test suite can detect them.

## Project Structure

```
.
├── calculator.py          # Source code to be mutation tested
├── test_calculator.py     # Test suite for the calculator
└── mutator.py            # Mutation testing tool
```

## Features

- Generates various types of mutations:
  - Arithmetic operators: +, -, *, /, //, %, **
  - Comparison operators: ==, !=, <, >, <=, >=
- Tests each mutation against the existing test suite
- Generates detailed mutation testing reports
- Calculates mutation coverage percentage
- Saves comprehensive test results to JSON files

## Calculator Module

The `calculator.py` implements a Calculator class with the following operations:
- Addition (`add`)
- Subtraction (`subtract`)
- Multiplication (`multiply`)
- Division (`divide`)
- Power (`power`)
- Modulo (`mod`)
- Floor Division (`floor_divide`)
- Absolute Value (`abs`)
- Maximum (`max`)
- Minimum (`min`)

## Test Suite

The `test_calculator.py` contains unit tests for each calculator operation using Python's unittest framework. Current mutation coverage: 42.8%

## Usage

1. Run the mutation testing tool:
```bash
python mutator.py calculator.py test_calculator.py
```

2. The tool will:
   - Generate mutations for the calculator code
   - Run the test suite against each mutation
   - Display results in the console
   - Save a detailed report to a JSON file

## Output

The tool generates:
- Console output showing each mutation and whether it was caught
- A JSON report file with detailed results
- Mutation coverage percentage

## Requirements

- Python 3.x
- Standard library modules:
  - ast
  - importlib
  - os
  - sys
  - unittest
  - json
  - datetime

## Mutation Testing Report Format

The generated JSON report includes:
- Timestamp
- Duration of testing
- Source and test files used
- Total number of mutations
- Number of caught/not caught mutations
- Mutation coverage percentage
- Detailed results for each mutation

## Current Status

- Total mutations tested: 14
- Mutations caught: 6
- Mutations not caught: 8
- Mutation coverage: 42.8%

## Future Improvements

Potential enhancements:
- Add more mutation operators
- Improve test coverage
- Add support for more complex code structures
- Implement parallel mutation testing
- Add visualization of mutation coverage 