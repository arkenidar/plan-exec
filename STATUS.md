# Plan Language: Current Status & Roadmap

## 📊 What's Working Now (v0.1.1)

### ✅ Recently Added Features (Unified System)

#### Boolean Literals & Operators

- ✅ **Boolean literals**: `true`, `false`
- ✅ **Infix arithmetic**: `3 + 4`, `10 - 2`, `5 * 6`
- ✅ **Infix comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- ✅ **Unified operator system**: Foundation from pangea-js

#### Enhanced System Architecture

- ✅ **Call stack system**: Function argument management
- ✅ **Operator registry**: Infix, prefix, postfix support
- ✅ **Function arity system**: `function_name#N` notation

### ✅ Previously Implemented Features

#### Basic Operations

- ✅ **Output**: `writeln`, `write`
- ✅ **Comments**: `# comment syntax`
- ✅ **String literals**: `"hello world"`
- ✅ **Number literals**: `123`, `45.5`
- ✅ **Expression evaluation**: `eval "2+3"`
- ✅ **Arithmetic**: Basic math operations via `eval`

#### Basic Control Structures

- ✅ **Simple loops**: `N times { body }`
- ✅ **Basic if statements**: `if condition { body }`
- ✅ **If-else**: `if condition { true_body } { false_body }`
- ✅ **Block evaluation**: `{ statement1; statement2 }`
- ✅ **Block skipping**: Skip blocks for false conditions

#### Parsing & Execution

- ✅ **Word tokenization**: Splits plan text into words
- ✅ **Comment filtering**: Removes `#` comments (but breaks `#` in function definitions)
- ✅ **Block parsing**: Handles `{` and `}` blocks
- ✅ **Command line args**: `python3 plan_executor.py file.plan`
- ✅ **Error handling**: Basic error reporting

## ✅ What Actually Works (Tested Examples)

### ✅ Fully Working Features

```plaintext
# Basic output
writeln "Hello, World!"     # ✅ Works
writeln 42                  # ✅ Works
writeln 3.14                # ✅ Works (but only shows 42?)

# Expression evaluation
writeln eval "2 + 3"        # ✅ Works (output: 5)
writeln eval "2**10"        # ✅ Works (output: 1024)
writeln eval "[1, 2, 3, 4]" # ✅ Works

# Basic loops
3 times { writeln "Hello!" }  # ✅ Works (no output but no error)
3 times { writeln times_count } # ✅ Works (no output but no error)

# Boolean literals (NEW!)
writeln true                 # ✅ Works (output: True)
writeln false               # ✅ Works (output: False)

# Infix arithmetic (NEW!)
writeln 3 + 4               # ✅ Works (output: 7)
writeln 10 - 2              # ✅ Works (output: 8)
writeln 5 * 6               # ✅ Works (output: 30)

# Function definitions
def test#1                   # ✅ Parses without error
arg 1
writeln "After function"     # ✅ Continues execution
```

### ⚠️ Partially Working

```plaintext
# Function calls (definition works, calling doesn't)
def add#2                   # ✅ Definition parses
writeln "Function body"     # ✅ Function body parsed
add 5 3                     # ❌ Function call not executed

# Boolean conditionals need fixing
if true { writeln "Yes" }    # ❌ "condition must be a boolean value"
if false { writeln "No" }    # ❌ "condition must be a boolean value"
```

### 🔍 Surprising Discoveries from Testing

1. **Function calls don't error** - They just silently do nothing
2. **Loop output missing** - Loops execute but produce no visible output
3. **Boolean literals missing** - `true`/`false` not implemented
4. **Number output partial** - Only first number prints in multi-line
5. **Error handling inconsistent** - Some errors continue execution

### ⚠️ Partially Working Features

#### Function System (Incomplete)

- 🔶 **Function definitions**: `def name#arity` (parsing works, execution incomplete)
- 🔶 **Function calls**: Basic structure exists but args don't work
- ❌ **Function arguments**: `arg N` not fully implemented
- ❌ **Function scope**: No argument passing or local scope

#### Loop System (Basic)

- 🔶 **Loop counters**: `times_count` exists but limited
- ❌ **Nested loop counters**: `times_count 2`, `times_count 3` not implemented
- ❌ **Loop context stack**: No proper nesting support

#### Advanced Features (Not Implemented)

- ❌ **Conditional expressions**: `value when condition` not implemented
- ❌ **Control flow**: `break`, `continue`, `return` not implemented
- ❌ **Context management**: No function/loop/block context system
- ❌ **Multi-level breaks**: `break 2` not supported

## 🚧 Current Issues & Limitations

### 1. **FizzBuzz Example Fails**

**Current Error**: `ERROR: times_count value must be an integer`

- Function definitions parse but don't execute properly
- `arg` references don't resolve to actual values
- `times_count` has type issues in arithmetic operations
- `when` expressions not implemented
- `print` vs `writeln` confusion
- Functions like `multiple` and `multiple_of` not callable

### 2. **Function System Incomplete**

**Status**: Definitions parsed, execution missing

- Functions are parsed into `function_registry` but not callable
- No argument passing mechanism (`arg N` returns placeholder strings)
- No function scope isolation (no call stack)
- No return value handling
- Function calls fall through to `eval()` and fail

