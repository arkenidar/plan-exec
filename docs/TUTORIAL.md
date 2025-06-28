# Plan Language Tutorial

A step-by-step guide to learning the Plan Language.

## Getting Started

### Installation and Setup

1. Clone the repository: `git clone <repo-url>`
2. Navigate to directory: `cd plan-exec`
3. Run your first program: `python3 plan_executor.py example_plans/testing.plan`

### Your First Program

Create a file called `hello.plan`:

```plaintext
writeln "Hello, Plan Language!"
```

Run it:

```bash
python3 plan_executor.py hello.plan
```

## Lesson 1: Basic Output

### Simple Output

```plaintext
# Basic output
writeln "Hello, World!"
write "No newline"
writeln " - with newline"

# Numbers
writeln 42
writeln 3.14159

# Expressions
writeln 2 + 3 * 4
```

**Exercise 1.1:** Create a program that prints your name, age, and favorite number.

## Lesson 2: Functions

### Defining Functions

```plaintext
# Function with no arguments (like a variable)
def my_name#0
"Alice"

# Function with arguments
def greet#1
writeln "Hello, " + arg 1

# Use the functions
greet my_name
```

### Function Arguments

```plaintext
def add#2
arg 1 + arg 2

def multiply#3
arg 1 * arg 2 * arg 3

writeln add 5 3          # Output: 8
writeln multiply 2 3 4   # Output: 24
```

**Exercise 2.1:** Create functions for basic arithmetic operations (add, subtract, multiply, divide).

**Exercise 2.2:** Create a function that takes a name and age, and prints a greeting message.

## Lesson 3: Loops

### Basic Loops

```plaintext
# Count from 1 to 5
5 times {
    writeln times_count 1
}

# Loop with operations
10 times {
    writeln "Square of " + times_count 1 + " is " + (times_count 1 * times_count 1)
}
```

### Nested Loops

```plaintext
# Multiplication table
3 times {
    5 times {
        write (times_count 2 * times_count 1) + " "
    }
    writeln ""
}
```

**Exercise 3.1:** Create a program that prints the numbers 1-10, but only the odd ones.

**Exercise 3.2:** Create a 4x4 grid of asterisks using nested loops.

## Lesson 4: Conditionals

### If Statements

```plaintext
def check_number#1 {
    if arg 1 > 0 {
        writeln arg 1 + " is positive"
    }
    if arg 1 < 0 {
        writeln arg 1 + " is negative"
    }
    if arg 1 == 0 {
        writeln "Zero!"
    }
}

check_number 5
check_number -3
check_number 0
```

### If-Else

```plaintext
def even_or_odd#1 {
    if arg 1 % 2 == 0 {
        writeln arg 1 + " is even"
    } {
        writeln arg 1 + " is odd"
    }
}

even_or_odd 4
even_or_odd 7
```

**Exercise 4.1:** Create a function that determines if a number is positive, negative, or zero.

**Exercise 4.2:** Create a simple grading function (A, B, C, D, F based on numeric score).

## Lesson 5: Conditional Expressions (when)

### Basic When

```plaintext
def describe_number#1
"even" when arg 1 % 2 == 0 "odd"

writeln describe_number 4    # Output: even
writeln describe_number 7    # Output: odd
```

### Chained When (like switch)

```plaintext
def day_type#1
"weekend" when arg 1 == 1
"weekend" when arg 1 == 7
"weekday"

writeln day_type 1    # Output: weekend
writeln day_type 3    # Output: weekday
```

**Exercise 5.1:** Create a function using `when` that converts numbers 1-7 to day names.

**Exercise 5.2:** Rewrite the grading function from Exercise 4.2 using `when` expressions.

## Lesson 6: Advanced Functions

### Recursive Functions

```plaintext
def factorial#1 {
    if arg 1 <= 1 { return 1 }
    return arg 1 * factorial (arg 1 - 1)
}

writeln factorial 5    # Output: 120
```

### Functions Using Loops

```plaintext
def count_to#1 {
    arg 1 times {
        writeln "Count: " + times_count 1
    }
}

count_to 3
```

**Exercise 6.1:** Create a recursive function to calculate Fibonacci numbers.

**Exercise 6.2:** Create a function that prints a triangle pattern of a given height.

## Lesson 7: Control Flow

### Break and Continue

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

### Return from Functions

