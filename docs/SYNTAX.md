# Plan Language Syntax Reference

## Basic Syntax

### Comments

```plaintext
# This is a comment
writeln "Hello"  # Inline comment
```

### Literals

```plaintext
123          # Integer
45.5         # Float
"hello"      # String
true         # Boolean
false        # Boolean
```

## Output Operations

### Write Operations

```plaintext
write "text"        # Write without newline
writeln "text"      # Write with newline
print "text"        # Print (equivalent to writeln)
```

### Buffer Operations (JS version)

```plaintext
buffer_write "text"   # Write to buffer
buffer_flush          # Flush buffer to output
```

## Function Definitions

### Function Syntax

```plaintext
def function_name#arity
function_body

# Examples:
def add#2               # Function with 2 arguments
arg 1 + arg 2

def greet#1             # Function with 1 argument
writeln "Hello " + arg 1

def counter#0           # Function with 0 arguments (like a variable)
times_count 1
```

### Function Arguments

```plaintext
arg 1    # First argument (1-indexed)
arg 2    # Second argument
arg N    # Nth argument
```

### Function Calls

```plaintext
add 5 3              # Call add function with arguments 5 and 3
greet "World"        # Call greet function with "World"
counter              # Call counter function (no arguments)
```

## Loops

### Times Loop

```plaintext
N times { body }     # Execute body N times
N times body         # Single statement body

# Examples:
5 times { writeln "Hello" }
3 times writeln times_count 1
```

### Loop Counter Access

```plaintext
times_count 1        # Current (innermost) loop counter
times_count 2        # One level outer loop counter
times_count N        # N levels outer loop counter

# Example with nested loops:
3 times {
    5 times {
        writeln times_count 1    # Prints 1,2,3,4,5 for each outer iteration
        writeln times_count 2    # Prints 1,1,1,1,1 then 2,2,2,2,2 then 3,3,3,3,3
    }
}
```

## Conditionals

### If Statements

```plaintext
if condition { body }
if condition { true_body } { false_body }    # if-else

# Examples:
if x > 5 { writeln "Greater than 5" }
if x % 2 == 0 { writeln "Even" } { writeln "Odd" }
```

### Conditional Expressions (when)

```plaintext
value when condition               # Returns value if condition is true
value when condition else_value    # Returns value if true, else_value if false

# Examples:
"even" when x % 2 == 0
"positive" when x > 0 "negative"
```

## Operators

### Arithmetic

```plaintext
+    # Addition
-    # Subtraction
*    # Multiplication
/    # Division
%    # Modulus
**   # Exponentiation
```

### Comparison

```plaintext
==   # Equal
!=   # Not equal
>    # Greater than
<    # Less than
>=   # Greater than or equal
<=   # Less than or equal
```

### Logical

```plaintext
and  # Logical AND
or   # Logical OR
not  # Logical NOT
```

## Expression Evaluation

### Eval Statement

```plaintext
eval "expression"    # Evaluate Python/JavaScript expression

# Examples:
eval "2**10"         # Returns 1024
eval "[1, 2, 3, 4]"  # Returns array/list
```

## Blocks and Scoping

### Block Syntax

```plaintext
{
    statement1
    statement2
    statement3
}
```

### Block Return Value

The last evaluated expression in a block becomes the block's return value.

## Control Flow

See [CONTROL_FLOW.md](CONTROL_FLOW.md) for detailed control flow documentation.

## Examples

See [EXAMPLES.md](EXAMPLES.md) for comprehensive examples of all language features.
