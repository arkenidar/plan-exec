# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-12-29

### Added - Major Release: Production-Ready Pangea Python Interpreter

#### New Core Implementation
- **`pangea_python_interpreter.py`** - Complete Python implementation of pangea-js
- **`pangea_cli.py`** - Full-featured command-line interface with REPL
- **Interactive REPL mode** with help, examples, and reset functionality
- **Comprehensive test suite** with real-world program validation

#### Advanced Language Features
- **Function definitions with arity** (`def funcname#arity`)
- **Recursive function support** (factorial, fibonacci, etc.)
- **Advanced operators**: infix, prefix, postfix
- **Data structures**: arrays `[ 1 2 3 ]`, objects `{ "key" "value" }`
- **String formatting** with special `(+)` syntax
- **Each iteration** with `each_item`, `each_key`, `each_break`
- **Complex control flow** with nested conditionals and loops

#### Operator System
- **Mathematical operators**: `+`, `-`, `*`, `**`, `%`, `squared`
- **Comparison operators**: `==`, `<`, `>`, `<=`, `>=`
- **Logical operators**: `when`, `unless`, `if`
- **Loop constructs**: `times` with `times_count`

#### Architecture Improvements
- **Word-based execution model** matching pangea-js exactly
- **Phrase length calculation** for proper expression parsing
- **Stack-based function calls** with argument passing
- **Namespace management** for built-ins and user functions
- **skipOperator mechanism** preventing infinite recursion

#### Examples and Documentation
- **`sample.pangea`** - Comprehensive example programs
- **FizzBuzz implementation** - Classic programming example
- **Factorial and Fibonacci** - Recursive function examples
- **Real-world test programs** from user-authored files

### Enhanced Plan Language Features
- **Improved function definitions** with better parsing
- **When operator chains** for conditional expressions
- **Better error handling** and debugging output
- **Index tracking fixes** for reliable execution

### Testing Infrastructure
- **`test_pangea_interpreter.py`** - Comprehensive test suite
- **`test_user_files.py`** - Real-world program testing
- **Multiple specialized test files** for feature validation
- **Automated testing** of all core functionality

### Command-Line Tools
- **Interactive REPL** with help and examples
- **File execution** support
- **Direct code execution** with `-c` flag
- **Comprehensive help system**

### Documentation
- **Updated README.md** with complete usage guide
- **Architecture documentation** explaining implementation
- **Example code** for all major features
- **Testing instructions** and contribution guidelines

## [0.3.0] - Previous Version

### Added
- When operator implementation
- Boolean literal support
- Basic function definitions
- Loop constructs with times_count
- Conditional statements (if, if-else)

### Fixed
- Function parsing issues
- Operator precedence problems
- Index tracking in evaluation

## [0.2.0] - Previous Version

### Added
- Basic plan language executor
- Simple function definitions
- Basic operators
- File parsing capability

### Fixed
- Various parsing and evaluation bugs

## [0.1.0] - Initial Version

### Added
- Initial plan language implementation
- Basic parsing infrastructure
- Simple evaluation system

---

## Migration Guide

### From v0.3.0 to v1.0.0

The main Plan Language functionality remains compatible. New Pangea interpreter is additional:

```bash
# Old way (still works)
python3 plan_executor.py myfile.plan

# New Pangea interpreter
python3 pangea_cli.py myfile.pangea
python3 pangea_cli.py -c 'print "Hello World"'
python3 pangea_cli.py  # Interactive mode
```

### Key Changes

1. **New file**: `pangea_python_interpreter.py` - Use this for Pangea programs
2. **CLI tool**: `pangea_cli.py` - Interactive and file execution
3. **Enhanced syntax**: Full pangea-js compatibility
4. **Better testing**: Run `test_pangea_interpreter.py` for validation

The Plan Language executor continues to work as before, while the new Pangea interpreter provides enhanced capabilities and pangea-js compatibility.
