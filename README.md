# Plan Executor & Pangea Python Interpreter

**🚀 v1.0.0 - Production Ready Implementation**

This repository contains implementations of programming language interpreters, including a Plan Language executor and a complete Python implementation of the Pangea programming language from [pangea-js](https://github.com/arkenidar/pangea-js).

## Overview

The project consists of two main components:

1. **Plan Language Executor** - A domain-specific language for structured execution
2. **Pangea Python Interpreter** - A comprehensive Python translation of the Pangea JavaScript interpreter

Both implementations are **production-ready** with comprehensive test suites, documentation, and real-world example programs.

## Main Features

### Plan Language
- Function definitions with explicit arity
- Control flow constructs (if, times, when, unless)
- Infix, prefix, and postfix operators
- Basic data types and operations
- Loop constructs with counters

### Pangea Python Interpreter (NEW!)
- Complete Python implementation of pangea-js
- Function definitions with arity (`def funcname#arity`)
- Advanced operators (infix, postfix, prefix)
- Control flow (if, times, each, when)
- Data structures (arrays, objects)
- String handling with special formatting
- Recursive functions
- Stack-based execution model
- Interactive REPL mode

## Quick Start

### Plan Language
```bash
# Run a plan file
python3 plan_executor.py example_plans/fizzbuzz.plan

# Test current features
python3 test_current_features.py
```

### Pangea Python Interpreter
```bash
# Interactive mode
python3 pangea_cli.py

# Run a pangea file
python3 pangea_cli.py sample.pangea

# Execute code directly
python3 pangea_cli.py -c 'print "Hello World"'
```

## Example Code

### Basic Pangea Examples
```pangea
# Basic arithmetic
print 2 + 3 * 4
print 5 squared

# Function definition
def greet#1 print "Hello," print arg 1
greet "World"

# Loops with counter
5 times print "Hello"
3 times ( print "Count:" print times_count 1 )

# Conditionals and when operator
print "positive" when 5 > 0
if true print "yes" print "no"

# Recursive factorial
def factorial#1
if ( arg 1 ) == 0
    1
    ( arg 1 ) * factorial ( arg 1 ) - 1
print factorial 5
```

### FizzBuzz Implementation
```pangea
def multiple#2
0 == ( ( arg 1 ) % ( arg 2 ) )

def i#0
times_count 1

def multiple_of#1
multiple i arg 1

20 times (
    print
    "fizz-buzz" when multiple_of 15
    "fizz" when multiple_of 3
    "buzz" when multiple_of 5
    i
)
```

### Plan Language Examples
```plan
# Function definition and call
def add#2
arg 1 + arg 2
writeln add 5 3        # Output: 8

# Boolean conditionals
if true { writeln "Yes" }                    # Output: Yes
if false { writeln "No" } { writeln "Else" } # Output: Else

# Loop with counter
3 times { writeln times_count }  # Output: 1, 2, 3

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

## Key Files

### Core Implementation
- `pangea_python_interpreter.py` - Main Pangea interpreter implementation
- `pangea_cli.py` - Command-line interface and REPL
- `plan_words_evaluation.py` - Plan language evaluator
- `plan_words_parsing.py` - Plan language parser

### Testing
- `test_pangea_interpreter.py` - Comprehensive Pangea test suite
- `test_user_files.py` - Test with real user-authored programs
- Various specialized test files for specific features

### Examples
- `sample.pangea` - Example Pangea programs
- `example_plans/` - Directory with Plan language examples
- `fizzbuzz.plan` - Classic FizzBuzz implementation

### Documentation
- `README_PANGEA.md` - Detailed Pangea language documentation
- `DEVELOPMENT.md` - Development notes and architecture
- `CONTRIBUTING.md` - Contributing guidelines

## Testing

### Run All Tests
```bash
# Test Pangea interpreter
python3 test_pangea_interpreter.py

# Test with user files
python3 test_user_files.py

# Interactive testing
python3 pangea_cli.py
```

### Test Specific Features
```bash
# Test arithmetic
python3 pangea_cli.py -c 'print 2 + 3 * 4'

# Test functions
python3 pangea_cli.py -c 'def double#1 ( arg 1 ) * 2; print double 21'

# Test FizzBuzz
python3 pangea_cli.py example_plans/fizzbuzz.plan
```

## Architecture

The Pangea interpreter follows the same architectural patterns as the original JavaScript implementation:

### Core Components
- **Word-based parsing** - Code is tokenized into words
- **Phrase length calculation** - Determines expression boundaries
- **Stack-based execution** - Function calls use a call stack
- **Namespace management** - Built-ins and user-defined functions
- **Operator precedence** - Proper handling of infix/postfix operators

### Key Features
- **skipOperator mechanism** - Prevents infinite recursion in operator parsing
- **Unified namespace** - Functions and operators in single namespace
- **Index-based parameters** - Parameters passed as word indices
- **Lazy evaluation** - Expressions evaluated only when needed

## Compatibility

This Python implementation is designed to be fully compatible with pangea-js programs. Most pangea-js code should run unchanged in this interpreter.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

This project maintains compatibility with the original pangea-js project licensing.

## Related Projects

- [pangea-js](https://github.com/arkenidar/pangea-js) - Original JavaScript implementation

## Status

✅ **Production Ready** - The interpreter is stable and suitable for real-world use.

Both the Plan Language executor and Pangea Python interpreter are feature-complete with comprehensive test coverage.
