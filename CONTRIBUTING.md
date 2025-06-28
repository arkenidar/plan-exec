# Contributing to Plan Language

## 🎯 Current Development Focus

We're currently working on **Phase 1: Core Function System (v0.2)** - implementing the pangea-js inspired unified operator and function system.

### ✅ Recently Completed

1. **Boolean literals** - ✅ `true`/`false` support working
2. **Infix operators** - ✅ Arithmetic (`+`, `-`, `*`, `/`, `%`) and comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`) working
3. **Unified system foundation** - ✅ Call stack and operator framework implemented

### 🔧 Current Priorities

1. **Function calls** - Make `def add#2` actually callable (partially working)
2. **Argument passing** - Fix `arg 1`, `arg 2` to return actual values from call stack
3. **Function scope** - Complete call stack and argument isolation
4. **Infix times** - Implement `N times { block }` syntax

## 🛠️ Development Setup

### Prerequisites

- Python 3.7+
- Git

### Getting Started

```bash
git clone <repository-url>
cd plan-exec
python3 test_current_features.py  # Run test suite
python3 plan_executor.py example_plans/testing.plan  # Test current functionality
```

### Testing Your Changes

```bash
# Run the test suite
python3 test_current_features.py

# Test unified system features
python3 plan_executor.py test_unified_features.plan

# Test specific examples
python3 plan_executor.py example_plans/testing.plan
python3 plan_executor.py example_plans/fizzbuzz.plan  # Currently fails

# Enable debug output
python3 -c "
import plan_words_evaluation
plan_words_evaluation.plan_eval_debug_flag = True
exec(open('plan_executor.py').read())
" example_plans/testing.plan
```

## 📋 Development Workflow

### Before You Start

1. Check [STATUS.md](STATUS.md) for current priorities
2. Look at existing issues or create a new one
3. Read [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) for architecture

### Making Changes

1. **Create a feature branch**: `git checkout -b feature/function-calls`
2. **Make your changes** in small, focused commits
3. **Test thoroughly** with the test suite
4. **Update documentation** if needed
5. **Commit with descriptive messages** (see commit message format below)

### Commit Message Format

```
type(scope): brief description

Detailed explanation of what changed and why.

- List specific changes
- Include any breaking changes
- Reference issues if applicable

Known issues:
- List any new issues introduced
- Document workarounds if any
```

**Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`

**Examples**:

```
feat(functions): implement basic function call mechanism

- Add function lookup in evaluate_word
- Add argument passing via call stack
- Add basic function scope isolation
- Add return value handling

Known issues:
- Nested function calls not tested
- Recursion depth not limited
```

## 🎯 Areas That Need Help

### 🔥 High Priority (v0.2)

- **Function execution**: Complete function call mechanism (def/call partially working)
- **Argument handling**: Fix `arg N` to return actual values from call stack
- **Call stack**: Complete proper function call stack (foundation implemented)
- **Infix times**: Implement `N times { block }` syntax

### 🔶 Medium Priority (v0.3)

- **Loop contexts**: Implement nested loop counter stack
- **Context system**: Add proper scope management
- **Control flow**: Add `return`, `break`, `continue`

### 🔵 Low Priority (v0.4+)

- **When expressions**: Implement conditional expressions
- **Error handling**: Better error messages
- **Performance**: Optimize execution
- **Standard library**: Add built-in functions

## 🧪 Testing Guidelines

### Test Categories

1. **Unit tests**: Test individual functions
2. **Integration tests**: Test feature combinations
3. **Regression tests**: Ensure fixes don't break existing features
4. **Example tests**: Ensure documentation examples work

### Adding Tests

When adding a feature, also add:

- Test cases in `test_current_features.py`
- Example in `docs/EXAMPLES.md`
- Documentation in appropriate docs file

### Test Requirements

- All tests should pass before committing
- New features need corresponding tests
- Bug fixes need regression tests
- Examples in documentation should work

## 📚 Documentation

### Documentation Files

- **README.md**: Project overview and quick start
- **STATUS.md**: Current status and roadmap
- **docs/TUTORIAL.md**: Learning guide
- **docs/SYNTAX.md**: Language reference
- **docs/EXAMPLES.md**: Code examples
- **docs/IMPLEMENTATION.md**: Architecture details

### Updating Documentation

- Keep examples current with implementation
- Update STATUS.md when features are completed
- Add new examples for new features
- Update roadmap when priorities change

## 🐛 Bug Reports

### Good Bug Reports Include

1. **Clear description** of the problem
2. **Steps to reproduce** the issue
3. **Expected behavior** vs actual behavior
4. **Plan code** that demonstrates the issue
5. **Error messages** if any
6. **Environment** (Python version, OS)

### Example Bug Report

```
**Problem**: Function calls silently fail instead of executing

**Steps to reproduce**:
1. Create file with: `def add#2\narg 1 + arg 2\nwriteln add 5 3`
2. Run: `python3 plan_executor.py test.plan`

**Expected**: Should output `8`
**Actual**: No output, no error

**Error messages**: None
**Environment**: Python 3.9, Ubuntu 20.04
```

## 🎯 Feature Requests

### Good Feature Requests Include

1. **Use case**: Why is this feature needed?
2. **Proposed syntax**: How should it look?
3. **Examples**: Show how it would be used
4. **Alternatives**: Other ways to achieve the same goal
5. **Priority**: How important is this feature?

## 🏗️ Architecture Guidelines

### Code Organization

- **plan_executor.py**: Entry point, file handling
- **plan_words_parsing.py**: Tokenization and parsing
- **plan_words_evaluation.py**: Evaluation and execution
- **docs/**: All documentation
- **example_plans/**: Example programs

### Design Principles

1. **Simplicity**: Keep the language simple and understandable
2. **Consistency**: Similar operations should work similarly
3. **Predictability**: Avoid surprising behavior
4. **Extensibility**: Make it easy to add new features
5. **Performance**: Don't sacrifice correctness for speed

### Code Style

- Follow Python PEP 8 conventions
- Use descriptive variable and function names
- Add comments for complex logic
- Keep functions focused and small
- Use type hints where helpful

## 🤝 Getting Help

### Communication

- **Issues**: For bugs, feature requests, and questions
- **Discussions**: For general questions and ideas
- **Documentation**: Check docs/ directory first

### Learning Resources

1. Start with [docs/TUTORIAL.md](docs/TUTORIAL.md)
2. Read [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) for architecture
3. Look at existing code in plan_words_evaluation.py
4. Check [STATUS.md](STATUS.md) for current focus

## 🎉 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- Git commit history
- Documentation authorship

Thank you for contributing to Plan Language! 🚀
