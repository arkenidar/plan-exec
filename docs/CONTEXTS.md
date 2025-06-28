# Context System

The Plan Language uses a sophisticated context system to manage function arguments, loop counters, and block scoping.

## Context Types

### 1. Function Context
Manages function arguments and local function state.

```plaintext
def factorial#1 {
    # Function context contains:
    # - arg 1 (function argument)
    # - local function scope
    
    if arg 1 == 0 { return 1 }
    return arg 1 * factorial (arg 1 - 1)
}
```

**Features:**
- Function arguments accessible via `arg N`
- Function call stack management
- Return value handling
- Local variable scope

### 2. Loop Context
Manages loop iteration counters and loop-specific state.

```plaintext
times 5 {
    # Loop context contains:
    # - Current iteration counter
    # - Loop control flags (break, continue)
    
    writeln times_count 1    # Access current loop counter
}
```

**Features:**
- Iteration counters via `times_count N`
- Nested loop counter stack
- Break/continue control flags
- Loop-specific variables

### 3. Block Context
Manages general block scoping and local variables.

```plaintext
{
    # Block context contains:
    # - Local block scope
    # - Block control flags
    
    writeln "Inside block"
}
```

**Features:**
- Block-local variable scope
- Block exit control
- Nested block management

## Context Stack

The evaluator maintains a context stack where each context type can have multiple instances:

```
Context Stack (top to bottom):
┌─────────────────────┐
│ Block Context       │ ← Current block
├─────────────────────┤
│ Loop Context        │ ← Current loop (times_count 1)
├─────────────────────┤
│ Function Context    │ ← Current function (arg 1, arg 2...)
├─────────────────────┤
│ Loop Context        │ ← Outer loop (times_count 2)
├─────────────────────┤
│ Function Context    │ ← Outer function
├─────────────────────┤
│ Global Context      │ ← Global scope
└─────────────────────┘
```

## Context Access Patterns

### Function Arguments
```plaintext
def example#3 {
    writeln arg 1    # First argument
    writeln arg 2    # Second argument  
    writeln arg 3    # Third argument
}

example "hello" 42 true
```

### Loop Counters
```plaintext
times 3 {              # Outer loop (times_count 2)
    times 5 {          # Inner loop (times_count 1)
        writeln times_count 1    # Inner counter: 1,2,3,4,5
        writeln times_count 2    # Outer counter: 1,1,1,1,1 then 2,2,2,2,2...
    }
}
```

### Cross-Context Access
```plaintext
def loop_function#1 {
    times arg 1 {
        # Function context: arg 1
        # Loop context: times_count 1
        
        if times_count 1 > arg 1 / 2 {
            writeln "Past halfway point"
        }
    }
}

loop_function 10
```

## Context Lifetime

### Function Context Lifetime
1. **Created**: When function is called
2. **Active**: During function execution
3. **Destroyed**: When function returns or exits

### Loop Context Lifetime
1. **Created**: When loop begins execution
2. **Active**: During each loop iteration
3. **Destroyed**: When loop completes or breaks

### Block Context Lifetime
1. **Created**: When entering block `{`
2. **Active**: During block execution
3. **Destroyed**: When exiting block `}`

## Context Isolation

### Function Isolation
```plaintext
def outer#1 {
    def inner#1 {
        # inner can access its own arg 1
        # inner cannot access outer's arg 1 directly
        writeln arg 1
    }
    
    inner "inner_arg"
}

outer "outer_arg"
```

### Loop Isolation
```plaintext
times 3 {
    times 5 {
        # Inner loop has its own counter space
        # Outer loop counter is still accessible
        writeln times_count 1    # Inner: 1-5
        writeln times_count 2    # Outer: 1-3
    }
}
```

## Context Implementation

### Context Stack Management
```python
context_stack = [
    {
        "type": "global",
        "variables": {},
        "functions": {}
    },
    {
        "type": "function", 
        "args": [arg1, arg2, ...],
        "should_return": False,
        "return_value": None
    },
    {
        "type": "loop",
        "counter": 1,
        "max_count": 10,
        "should_break": False,
        "should_continue": False
    },
    {
        "type": "block",
        "variables": {},
        "should_exit": False
    }
]
```

### Context Lookup Algorithm
1. Search current context for identifier
2. If not found, search parent contexts
3. Continue until identifier found or global context reached
4. Respect context type boundaries (functions can't see outer function args)

## Advanced Context Features

### Context Switching
The evaluator automatically switches between contexts based on the current execution point.

### Context Inheritance
Child contexts can access parent context data according to scoping rules.

### Context Cleanup
Contexts are automatically cleaned up when their scope ends, preventing memory leaks.

## See Also

- [CONTROL_FLOW.md](CONTROL_FLOW.md) - How contexts interact with control flow
- [SYNTAX.md](SYNTAX.md) - Language syntax using contexts
- [EXAMPLES.md](EXAMPLES.md) - Practical context usage examples
