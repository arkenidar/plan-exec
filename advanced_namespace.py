# Plan Language - Advanced Namespace System
# Building upon pangea-js unified namespace with practical improvements

import types
from typing import Dict, List, Any, Callable, Optional, Union

class NamespaceManager:
    """Advanced namespace system that improves upon pangea-js unified approach"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all namespaces"""
        self.namespaces = {
            # Core language features (immutable)
            'core': {
                'operators': {},     # +, -, *, /, ==, when, etc.
                'control': {},       # if, times, def, etc.
                'literals': {},      # true, false, etc.
            },
            
            # User-defined elements (mutable)
            'user': {
                'functions': {},     # User-defined functions
                'variables': {},     # Future: user variables
            },
            
            # Execution context (dynamic)
            'runtime': {
                'call_stack': [{}],      # Function call contexts
                'loop_stack': [],        # Loop counter stack
                'scope_stack': [{}],     # Variable scopes (future)
            },
            
            # Module system (future expansion)
            'modules': {},
            
            # Metadata and introspection
            'meta': {
                'phrase_lengths': [],    # Pre-calculated phrase boundaries
                'word_types': {},        # Cache for word type lookups
                'aliases': {},           # Operator aliases (future)
            }
        }
        
        # Initialize core namespace
        self._init_core_namespace()
    
    def _init_core_namespace(self):
        """Initialize core language features"""
        
        # Core operators (improved from pangea-js)
        operators = {
            # Arithmetic (infix, arity 1)
            '+': {'type': 'infix', 'arity': 1, 'precedence': 5, 'func': lambda a, b: a + b},
            '-': {'type': 'infix', 'arity': 1, 'precedence': 5, 'func': lambda a, b: a - b},
            '*': {'type': 'infix', 'arity': 1, 'precedence': 6, 'func': lambda a, b: a * b},
            '/': {'type': 'infix', 'arity': 1, 'precedence': 6, 'func': lambda a, b: a / b},
            '%': {'type': 'infix', 'arity': 1, 'precedence': 6, 'func': lambda a, b: a % b},
            
            # Comparison (infix, arity 1)
            '==': {'type': 'infix', 'arity': 1, 'precedence': 3, 'func': lambda a, b: a == b},
            '!=': {'type': 'infix', 'arity': 1, 'precedence': 3, 'func': lambda a, b: a != b},
            '<': {'type': 'infix', 'arity': 1, 'precedence': 4, 'func': lambda a, b: a < b},
            '>': {'type': 'infix', 'arity': 1, 'precedence': 4, 'func': lambda a, b: a > b},
            '<=': {'type': 'infix', 'arity': 1, 'precedence': 4, 'func': lambda a, b: a <= b},
            '>=': {'type': 'infix', 'arity': 1, 'precedence': 4, 'func': lambda a, b: a >= b},
            
            # Conditional (infix, arity 2 - like pangea-js)
            'when': {'type': 'infix', 'arity': 2, 'precedence': 2, 'func': self._when_operator},
        }
        
        # Control structures (prefix)
        control = {
            'if': {'type': 'prefix', 'arity': 2, 'func': None},  # Special handling
            'times': {'type': 'infix', 'arity': 1, 'func': None},  # Special handling
            'def': {'type': 'prefix', 'arity': 2, 'func': None},  # Special handling
            'writeln': {'type': 'prefix', 'arity': 1, 'func': None},  # Special handling
            'write': {'type': 'prefix', 'arity': 1, 'func': None},  # Special handling
            'print': {'type': 'prefix', 'arity': -1, 'func': None},  # Variable arity
            'eval': {'type': 'prefix', 'arity': 1, 'func': None},  # Special handling
            'arg': {'type': 'prefix', 'arity': 1, 'func': None},  # Special handling
            'times_count': {'type': 'prefix', 'arity': 1, 'func': None},  # Special handling
        }
        
        # Literals
        literals = {
            'true': {'type': 'literal', 'value': True},
            'false': {'type': 'literal', 'value': False},
        }
        
        self.namespaces['core']['operators'] = operators
        self.namespaces['core']['control'] = control
        self.namespaces['core']['literals'] = literals
    
    def _when_operator(self, value, condition, else_value=None):
        """Implementation of the when operator (pangea-js style)"""
        return value if condition else else_value
    
    # Improved lookup methods (better than pangea-js)
    def lookup_word(self, word: str) -> Optional[Dict[str, Any]]:
        """Smart word lookup with fallback chain"""
        
        # 1. Check user functions first (highest priority)
        if word in self.namespaces['user']['functions']:
            return {
                'type': 'user_function',
                'namespace': 'user.functions',
                **self.namespaces['user']['functions'][word]
            }
        
        # 2. Check core operators
        if word in self.namespaces['core']['operators']:
            return {
                'type': 'operator',
                'namespace': 'core.operators',
                **self.namespaces['core']['operators'][word]
            }
        
        # 3. Check core control structures
        if word in self.namespaces['core']['control']:
            return {
                'type': 'control',
                'namespace': 'core.control',
                **self.namespaces['core']['control'][word]
            }
        
        # 4. Check literals
        if word in self.namespaces['core']['literals']:
            return {
                'type': 'literal',
                'namespace': 'core.literals',
                **self.namespaces['core']['literals'][word]
            }
        
        # 5. Check if it's a function definition (word#arity)
        if '#' in word and not word.startswith('"'):
            return {
                'type': 'function_definition',
                'namespace': 'meta',
                'arity': 0  # Function definitions take no args during definition
            }
        
        return None
    
    def get_word_arity(self, word: str) -> Optional[int]:
        """Get word arity with improved lookup"""
        entry = self.lookup_word(word)
        return entry.get('arity') if entry else None
    
    def get_word_type(self, word: str) -> Optional[str]:
        """Get word type (operator, control, literal, etc.)"""
        entry = self.lookup_word(word)
        return entry.get('type') if entry else None
    
    def is_operator(self, word: str) -> bool:
        """Check if word is an operator"""
        return self.get_word_type(word) == 'operator'
    
    def get_operator_info(self, word: str) -> Optional[Dict[str, Any]]:
        """Get complete operator information"""
        if self.is_operator(word):
            return self.lookup_word(word)
        return None
    
    # Function management (improved)
    def define_function(self, name: str, arity: int, body: List[str]):
        """Define a user function with better validation"""
        self.namespaces['user']['functions'][name] = {
            'arity': arity,
            'body': body,
            'defined_at': len(self.namespaces['runtime']['call_stack'])  # For debugging
        }
    
    def call_function(self, name: str, args: List[Any]) -> Any:
        """Call a user function with proper context management"""
        if name not in self.namespaces['user']['functions']:
            raise NameError(f"Function '{name}' not defined")
        
        func_def = self.namespaces['user']['functions'][name]
        
        if len(args) != func_def['arity']:
            raise ValueError(f"Function '{name}' expects {func_def['arity']} arguments, got {len(args)}")
        
        # Push new call context
        self.namespaces['runtime']['call_stack'].append({'args': args, 'function': name})
        
        try:
            # Execute function body with proper argument substitution
            func_body_str = ' '.join(func_def['body'])
            
            # Replace arg references
            for i in range(len(args)):
                func_body_str = func_body_str.replace(f'arg {i+1}', str(args[i]))
            
            # Try to evaluate as expression
            try:
                result = eval(func_body_str)
            except:
                result = func_body_str
            
            return result
        finally:
            # Pop call context
            self.namespaces['runtime']['call_stack'].pop()
    
    # Context management (improved)
    def push_loop_context(self):
        """Push a new loop context"""
        self.namespaces['runtime']['loop_stack'].append(1)
    
    def pop_loop_context(self):
        """Pop loop context"""
        if self.namespaces['runtime']['loop_stack']:
            self.namespaces['runtime']['loop_stack'].pop()
    
    def update_loop_counter(self, value: int):
        """Update current loop counter"""
        if self.namespaces['runtime']['loop_stack']:
            self.namespaces['runtime']['loop_stack'][-1] = value
    
    def get_loop_counter(self, depth: int = 1) -> int:
        """Get loop counter at specified depth"""
        stack = self.namespaces['runtime']['loop_stack']
        if len(stack) >= depth:
            return stack[-depth]
        return 0
    
    # Introspection methods (new improvement)
    def get_namespace_info(self) -> Dict[str, Any]:
        """Get information about all namespaces"""
        return {
            'core_operators': len(self.namespaces['core']['operators']),
            'core_control': len(self.namespaces['core']['control']),
            'user_functions': len(self.namespaces['user']['functions']),
            'call_stack_depth': len(self.namespaces['runtime']['call_stack']),
            'loop_stack_depth': len(self.namespaces['runtime']['loop_stack']),
        }
    
    def debug_dump(self) -> str:
        """Dump namespace state for debugging"""
        info = self.get_namespace_info()
        result = ["=== Namespace Debug Dump ==="]
        for key, value in info.items():
            result.append(f"{key}: {value}")
        
        result.append("\nUser Functions:")
        for name, func in self.namespaces['user']['functions'].items():
            result.append(f"  {name}#{func['arity']}: {func['body']}")
        
        result.append(f"\nCall Stack: {self.namespaces['runtime']['call_stack']}")
        result.append(f"Loop Stack: {self.namespaces['runtime']['loop_stack']}")
        
        return '\n'.join(result)

# Global namespace manager instance
namespace_manager = NamespaceManager()

# Compatibility functions for existing code
def get_word_arity(word: str) -> Optional[int]:
    return namespace_manager.get_word_arity(word)

def is_operator(word: str) -> bool:
    return namespace_manager.is_operator(word)

def lookup_word(word: str) -> Optional[Dict[str, Any]]:
    return namespace_manager.lookup_word(word)