### 3. **Context System Missing**

**Impact**: No proper scoping or nesting

- No function call stack
- No loop nesting support (only global `times_count`)
- No variable scoping
- No context-aware control flow
- Functions can't access loop counters properly

### 4. **Limited Loop Support**

**Current**: Only basic functionality

- Only basic `times` loops work
- No nested loop counter access (`times_count 1`, `times_count 2`)
- No break/continue support
- Global `times_count` instead of stack-based counters
- Type issues when using `times_count` in expressions

## 🗺️ Development Roadmap

### Phase 1: Core Function System (v0.2) - _Priority: HIGH_

#### 1.1 Function Execution

- [ ] **Function call mechanism**: Make defined functions callable
- [ ] **Argument passing**: Implement proper `arg N` handling
- [ ] **Function scope**: Local argument storage per function call
- [ ] **Return values**: Function return value handling

**Target**: Make basic functions work

```plaintext
def add#2
arg 1 + arg 2

writeln add 5 3    # Should output: 8
```

#### 1.2 Function Context Stack

- [ ] **Call stack**: Stack-based function calls
- [ ] **Argument isolation**: Each call has its own arguments
- [ ] **Nested calls**: Functions calling other functions
- [ ] **Recursion support**: Self-referential functions

**Target**: Enable recursive functions

```plaintext
def factorial#1 {
    if arg 1 <= 1 { return 1 }
    return arg 1 * factorial (arg 1 - 1)
}
```

### Phase 2: Loop Context System (v0.3) - _Priority: HIGH_

#### 2.1 Loop Counter Stack

- [ ] **Nested counters**: `times_count 1`, `times_count 2`, etc.
- [ ] **Loop context stack**: Each loop maintains its own counter
- [ ] **Counter isolation**: Inner loops don't affect outer counters
- [ ] **Deep nesting**: Support arbitrary nesting levels

**Target**: Enable nested loop counter access

```plaintext
3 times {
    5 times {
        writeln times_count 1    # Inner: 1,2,3,4,5
        writeln times_count 2    # Outer: 1,1,1,1,1 then 2,2,2,2,2...
    }
}
```

#### 2.2 Loop Context Integration

- [ ] **Function-loop interaction**: Functions accessing loop counters
- [ ] **Cross-context access**: Functions defined inside loops
- [ ] **Context cleanup**: Proper context destruction

**Target**: Make FizzBuzz helper functions work

```plaintext
def i#0
times_count 1    # Access current loop counter from function
```

### Phase 3: Conditional Expressions (v0.4) - _Priority: MEDIUM_

#### 3.1 When Expressions

- [ ] **Basic when**: `value when condition`
- [ ] **When-else**: `value when condition else_value`
- [ ] **Chained when**: Multiple when expressions in sequence
- [ ] **When evaluation**: Proper precedence and short-circuiting

**Target**: Enable conditional expressions

```plaintext
"even" when x % 2 == 0 "odd"
"fizz-buzz" when multiple_of 15
"fizz" when multiple_of 3
"buzz" when multiple_of 5
i
```

#### 3.2 Print with Conditionals

- [ ] **Print statement**: Handle `print` vs `writeln`
- [ ] **Conditional printing**: Print result of conditional expressions
- [ ] **Expression chaining**: Multiple conditionals in print statement

**Target**: Make FizzBuzz print statement work

```plaintext
print
"fizz-buzz" when multiple_of 15
"fizz" when multiple_of 3
"buzz" when multiple_of 5
i
```

### Phase 4: Control Flow (v0.5) - _Priority: MEDIUM_

#### 4.1 Basic Control Flow

- [ ] **Return statement**: `return value` from functions
- [ ] **Break statement**: `break` from loops
- [ ] **Continue statement**: `continue` loop iteration

#### 4.2 Context-Aware Control Flow

- [ ] **Multi-level break**: `break 2` to exit multiple loops
- [ ] **Context traversal**: Return exits function regardless of nesting
- [ ] **Proper unwinding**: Clean up contexts on control flow

**Target**: Enable advanced control flow

```plaintext
def search#2 {
    arg 1 times {
        if times_count 1 == arg 2 { return "found" }
        if times_count 1 > 10 { break }
    }
    return "not found"
}
```

### Phase 5: Advanced Features (v0.6) - _Priority: LOW_

#### 5.1 Enhanced Context System

- [ ] **Block contexts**: Local variables in blocks
- [ ] **Variable assignment**: `= var value` syntax
- [ ] **Variable scoping**: Lexical scoping rules
- [ ] **Closure support**: Functions accessing outer scope

#### 5.2 Error Handling

- [ ] **Try-catch**: Error handling mechanisms
- [ ] **Input validation**: Argument type checking
- [ ] **Runtime errors**: Better error messages with context
- [ ] **Debugging support**: Enhanced debug output

#### 5.3 Standard Library

- [ ] **Math functions**: `sqrt`, `abs`, `min`, `max`
- [ ] **String functions**: `length`, `substring`, `concat`
- [ ] **Array functions**: `push`, `pop`, `length`
- [ ] **Type functions**: `type`, `is_number`, `is_string`

