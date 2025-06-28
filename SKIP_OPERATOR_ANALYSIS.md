# The Critical skipOperator Pattern in Pangea-js
## Why This Parameter is Essential for Operator Handling

The `skipOperator` parameter in pangea-js's `phraseLength` function is **absolutely critical** for proper operator precedence and recursion control. This is one of the most important insights from pangea-js architecture.

## 🔄 The Infinite Recursion Problem

Without `skipOperator`, parsing expressions like `"3 + 2"` would cause infinite recursion:

```
phraseLength("3") 
  -> sees next word "+" (infix operator)
  -> calls phraseLength("+") 
    -> arity of "+" is 1, needs right operand
    -> calls phraseLength("2")
      -> sees next word (none), returns 1
    -> BUT THEN: infix operators also need LEFT operand
    -> calls phraseLength("3") again!
    -> INFINITE RECURSION!
```

## ✅ How skipOperator Solves This

The `skipOperator=true` parameter tells the function:
**"Calculate this phrase length, but DON'T include any trailing operators"**

```javascript
// From pangea-js source
function phraseLength(wordIndex, skipOperator = false) {
    // Cache check - ONLY when not skipping operators
    if (skipOperator == false)
        if (phraseLengths[wordIndex] !== undefined)
            return phraseLengths[wordIndex]
    
    // ... calculate length ...
    
    // CRITICAL: Only check for operators when not skipping
    if (skipOperator == false) {
        var nextWord = words[nextIndex()]
        if (nextWord !== undefined) {
            var entry = namespace[nextWord]
            if (entry && (entry.operator == "postfix" || entry.operator == "infix"))
                length += phraseLength(nextIndex()) // Recursive call WITHOUT skipOperator
        }
    }
    
    // Cache ONLY when not skipping
    if (skipOperator == false)
        phraseLengths[wordIndex] = length
    return length
}
```

## 🎯 The Pattern in Action

For expression: `"fizz" when true`

### Without skipOperator (Broken):
```
phraseLength(0) // "fizz"
  -> length = 1
  -> next word is "when" (infix)
  -> calls phraseLength(1) // "when"
    -> arity = 2, needs 2 operands
    -> LEFT operand: calls phraseLength(0) // "fizz" AGAIN!
    -> INFINITE RECURSION
```

### With skipOperator (Correct):
```
phraseLength(0, false) // "fizz"
  -> length = 1
  -> next word is "when" (infix)
  -> calls phraseLength(1, false) // "when"
    -> arity = 2
    -> LEFT operand already processed (index 0)
    -> RIGHT operand: calls phraseLength(2, false) // "true"
    -> returns 1 + 1 = 2
  -> returns 1 + 2 = 3

// When executing the operator:
wordExec(0, false) // "fizz"
  -> detects "when" at next position
  -> calls wordExec(0, true) // "fizz" with skipOperator=TRUE
    -> returns "fizz" (no operator processing)
  -> calls wordExec(2, false) // "true"
    -> returns true
  -> executes: "fizz" when true -> "fizz"
```

## 🏗️ Our Implementation in Plan Language

Looking at your selected code:
```plan
def i#0
times_count 1
```

This should be parsed as:
- `def` (function definition, arity=2)
  - Parameter 1: `i#0` (function signature) 
  - Parameter 2: `times_count 1` (function body)

The phrase lengths should be:
- `def`: 4 (covers entire definition)
- `i#0`: 1 (function signature)  
- `times_count`: 2 (function call with 1 arg)
- `1`: 1 (literal argument)

## 🎯 Key Insights for Our Improvement

1. **Cache Control**: Only cache when `skipOperator=false`
2. **Recursion Breaking**: Use `skipOperator=true` when getting operands
3. **Operator Detection**: Only look for trailing operators when `skipOperator=false`
4. **Context Separation**: Cleanly separate operand parsing from operator parsing

This pattern is what makes pangea-js's unified namespace practical - it prevents the chaos that would otherwise result from everything being in one namespace.

## 🚀 Our Enhancement Opportunities

We can improve on pangea-js by:

1. **Better Type Safety**: Add compile-time operator validation
2. **Precedence Levels**: Explicit precedence instead of implicit
3. **Error Recovery**: Graceful handling of malformed expressions
4. **Debug Introspection**: Better debugging tools for phrase boundaries
5. **Performance**: Smarter caching strategies

The `skipOperator` pattern is the foundation that makes all these improvements possible!
