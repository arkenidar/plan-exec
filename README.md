# Plan Execution Language

A domain-specific language (DSL) for plan execution with support for functions, loops, conditionals, and context-aware control flow.

## Overview

The Plan Execution Language is inspired by [pangea-js](https://github.com/arkenidar/pangea-js) and provides a simple yet powerful syntax for defining and executing computational plans.

## Quick Start

```bash
python3 plan_executor.py example_plans/testing.plan
python3 plan_executor.py example_plans/fizzbuzz.plan
```

## Language Features

- **Functions**: Define reusable code blocks with arguments
- **Loops**: Iterate with nested loop counter access
- **Conditionals**: If-else statements and conditional expressions
- **Context Management**: Function arguments, loop counters, and block scoping
- **Control Flow**: Break, continue, and return with context awareness

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