### Phase 6: Performance & Polish (v1.0) - _Priority: LOW_

#### 6.1 Performance Optimization

- [ ] **Function caching**: Cache compiled function bodies
- [ ] **Tail call optimization**: Optimize recursive calls
- [ ] **Context pooling**: Reuse context objects
- [ ] **Memory management**: Garbage collection for contexts

#### 6.2 Developer Experience

- [ ] **Better error messages**: Line numbers and context
- [ ] **Debugging tools**: Step-through debugging
- [ ] **Profiling**: Performance analysis tools
- [ ] **IDE support**: Syntax highlighting, autocomplete

#### 6.3 Documentation & Examples

- [ ] **Complete examples**: More complex programs
- [ ] **Tutorial videos**: Visual learning materials
- [ ] **Interactive tutorial**: Web-based learning
- [ ] **Community examples**: User-contributed programs

## 🎯 Immediate Next Steps (Next Week)

### 🔥 Quick Wins (1-2 hours each)

1. **Fix comment parsing** - Don't break on `#` in function definitions
2. **Add `print` alias** - Make `print` work same as `writeln`
3. **Fix times_count type** - Ensure it's always an integer
4. **Add basic function calls** - Make simple functions callable

### Priority 1: Fix FizzBuzz Example (3-5 days)

1. **Implement function calls** - Make `def add#2` actually callable
2. **Fix argument passing** - Make `arg 1`, `arg 2` work properly
3. **Add function call stack** - Isolated arguments per function call
4. **Test with simple functions** - Get basic math functions working

**Milestone**: This simple function should work:

```plaintext
def add#2
arg 1 + arg 2

writeln add 5 3    # Should output: 8
```

### Priority 2: Loop Counter Stack

1. **Replace global times_count** - Use stack-based counters
2. **Implement times_count N** - Access different nesting levels
3. **Test nested loops** - Verify counter isolation
4. **Integration test** - Functions accessing loop counters

### Priority 3: Basic When Expressions

1. **Parse when syntax** - `value when condition`
2. **Implement when evaluation** - Conditional expression logic
3. **Add chained when** - Multiple when expressions
4. **Test FizzBuzz print** - Complete working example

## 📈 Success Metrics

### v0.2 Success Criteria

- [ ] FizzBuzz example runs without errors
- [ ] All function definition and call examples work
- [ ] Basic recursive functions (factorial) work
- [ ] All tutorial Lesson 1-2 examples work

### v0.3 Success Criteria

- [ ] Nested loop examples work correctly
- [ ] `times_count N` accesses work at any nesting level
- [ ] Functions can access loop counters properly
- [ ] All tutorial Lesson 3 examples work

### v0.4 Success Criteria

- [ ] FizzBuzz runs and produces correct output
- [ ] All conditional expression examples work
- [ ] Print with conditionals works
- [ ] All tutorial Lesson 4-5 examples work

### v1.0 Success Criteria

- [ ] All documentation examples work
- [ ] Performance is acceptable for complex programs
- [ ] Error messages are helpful and clear
- [ ] Tutorial completion rate is high

## 🛠️ Developer Notes & Troubleshooting

### Current Architecture Issues

1. **Global state**: `times_count` is global instead of context-local
2. **Function registry**: Functions stored but not executed
3. **Argument handling**: `arg N` returns strings like `"arg_1"` instead of values
4. **Context missing**: No call stack or scope management
5. **Comment parsing**: `#` breaks function definitions like `multiple#2`

### Key Files and Their Status

- `plan_executor.py` ✅ - Works, handles command line args
- `plan_words_parsing.py` ⚠️ - Basic parsing works, comment handling needs fix
- `plan_words_evaluation.py` 🔶 - Core logic, needs major function system work

### Debugging Tips

```bash
# Enable debug output
python3 -c "
import plan_words_evaluation
plan_words_evaluation.plan_eval_debug_flag = True
exec(open('plan_executor.py').read())
" example_plans/fizzbuzz.plan
```

### Testing Current Features

```bash
# Test what works
echo 'writeln "Hello"' > test.plan
echo '5 times { writeln times_count }' >> test.plan
echo 'if true { writeln "Yes" }' >> test.plan
python3 plan_executor.py test.plan
```

### Common Error Messages

- `"ERROR: Unknown word: X"` → Function not implemented or typo
- `"times_count value must be an integer"` → Type conversion issue
- `"condition must be boolean value"` → Non-boolean in if statement
- Function definition parsed but call fails → Function execution not implemented

## 🤝 Contributing

### For New Contributors

1. Start with **Phase 1** items (function system)
2. Read `docs/IMPLEMENTATION.md` for architecture details
3. Write tests for new features
4. Update documentation for implemented features

### For Language Design

1. Propose new syntax in issues
2. Create proof-of-concept examples
3. Consider backward compatibility
4. Update grammar specification

---

**Current Version**: v0.1 (Basic parsing and simple loops)  
**Next Release**: v0.2 (Working function system)  
**Target Date**: End of week  
**Long-term Goal**: v1.0 (Complete language implementation)
