# Pangea Python Interpreter

A Python translation of the Pangea programming language interpreter, originally implemented in JavaScript. This interpreter implements a stack-based functional programming language with advanced features including function definitions, control flow, data structures, and operator overloading.

## Features

### Core Language Features

- **Function Definitions**: Define functions with explicit arity using `def funcname#arity`
- **Function Calls**: Call functions with parameters
- **Arguments**: Access function arguments using `arg n` (1-indexed)
- **Control Flow**: `if`, `times`, `when`, `unless` constructs
- **Data Structures**: Arrays `[1 2 3]` and objects `{"key" "value"}`
- **Operators**: Arithmetic, comparison, and logical operators
- **String Handling**: Quoted strings with special `(+)` syntax for spaces

### Operators

#### Infix Operators

- Arithmetic: `+`, `-`, `*`, `**` (exponent), `%` (modulus)
- Comparison: `==`, `<`, `>`, `<=`
- Logical: `when` (ternary), `unless`

#### Postfix Operators

- `squared`: Square a number (e.g., `5 squared` → `25`)

#### Prefix Operators

- `print`: Output a value
- `times`: Repeat execution
- `if`: Conditional execution
- `def`: Function definition

### Built-in Functions

- `print value`: Print a value to console
- `times count block`: Execute block count times
- `times_count depth`: Get current iteration counter
- `if condition then else`: Conditional execution
- `when condition value`: Return value if condition is true
- `unless condition block`: Execute block if condition is false
- `def name#arity body`: Define a function
- `arg index`: Get function argument (1-indexed)
- `each iterable block`: Iterate over arrays/objects
- `each_item`, `each_key`: Get current iteration item/key
- `each_break`: Break from iteration

## Usage Examples

### Basic Arithmetic

```pangea
print 3 + 4        # Output: 7
print 5 squared    # Output: 25
print 2 ** 3       # Output: 8
```

### Function Definition

```pangea
def greet#1 (
    print "Hello,"
    print arg 1
)
greet "World"      # Output: Hello, World
```

### Recursion (Factorial)

```pangea
def factorial#1
if ( arg 1 ) == 0
    1
    ( arg 1 ) * factorial ( arg 1 ) - 1

print factorial 5  # Output: 120
```

### Loops

```pangea
5 times print "Hello"    # Prints "Hello" 5 times

10 times (
    print times_count 1  # Prints 1, 2, 3, ..., 10
)
```

### Conditional Logic

```pangea
print "positive" when 5 > 0    # Output: positive
if true print "yes" print "no" # Output: yes
```

### Data Structures

```pangea
print [ 1 2 3 4 5 ]                           # Array
print { "name" "John" "age" 30 }             # Object

# Iteration
[ 1 2 3 ] each (
    print each_item
)
```

### FizzBuzz Example

```pangea
def multiple#2
0 == ( ( arg 1 ) % ( arg 2 ) )

def i#0
times_count 1

def multiple_of#1
multiple i arg 1

20 times (
    print
    "fizz-buzz" when multiple_of 15
    "fizz" when multiple_of 3
    "buzz" when multiple_of 5
    i
)
```

## Installation and Running

### Requirements

- Python 3.6+

### Running the Interpreter

```bash
# Run the main interpreter with built-in tests
python3 pangea_python_interpreter.py

# Run additional test cases
python3 test_pangea_interpreter.py
```

### Using as a Module

```python
from pangea_python_interpreter import PangeaInterpreter

interpreter = PangeaInterpreter()
result = interpreter.exec('print 2 + 3')  # Output: 5
```

## Architecture

### Core Components

1. **PangeaInterpreter**: Main interpreter class
2. **Word Parsing**: Tokenizes input code into words
3. **Phrase Length Calculation**: Determines expression boundaries
4. **Word Execution**: Evaluates individual words and expressions
5. **Namespace Management**: Handles function definitions and built-ins

### Key Methods

- `exec(code)`: Execute Pangea code
- `word_exec(index)`: Execute word at given index
- `_phrase_length(index)`: Calculate phrase length for parsing
- `parse_code(code)`: Tokenize code into words

### Special Features

#### String Handling

Strings use special `(+)` syntax for embedded spaces:

```pangea
print "hello+world+(+)test"  # Outputs: "hello world + test"
```

#### Operator Precedence

The language uses prefix notation primarily, with special handling for infix and postfix operators:

- Postfix: `5 squared`
- Infix: `5 + 3`, `x when condition`
- Prefix: `print value`, `times 5 block`

#### Function Arity

Functions must declare their arity (number of parameters):

```pangea
def add#2 ( arg 1 ) + ( arg 2 )    # Function takes 2 arguments
def greet#1 print arg 1            # Function takes 1 argument
def nothing#0 print "hello"        # Function takes 0 arguments
```

## Differences from JavaScript Version

This Python implementation maintains compatibility with the original JavaScript version while leveraging Python's features:

1. **Type System**: Uses Python's dynamic typing
2. **Error Handling**: More robust error handling with Python exceptions
3. **Data Structures**: Uses Python lists and dictionaries
4. **String Processing**: Uses Python's string methods and regex
5. **JSON Parsing**: Uses Python's json module for literal parsing

## Testing

The interpreter includes comprehensive tests covering:

- Basic arithmetic and operators
- Function definitions and calls
- Control flow constructs
- Data structure manipulation
- Complex recursive examples
- Edge cases and error conditions

Run tests with:

```bash
python3 test_pangea_interpreter.py
```

## Contributing

This is a translation of the original Pangea JavaScript interpreter. When contributing:

1. Maintain compatibility with the original language semantics
2. Follow Python coding conventions
3. Add tests for new features
4. Update documentation

## License

This project maintains the same license as the original Pangea JavaScript implementation.
