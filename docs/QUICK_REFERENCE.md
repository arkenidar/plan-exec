# Quick Reference

A concise reference for the Plan Language syntax and features.

## Syntax Overview

| Category | Syntax | Example |
|----------|--------|---------|
| **Comments** | `# comment` | `# This is a comment` |
| **Output** | `writeln "text"` | `writeln "Hello World"` |
| | `write "text"` | `write "No newline"` |
| | `print "text"` | `print "Same as writeln"` |
| **Functions** | `def name#arity` | `def add#2` |
| | `arg N` | `arg 1 + arg 2` |
| **Loops** | `N times { body }` | `5 times { writeln "hi" }` |
| | `times_count N` | `times_count 1` |
| **Conditionals** | `if cond { body }` | `if x > 0 { writeln "positive" }` |
| | `if cond { true } { false }` | `if x % 2 == 0 { "even" } { "odd" }` |
| | `value when cond` | `"even" when x % 2 == 0` |
| | `val when cond else_val` | `"even" when x % 2 == 0 "odd"` |
| **Control Flow** | `break` | `break` (exit current loop) |
| | `break N` | `break 2` (exit N loop levels) |
| | `continue` | `continue` (next iteration) |
| | `return value` | `return 42` (exit function) |
| **Evaluation** | `eval "expr"` | `eval "2**10"` |

## Operators

### Arithmetic
```plaintext
+     # Addition        5 + 3 → 8
-     # Subtraction     5 - 3 → 2  
*     # Multiplication  5 * 3 → 15
/     # Division        6 / 3 → 2
%     # Modulus         7 % 3 → 1
**    # Exponentiation  2 ** 3 → 8
```

### Comparison
```plaintext
==    # Equal           5 == 5 → true
!=    # Not equal       5 != 3 → true
>     # Greater than    5 > 3 → true  
<     # Less than       3 < 5 → true
>=    # Greater/equal   5 >= 5 → true
<=    # Less/equal      3 <= 5 → true
```

### Logical
```plaintext
and   # Logical AND     true and false → false
or    # Logical OR      true or false → true  
not   # Logical NOT     not true → false
```

## Common Patterns

### Function Definition
```plaintext
def function_name#argument_count
function_body

# Examples:
def square#1               # One argument
arg 1 * arg 1

def greet#2               # Two arguments  
writeln "Hello " + arg 1 + ", age " + arg 2

def pi#0                  # No arguments (constant)
3.14159
```

### Loop Patterns
```plaintext
# Simple counting
N times { writeln times_count 1 }

# Nested loops  
3 times {
    5 times {
        writeln times_count 2 + "," + times_count 1
    }
}

# Loop with conditions
10 times {
    if times_count 1 % 2 == 0 { continue }
    writeln times_count 1
}
```

### Conditional Patterns
```plaintext
# Simple if
if condition { action }

# If-else
if condition { true_action } { false_action }

# Multiple conditions
if x > 10 { "large" }
if x > 5 { "medium" }
"small"

# When expressions
"positive" when x > 0
"negative" when x < 0  
"zero"
```

### Recursive Functions
```plaintext
def factorial#1 {
    if arg 1 <= 1 { return 1 }
    return arg 1 * factorial (arg 1 - 1)
}

def fibonacci#1 {
    if arg 1 <= 1 { return arg 1 }
    return fibonacci (arg 1 - 1) + fibonacci (arg 1 - 2)
}
```

## Context Rules

| Context Type | Access Method | Scope Rules |
|--------------|---------------|-------------|
| **Function Arguments** | `arg N` | Only within same function |
| **Loop Counters** | `times_count N` | N=1 is innermost, N=2 outer, etc. |
| **Global Functions** | `function_name` | Available everywhere after definition |

### Context Nesting
```plaintext
def outer_func#1 {           # Function context
    times arg 1 {            # Loop context  
        if times_count 1 > 5 { # Block context
            return "done"    # Returns from outer_func
        }
        if times_count 1 % 2 == 0 {
            continue         # Continues times loop
        }
    }
}
```

