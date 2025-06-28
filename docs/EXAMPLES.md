# Examples

This document provides comprehensive examples demonstrating all features of the Plan Language.

## Basic Examples

### Hello World
```plaintext
writeln "Hello, World!"
```

### Simple Arithmetic
```plaintext
writeln 2 + 3 * 4        # Output: 14
writeln (2 + 3) * 4      # Output: 20
writeln eval "2**10"     # Output: 1024
```

### Variables and Functions
```plaintext
# Define a simple variable-like function
def name#0
"Alice"

# Define a function with arguments
def greet#1
writeln "Hello, " + arg 1

# Use them
greet name               # Output: Hello, Alice
```

## Loop Examples

### Basic Loops
```plaintext
# Simple counting
5 times {
    writeln times_count 1
}
# Output: 1, 2, 3, 4, 5

# Loop with condition
10 times {
    if times_count 1 % 2 == 0 {
        writeln "Even: " + times_count 1
    }
}
# Output: Even: 2, Even: 4, Even: 6, Even: 8, Even: 10
```

### Nested Loops
```plaintext
# Multiplication table
3 times {
    5 times {
        writeln times_count 2 + " × " + times_count 1 + " = " + (times_count 2 * times_count 1)
    }
}
```

### Loop Control
```plaintext
# Break example
10 times {
    if times_count 1 == 6 { break }
    writeln times_count 1
}
# Output: 1, 2, 3, 4, 5

# Continue example  
10 times {
    if times_count 1 % 2 == 0 { continue }
    writeln times_count 1
}
# Output: 1, 3, 5, 7, 9
```

## Function Examples

### Mathematical Functions
```plaintext
# Factorial function
def factorial#1 {
    if arg 1 <= 1 { return 1 }
    return arg 1 * factorial (arg 1 - 1)
}

writeln factorial 5      # Output: 120
```

### Utility Functions
```plaintext
# Check if number is even
def is_even#1
arg 1 % 2 == 0

# Check if number is prime (simple version)
def is_prime#1 {
    if arg 1 < 2 { return false }
    if arg 1 == 2 { return true }
    if is_even arg 1 { return false }
    
    # Check odd divisors up to sqrt
    def i#0 { times_count 1 * 2 + 1 }
    (arg 1 / 2) times {
        if i > arg 1 / 2 { break }
        if arg 1 % i == 0 { return false }
    }
    return true
}

writeln is_prime 17      # Output: true
writeln is_prime 15      # Output: false
```

## Conditional Examples

### If-Else Chains
```plaintext
def grade_letter#1 {
    if arg 1 >= 90 { return "A" }
    if arg 1 >= 80 { return "B" }
    if arg 1 >= 70 { return "C" }
    if arg 1 >= 60 { return "D" }
    return "F"
}

writeln grade_letter 85  # Output: B
```

### When Expressions
```plaintext
def number_type#1
"positive" when arg 1 > 0
"negative" when arg 1 < 0  
"zero"

writeln number_type 5    # Output: positive
writeln number_type -3   # Output: negative
writeln number_type 0    # Output: zero
```

## FizzBuzz Implementation

### Complete FizzBuzz
```plaintext
# Define helper functions
def multiple#2
arg 1 % arg 2 == 0

def i#0
times_count 1

def multiple_of#1
multiple i arg 1

# Main FizzBuzz loop
20 times {
    print
    "fizz-buzz" when multiple_of 15
    "fizz" when multiple_of 3
    "buzz" when multiple_of 5
    i
}
```

### Alternative FizzBuzz
```plaintext
def fizzbuzz#1 {
    if arg 1 % 15 == 0 { return "fizz-buzz" }
    if arg 1 % 3 == 0 { return "fizz" }
    if arg 1 % 5 == 0 { return "buzz" }
    return arg 1
}

100 times {
    writeln fizzbuzz times_count 1
}
```

## Advanced Examples

### Matrix Processing
```plaintext
def print_matrix#2 {
    writeln "Matrix " + arg 1 + "×" + arg 2 + ":"
    
    arg 1 times {                    # rows
        write "["
        arg 2 times {                # columns
            write (times_count 2 * times_count 1)
            if times_count 1 < arg 2 { write ", " }
        }
        writeln "]"
    }
}

print_matrix 3 4
```

