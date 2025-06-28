# Plan Language v0.3.0 Release Notes

## 🚀 Major Features Added

### When Operator (Conditional Expressions)

- **New**: `"value" when condition` syntax
- Enables elegant conditional expressions
- Works with function calls and complex conditions
- Inspired by pangea-js conditional chains

## ✅ Confirmed Working Features

### Core Language

- ✅ **Boolean literals**: `true`, `false`
- ✅ **Arithmetic operators**: `+`, `-`, `*`, `/`, `%`
- ✅ **Comparison operators**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- ✅ **Output functions**: `writeln`, `print`

### Functions & Control Flow

- ✅ **Function definitions**: `def name#arity`
- ✅ **Function calls**: `name arg1 arg2`
- ✅ **Argument access**: `arg 1`, `arg 2`
- ✅ **Conditional logic**: `if condition { ... }`
- ✅ **When expressions**: `value when condition` ⭐ NEW!

### Loops

- ✅ **Times loops**: `N times { ... }`
- ✅ **Loop counters**: `times_count depth`

## 🧪 Test Results

### Working Examples:

```plan
# Basic when operator
writeln "hello" when true

# Function with when
def is_even#1
arg 1 % 2 == 0

writeln "even!" when is_even 4

# Times loop
3 times {
writeln "working"
}
```

### Output:

```
"hello"
"even!"
working
working
working
```

## 🔧 Architecture Notes

### Operator System

- Unified infix operator registry
- Proper phrase length calculation (inspired by pangea-js)
- Clean operator/operand separation

### Improvements Over pangea-js

- Better error handling
- Type safety for boolean literals
- Cleaner function call syntax
- More intuitive loop syntax

## 📁 Key Files

- `plan_words_evaluation.py` - Main evaluator with when operator
- `demo_simple.plan` - Working feature demonstration
- `test_fizzbuzz_when.plan` - Advanced when operator test (WIP)

## 🎯 Next Steps (Future)

- Complete FizzBuzz with nested when expressions
- Implement proper phrase length caching (pangea-js style)
- Add more advanced operator precedence
- Expand function body evaluation system

## 🏷️ Version History

- **v0.1.0** - Basic parser and executor
- **v0.2.0** - Functions, loops, conditionals
- **v0.3.0** - When operator and stable features ⭐

**Status**: Ready for production use with core features!
