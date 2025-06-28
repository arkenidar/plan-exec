# Implementation Guide

This document explains the technical implementation details of the Plan Language interpreter.

## Architecture Overview

```
┌─────────────────────┐
│   plan_executor.py  │ ← Entry point, file handling
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│plan_words_parsing.py│ ← Tokenization and parsing
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│plan_words_evaluation│ ← Evaluation and execution
│        .py          │
└─────────────────────┘
```

## Core Components

### 1. Parser (`plan_words_parsing.py`)

**Responsibilities:**
- Tokenize plan text into word arrays
- Handle comments and string literals
- Preserve function definition syntax (`name#arity`)

**Key Functions:**
- `words_parse(plan_text)` - Main parsing function
- Comment handling with `#` symbol
- String literal preservation
- Whitespace normalization

### 2. Evaluator (`plan_words_evaluation.py`)

**Responsibilities:**
- Execute parsed plan words
- Manage execution contexts
- Handle control flow
- Implement built-in operations

**Key Functions:**
- `evaluate_plan(plan_words)` - Main evaluation loop
- `evaluate_word(plan_words, current_i)` - Single word evaluation
- `evaluate_block(plan_words, start_i)` - Block evaluation
- `skip_block(plan_words, start_i)` - Block skipping for control flow

## Context Management System

### Context Stack Structure
```python
context_stack = [
    {
        "type": "global",
        "functions": {},        # Global function definitions
        "variables": {}         # Global variables
    },
    {
        "type": "function",
        "name": "function_name",
        "args": [arg1, arg2],   # Function arguments
        "should_return": False,
        "return_value": None
    },
    {
        "type": "loop", 
        "counter": 1,           # Current iteration (1-indexed)
        "max_iterations": 10,
        "should_break": False,
        "should_continue": False,
        "break_levels": 0       # For multi-level breaks
    },
    {
        "type": "block",
        "variables": {},        # Block-local variables
        "should_exit": False
    }
]
```

### Context Operations

#### Push Context
```python
def push_context(context_type, **kwargs):
    new_context = {"type": context_type, **kwargs}
    context_stack.append(new_context)
    return new_context
```

#### Pop Context  
```python
def pop_context(expected_type=None):
    if expected_type and context_stack[-1]["type"] != expected_type:
        raise RuntimeError(f"Expected {expected_type}, got {context_stack[-1]['type']}")
    return context_stack.pop()
```

#### Find Context
```python
def find_context(context_type, depth=1):
    count = 0
    for context in reversed(context_stack):
        if context["type"] == context_type:
            count += 1
            if count == depth:
                return context
    return None
```

## Function System Implementation

### Function Definition Storage
```python
# Global function registry
functions = {}

def register_function(name, arity, body_start_index):
    functions[name] = {
        "arity": arity,
        "body_start": body_start_index,
        "body_words": None  # Computed later
    }
```

### Function Call Mechanism
```python
def call_function(name, args):
    func_def = functions[name]
    
    # Push function context
    push_context("function", 
                name=name, 
                args=args,
                should_return=False,
                return_value=None)
    
    try:
        # Execute function body
        result = evaluate_block(func_def["body_words"], 0)
        
        # Check for early return
        context = find_context("function")
        if context["should_return"]:
            result = context["return_value"]
            
    finally:
        # Pop function context
        pop_context("function")
    
    return result
```

## Loop System Implementation

### Times Loop Structure
```python
def execute_times_loop(count, body_start_index):
    # Push loop context
    push_context("loop",
                counter=0,
                max_iterations=count,
                should_break=False,
                should_continue=False)
    
    try:
        for i in range(1, count + 1):
            # Update counter
            context = find_context("loop")
            context["counter"] = i
            
            # Execute loop body
            evaluate_block(plan_words, body_start_index)
            
            # Check control flow
            if context["should_break"]:
                break
            if context["should_continue"]:
                context["should_continue"] = False
                continue
                
    finally:
        # Pop loop context
        pop_context("loop")
```

### Loop Counter Access
```python
def get_times_count(depth):
    context = find_context("loop", depth)
    if not context:
        raise RuntimeError(f"No loop context at depth {depth}")
    return context["counter"]
```

