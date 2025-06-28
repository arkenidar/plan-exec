# Control Flow

The Plan Language provides powerful context-aware control flow mechanisms that respect the different execution contexts (functions, loops, blocks).

## Break Statement

### Basic Break
```plaintext
times 10 {
    if times_count 1 == 5 { break }    # Exit current loop
    writeln times_count 1
}
# Output: 1, 2, 3, 4
```

### Multi-level Break
```plaintext
times 3 {                    # Outer loop (level 2)
    times 5 {                # Inner loop (level 1)
        if times_count 1 == 3 and times_count 2 == 2 {
            break 2          # Break out of both loops
        }
        if times_count 1 == 2 {
            break 1          # Break out of inner loop only (same as 'break')
        }
        writeln times_count 1 + " " + times_count 2
    }
}
```

### Break Levels
- `break` or `break 1` - Break current (innermost) loop
- `break 2` - Break current loop and one outer loop
- `break N` - Break N levels of nested loops

## Continue Statement

### Basic Continue
```plaintext
times 10 {
    if times_count 1 % 2 == 0 { continue }    # Skip even numbers
    writeln times_count 1
}
# Output: 1, 3, 5, 7, 9
```

### Multi-level Continue
```plaintext
times 3 {                    # Outer loop
    times 5 {                # Inner loop
        if times_count 1 == 3 {
            continue 2       # Continue outer loop (skip rest of outer iteration)
        }
        if times_count 1 == 2 {
            continue 1       # Continue inner loop (same as 'continue')
        }
        writeln times_count 1 + " " + times_count 2
    }
}
```

## Return Statement

### Function Return
```plaintext
def factorial#1 {
    if arg 1 == 0 { return 1 }
    if arg 1 < 0 { return "error" }
    return arg 1 * factorial (arg 1 - 1)
}
```

### Return from Nested Contexts
```plaintext
def complex_function#2 {
    times arg 1 {                    # Loop context
        if times_count 1 % 2 == 0 {  # Block context
            times 3 {                # Nested loop context
                if times_count 1 == 2 and arg 2 < 0 {
                    return "early_exit"    # Returns from function, not loops
                }
                writeln times_count 1
            }
        }
    }
    return "completed"
}
```

**Key Points:**
- `return` always exits the innermost function, regardless of nested loops/blocks
- All intermediate contexts (loops, blocks) are properly unwound
- Return value is passed back to the function caller

## If-Else Statements

### Basic If
```plaintext
if condition {
    # Execute if condition is true
    writeln "Condition is true"
}
```

### If-Else
```plaintext
if condition {
    writeln "True branch"
} {
    writeln "False branch"
}
```

### Nested If-Else
```plaintext
if x > 0 {
    if x > 10 {
        writeln "Greater than 10"
    } {
        writeln "Between 1 and 10"
    }
} {
    writeln "Zero or negative"
}
```

### If with Control Flow
```plaintext
def check_value#1 {
    if arg 1 < 0 { return "negative" }
    if arg 1 == 0 { return "zero" }
    return "positive"
}

times 10 {
    if times_count 1 % 3 == 0 { continue }
    if times_count 1 > 7 { break }
    writeln times_count 1
}
```

## Conditional Expressions (when)

### Basic When
```plaintext
result = "even" when x % 2 == 0
writeln result    # Prints "even" if x is even, otherwise prints nothing
```

### When with Else
```plaintext
result = "even" when x % 2 == 0 "odd"
writeln result    # Prints "even" or "odd"
```

### Chained When (like switch)
```plaintext
print
"fizz-buzz" when multiple_of 15
"fizz" when multiple_of 3  
"buzz" when multiple_of 5
i
```

**How chained when works:**
1. Evaluates first `when`: if true, returns "fizz-buzz"
2. If false, evaluates second `when`: if true, returns "fizz"
3. If false, evaluates third `when`: if true, returns "buzz"
4. If all false, returns `i`

## Context-Aware Control Flow Rules

### Break/Continue Scope
- Only affects loop contexts
- Skips over function and block contexts
- Counts loop nesting levels from innermost outward

### Return Scope  
- Only affects function contexts
- Skips over all loop and block contexts
- Always targets the innermost function

### Context Unwinding
When control flow statements execute:

1. **Break/Continue**: 
   - Marks target loop contexts for exit/restart
   - Preserves function contexts
   - Cleans up intermediate block contexts

2. **Return**:
   - Marks target function context for return
   - Marks all inner contexts (loops, blocks) for cleanup
   - Unwinds entire call stack to function boundary

## Error Handling

### Invalid Control Flow
```plaintext
# ERROR: break outside of loop
def invalid_function#0 {
    break    # Error: no loop context to break from
}

# ERROR: return outside of function  
break      # Error: no function context to return from (if at global scope)
```

### Context Validation
The evaluator validates that control flow statements are used in appropriate contexts:
- `break`/`continue` require active loop context
- `return` requires active function context
- Level numbers must not exceed available context depth

## Advanced Control Flow

### Combining Control Statements
```plaintext
def process_matrix#2 {
    times arg 1 {                # rows
        times arg 2 {            # columns
            if times_count 1 == 1 and times_count 2 == 1 {
                continue 2       # Skip first row entirely
            }
            if times_count 1 > 5 {
                return "matrix too large"
            }
            if times_count 2 % 2 == 0 {
                continue 1       # Skip even columns
            }
            writeln times_count 2 + "," + times_count 1
        }
    }
    return "matrix processed"
}
```

### Early Return Patterns
```plaintext
def validate_and_process#1 {
    if arg 1 < 0 { return "error: negative input" }
    if arg 1 == 0 { return "error: zero input" }
    if arg 1 > 100 { return "error: input too large" }
    
    # Main processing logic
    times arg 1 {
        if times_count 1 % 10 == 0 {
            writeln "Processing: " + times_count 1
        }
    }
    return "success"
}
```

## See Also

- [CONTEXTS.md](CONTEXTS.md) - Understanding execution contexts
- [SYNTAX.md](SYNTAX.md) - Complete syntax reference  
- [EXAMPLES.md](EXAMPLES.md) - Practical control flow examples