## Control Flow Rules

| Statement | Scope | Effect |
|-----------|-------|--------|
| `break` | Current loop | Exit loop |
| `break N` | N loop levels | Exit N nested loops |
| `continue` | Current loop | Next iteration |
| `continue N` | N levels up | Continue Nth outer loop |
| `return value` | Current function | Exit function with value |

## Built-in Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `writeln` | Output with newline | `writeln "hello"` |
| `write` | Output without newline | `write "hello"` |
| `print` | Same as writeln | `print "hello"` |
| `eval` | Evaluate expression | `eval "2+3"` |
| `times_count` | Get loop counter | `times_count 1` |
| `arg` | Get function argument | `arg 1` |

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Unknown word: X" | Undefined function/variable | Define function or check spelling |
| "condition must be boolean" | Non-boolean in if statement | Use comparison operators |
| "times_count value must be integer" | Non-integer loop count | Use integer expression |
| "No loop context" | break/continue outside loop | Use only within loops |
| "No function context" | return outside function | Use only within functions |

## Examples

### Hello World
```plaintext
writeln "Hello, World!"
```

### Simple Calculator
```plaintext
def add#2 { return arg 1 + arg 2 }
def sub#2 { return arg 1 - arg 2 }
def mul#2 { return arg 1 * arg 2 }
def div#2 { return arg 1 / arg 2 }

writeln add 10 5    # Output: 15
writeln mul 3 4     # Output: 12
```

### FizzBuzz (Compact)
```plaintext
def fb#1
"fizzbuzz" when arg 1 % 15 == 0
"fizz" when arg 1 % 3 == 0
"buzz" when arg 1 % 5 == 0
arg 1

20 times { writeln fb times_count 1 }
```

### Factorial
```plaintext
def fact#1 {
    if arg 1 <= 1 { return 1 }
    return arg 1 * fact (arg 1 - 1)
}

writeln fact 5    # Output: 120
```

### Counting Even Numbers
```plaintext
10 times {
    if times_count 1 % 2 != 0 { continue }
    writeln "Even: " + times_count 1
}
```

### Nested Loop Pattern
```plaintext
5 times {
    times_count 1 times {
        write "*"
    }
    writeln ""
}
# Output: Triangle pattern
```

## File Structure

```
plan-exec/
├── plan_executor.py           # Run with: python3 plan_executor.py file.plan
├── plan_words_parsing.py      # Tokenizer
├── plan_words_evaluation.py   # Interpreter  
├── example_plans/
│   ├── fizzbuzz.plan          # FizzBuzz example
│   └── testing.plan           # Feature demonstration
└── docs/                      # Documentation
```

## Running Programs

```bash
# Run a plan file
python3 plan_executor.py example_plans/testing.plan

# Run specific plan
python3 plan_executor.py my_program.plan

# Default runs testing.plan if no file specified
python3 plan_executor.py
```

## Tips

1. **Function arity must match calls**: `def add#2` needs exactly 2 arguments
2. **Arguments are 1-indexed**: Use `arg 1`, `arg 2`, not `arg 0`
3. **Loop counters are 1-indexed**: `times_count 1` starts at 1, not 0
4. **Blocks return last value**: `{ writeln "hi"; 42 }` returns 42
5. **Use parentheses for complex expressions**: `(a + b) * c`
6. **Comments start with #**: Everything after `#` is ignored
7. **Strings use double quotes**: `"hello world"`
8. **Functions must be defined before use**: Define at top of file

## See Also

- [TUTORIAL.md](TUTORIAL.md) - Step-by-step learning guide
- [SYNTAX.md](SYNTAX.md) - Complete syntax reference  
- [EXAMPLES.md](EXAMPLES.md) - Comprehensive examples
- [CONTEXTS.md](CONTEXTS.md) - Context system details
- [CONTROL_FLOW.md](CONTROL_FLOW.md) - Control flow mechanics