### Recursive Functions
```plaintext
# Fibonacci sequence
def fibonacci#1 {
    if arg 1 <= 1 { return arg 1 }
    return fibonacci (arg 1 - 1) + fibonacci (arg 1 - 2)
}

# Print first 10 Fibonacci numbers
10 times {
    writeln "fib(" + times_count 1 + ") = " + fibonacci times_count 1
}
```

### Pattern Generation
```plaintext
# Generate triangle pattern
def triangle#1 {
    arg 1 times {
        times_count 1 times { write "*" }
        writeln ""
    }
}

triangle 5
# Output:
# *
# **
# ***
# ****
# *****
```

### Text Processing
```plaintext
# Count vowels in a string (simplified)
def count_vowels#1 {
    def vowels#0 "aeiouAEIOU"
    def count#0 0
    
    # This is a simplified example - actual implementation
    # would need string iteration capabilities
    writeln "Counting vowels in: " + arg 1
    return count
}
```

## Interactive Examples

### Simple Calculator
```plaintext
def add#2 { return arg 1 + arg 2 }
def subtract#2 { return arg 1 - arg 2 }
def multiply#2 { return arg 1 * arg 2 }
def divide#2 { 
    if arg 2 == 0 { return "Error: Division by zero" }
    return arg 1 / arg 2 
}

writeln "Calculator Demo:"
writeln "10 + 5 = " + add 10 5
writeln "10 - 5 = " + subtract 10 5
writeln "10 × 5 = " + multiply 10 5
writeln "10 ÷ 5 = " + divide 10 5
```

### Game Logic
```plaintext
# Simple number guessing game logic
def check_guess#2 {
    if arg 1 == arg 2 { return "Correct!" }
    if arg 1 < arg 2 { return "Too low" }
    return "Too high"
}

def target#0 { 42 }

# Simulate some guesses
writeln check_guess 30 target    # Output: Too low
writeln check_guess 50 target    # Output: Too high  
writeln check_guess 42 target    # Output: Correct!
```

## Error Handling Examples

### Input Validation
```plaintext
def safe_divide#2 {
    if arg 2 == 0 {
        writeln "Error: Cannot divide by zero"
        return "undefined"
    }
    return arg 1 / arg 2
}

def validate_positive#1 {
    if arg 1 <= 0 {
        writeln "Error: Expected positive number, got " + arg 1
        return false
    }
    return true
}
```

### Boundary Checking
```plaintext
def safe_array_access#2 {
    # arg 1 = array size, arg 2 = index
    if arg 2 < 1 {
        writeln "Error: Index too small (minimum 1)"
        return "error"
    }
    if arg 2 > arg 1 {
        writeln "Error: Index too large (maximum " + arg 1 + ")"
        return "error"
    }
    return "valid"
}
```

## Performance Examples

### Optimized Algorithms
```plaintext
# Fast exponentiation
def power#2 {
    if arg 2 == 0 { return 1 }
    if arg 2 == 1 { return arg 1 }
    
    if arg 2 % 2 == 0 {
        def half#0 { power arg 1 (arg 2 / 2) }
        return half * half
    } {
        return arg 1 * power arg 1 (arg 2 - 1)
    }
}

writeln power 2 10       # Output: 1024
```

### Loop Optimization
```plaintext
# Early termination in search
def find_first_even#1 {
    arg 1 times {
        if times_count 1 % 2 == 0 {
            writeln "Found first even: " + times_count 1
            return times_count 1
        }
    }
    return "No even numbers found"
}
```

## Integration Examples

### Using External Evaluation
```plaintext
# Mathematical calculations
writeln eval "import math; math.sqrt(16)"    # Python version
writeln eval "Math.sqrt(16)"                 # JavaScript version

# Array/List operations
writeln eval "[1,2,3,4,5].length"           # JavaScript
writeln eval "len([1,2,3,4,5])"              # Python
```

### Buffer Operations (JavaScript version)
```plaintext
# Building formatted output
buffer_write "Result: "
buffer_write eval "2 + 3"
buffer_write " (calculated)"
buffer_flush
writeln ""
```

## See Also

- [SYNTAX.md](SYNTAX.md) - Complete syntax reference
- [CONTROL_FLOW.md](CONTROL_FLOW.md) - Control flow details
- [CONTEXTS.md](CONTEXTS.md) - Context system explanation