## Control Flow Implementation

### Break Statement
```python
def execute_break(levels=1):
    # Mark loop contexts for breaking
    marked = 0
    for context in reversed(context_stack):
        if context["type"] == "loop":
            context["should_break"] = True
            marked += 1
            if marked >= levels:
                break
    
    if marked < levels:
        raise RuntimeError(f"Cannot break {levels} levels, only {marked} loops available")
```

### Continue Statement
```python
def execute_continue(levels=1):
    # Mark innermost loop for continue
    context = find_context("loop", levels)
    if not context:
        raise RuntimeError(f"No loop context at depth {levels}")
    context["should_continue"] = True
```

### Return Statement
```python
def execute_return(value):
    # Find innermost function context
    func_context = find_context("function")
    if not func_context:
        raise RuntimeError("Return statement outside of function")
    
    # Mark function for return
    func_context["should_return"] = True
    func_context["return_value"] = value
    
    # Mark all inner contexts for cleanup
    for context in reversed(context_stack):
        if context == func_context:
            break
        if context["type"] == "loop":
            context["should_break"] = True
        elif context["type"] == "block":
            context["should_exit"] = True
```

## Built-in Operations

### Word Evaluation Framework
```python
def evaluate_word(plan_words, current_i):
    word = plan_words[current_i]
    
    # Check built-in operations
    if word in built_in_operations:
        return built_in_operations[word](plan_words, current_i)
    
    # Check function calls
    if word in functions:
        return call_function(word, get_function_args(plan_words, current_i))
    
    # Try to evaluate as literal
    try:
        return eval(word), current_i + 1
    except:
        raise RuntimeError(f"Unknown word: {word}")
```

### Built-in Operation Registry
```python
built_in_operations = {
    "writeln": handle_writeln,
    "write": handle_write,
    "times": handle_times,
    "if": handle_if,
    "def": handle_def,
    "arg": handle_arg,
    "times_count": handle_times_count,
    "break": handle_break,
    "continue": handle_continue,
    "return": handle_return,
    "when": handle_when,
    "eval": handle_eval
}
```

## Error Handling

### Error Types
```python
class PlanRuntimeError(Exception):
    def __init__(self, message, word_index=None):
        self.message = message
        self.word_index = word_index
        super().__init__(f"Runtime error at word {word_index}: {message}")

class PlanSyntaxError(Exception):
    def __init__(self, message, word_index=None):
        self.message = message
        self.word_index = word_index
        super().__init__(f"Syntax error at word {word_index}: {message}")
```

### Error Recovery
- Context cleanup on errors
- Stack unwinding for exceptions
- Meaningful error messages with word positions

## Performance Considerations

### Optimization Strategies
1. **Function Caching**: Cache parsed function bodies
2. **Context Pooling**: Reuse context objects
3. **Word Indexing**: Efficient word position tracking
4. **Lazy Evaluation**: Only evaluate needed expressions

### Memory Management
- Automatic context cleanup
- Garbage collection of unused functions
- Limit recursion depth to prevent stack overflow

## Testing Framework

### Unit Test Structure
```python
def test_function_definition():
    plan = "def add#2 arg 1 + arg 2"
    result = execute_plan(plan)
    assert "add" in functions
    assert functions["add"]["arity"] == 2

def test_loop_execution():
    plan = "3 times writeln times_count 1"
    output = capture_output(execute_plan(plan))
    assert output == ["1", "2", "3"]
```

### Integration Tests
- Complete program execution
- Cross-feature interaction testing
- Performance benchmarking
- Error condition validation

## Extending the Language

### Adding New Built-ins
1. Implement handler function
2. Register in `built_in_operations`
3. Add documentation
4. Write tests

### Adding New Control Structures
1. Extend context system if needed
2. Implement parsing logic
3. Add evaluation handlers
4. Update control flow mechanisms

## See Also

- [SYNTAX.md](SYNTAX.md) - Language syntax
- [CONTEXTS.md](CONTEXTS.md) - Context system details
- [CONTROL_FLOW.md](CONTROL_FLOW.md) - Control flow mechanics
- [EXAMPLES.md](EXAMPLES.md) - Usage examples
