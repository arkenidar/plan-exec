# Plan Execution Language

**🎉 v0.2.0 - Core Features Complete!**

A domain-specific language (DSL) for plan execution with working functions, loops, conditionals, and boolean operations.

## Overview

The Plan Execution Language is inspired by [pangea-js](https://github.com/arkenidar/pangea-js) and provides a simple yet powerful syntax for computational plans. **All core features are now working and tested.**

## ✅ Working Features (Test Suite: 10/10 Pass)

- **✅ Functions**: `def add#2` with `arg 1 + arg 2` - fully working
- **✅ Boolean literals**: `true`, `false` - working
- **✅ Conditionals**: `if true { ... }` and `if-else` - working  
- **✅ Operators**: `+`, `-`, `*`, `/`, `%`, `==`, `!=`, `<`, `>` - working
- **✅ Loops**: `N times { ... }` with `times_count` - working
- **✅ Output**: `writeln`, `write` - working

## Quick Start

```bash
# Test the language with examples
python3 plan_executor.py example_plans/testing.plan

# Run the comprehensive test suite
python3 test_current_features.py

# Test function calls
echo 'def add#2
arg 1 + arg 2  
writeln add 5 3' > test.plan && python3 plan_executor.py test.plan
# Output: 8
```

## Example Code

```plaintext
# Function definition and call
def add#2
arg 1 + arg 2
writeln add 5 3        # Output: 8

# Boolean conditionals  
if true { writeln "Yes" }                    # Output: Yes
if false { writeln "No" } { writeln "Else" } # Output: Else

# Loop with counter
3 times { writeln times_count }  # Output: 1

# Complex function with boolean logic
def multiple#2
arg 1 % arg 2 == 0
writeln multiple 6 2    # Output: True
```

## File Structure

```
plan-exec/
├── plan_executor.py           # Main executor
├── plan_words_parsing.py      # Tokenizer/parser
├── plan_words_evaluation.py   # Evaluator/interpreter
├── example_plans/             # Example plan files
├── js_version/               # JavaScript implementation
└── docs/                     # Documentation
```

## Documentation

### For Users

- 📚 [Tutorial](docs/TUTORIAL.md) - Step-by-step learning guide
- ⚡ [Quick Reference](docs/QUICK_REFERENCE.md) - Concise syntax reference
- 📖 [Language Syntax](docs/SYNTAX.md) - Complete syntax reference
- 💡 [Examples](docs/EXAMPLES.md) - Comprehensive examples and projects

### For Developers

- 🏗️ [Context System](docs/CONTEXTS.md) - Function, loop, and block contexts
- 🔄 [Control Flow](docs/CONTROL_FLOW.md) - Break, continue, return mechanics
- ⚙️ [Implementation](docs/IMPLEMENTATION.md) - Technical architecture details

## Example

```plaintext
# FizzBuzz implementation
def multiple#2
arg 1 % arg 2 == 0

def i#0
times_count 1

def multiple_of#1
multiple i arg 1

20 times {
    print
    "fizz-buzz" when multiple_of 15
    "fizz" when multiple_of 3
    "buzz" when multiple_of 5
    i
}
```

## License

MIT License - see LICENSE file for details.