```plaintext
def find_first_divisible#2 {
    arg 1 times {
        if times_count 1 % arg 2 == 0 {
            return times_count 1
        }
    }
    return "not found"
}

writeln find_first_divisible 20 3    # Output: 3
```

**Exercise 7.1:** Create a function that finds the first even number in a range.

**Exercise 7.2:** Create a function that stops printing numbers when it reaches a multiple of 7.

## Lesson 8: Complex Examples

### FizzBuzz

```plaintext
def fizzbuzz#1 {
    if arg 1 % 15 == 0 { return "fizzbuzz" }
    if arg 1 % 3 == 0 { return "fizz" }
    if arg 1 % 5 == 0 { return "buzz" }
    return arg 1
}

20 times {
    writeln fizzbuzz times_count 1
}
```

### Prime Number Checker

```plaintext
def is_prime#1 {
    if arg 1 < 2 { return false }
    if arg 1 == 2 { return true }
    if arg 1 % 2 == 0 { return false }

    # Check odd divisors
    def i#0 { times_count 1 * 2 + 1 }
    (arg 1 / 2) times {
        if i * i > arg 1 { break }
        if arg 1 % i == 0 { return false }
    }
    return true
}

20 times {
    if is_prime times_count 1 {
        writeln times_count 1 + " is prime"
    }
}
```

**Exercise 8.1:** Create a program that prints the first 10 prime numbers.

**Exercise 8.2:** Create a simple calculator that can add, subtract, multiply, and divide.

## Lesson 9: Advanced Patterns

### Higher-Order Function Simulation

```plaintext
# Apply operation to range
def apply_to_range#3 {
    # arg 1 = start, arg 2 = end, arg 3 = operation
    (arg 2 - arg 1 + 1) times {
        def current#0 { arg 1 + times_count 1 - 1 }
        writeln "f(" + current + ") = " + (current * current)  # Example: square
    }
}

apply_to_range 1 5 "square"
```

### State Management

```plaintext
# Accumulator pattern
def sum_range#2 {
    def total#0 { 0 }
    (arg 2 - arg 1 + 1) times {
        def current#0 { arg 1 + times_count 1 - 1 }
        # Note: This is simplified - real implementation would need mutable state
        writeln "Adding " + current
    }
}
```

**Exercise 9.1:** Create a program that calculates the sum of squares from 1 to n.

**Exercise 9.2:** Create a program that finds the maximum number in a simulated array.

## Projects

### Project 1: Number Guessing Game Logic

Create the logic for a number guessing game:

- Generate a target number (use a fixed value)
- Create a function to check guesses (too high, too low, correct)
- Simulate a few guesses and show results

### Project 2: Text Analysis

Create functions to analyze text:

- Count characters in a string (simplified)
- Check if a string is a palindrome
- Convert between upper and lower case

### Project 3: Mathematical Library

Create a collection of mathematical functions:

- GCD (Greatest Common Divisor)
- LCM (Least Common Multiple)
- Power function with integer exponents
- Square root approximation

### Project 4: Pattern Generator

Create programs that generate various patterns:

- Pyramid patterns with stars
- Number triangles
- Checkerboard patterns

## Next Steps

1. **Explore the examples**: Study `example_plans/fizzbuzz.plan` and `example_plans/testing.plan`
2. **Read the documentation**: Check out the other documentation files
3. **Experiment**: Try combining different language features
4. **Build something**: Create your own programs using the Plan Language

## Common Mistakes

1. **Forgetting function arity**: Always specify the correct number after `#`
2. **Wrong argument indexing**: Arguments start at 1, not 0
3. **Missing return statements**: Functions without explicit returns may not behave as expected
4. **Loop counter confusion**: Remember `times_count 1` is innermost, higher numbers are outer loops
5. **Context misunderstanding**: `break`/`continue` affect loops, `return` affects functions

## Tips and Tricks

1. **Use meaningful function names**: `def calculate_area#2` is better than `def calc#2`
2. **Break complex logic into smaller functions**: Makes code more readable
3. **Use `when` for simple conditionals**: Often cleaner than if-else
4. **Test incrementally**: Start with simple cases and build up complexity
5. **Use debug output**: Add `writeln` statements to trace execution

## See Also

- [SYNTAX.md](SYNTAX.md) - Complete syntax reference
- [EXAMPLES.md](EXAMPLES.md) - More comprehensive examples
- [IMPLEMENTATION.md](IMPLEMENTATION.md) - How the language works internally
