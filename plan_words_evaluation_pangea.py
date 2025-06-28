# Plan Language - True Pangea-js Architecture Implementation
# Implementing the core pangea-js innovations with Python improvements

import json
from typing import Dict, List, Any, Optional, Callable, Union

# Core namespace (pangea-js style)
namespace = {
    'arities': {},           # Function arity registry
    'stack': [{}],           # Function call stack  
    'times_stack': [],       # Loop counter stack
    'each_stack': [],        # Iterator stack (future)
}

# Global state
words: List[str] = []
phrase_lengths: List[int] = []
debug_enabled = False

def debug_print(*args):
    if debug_enabled:
        print("debug:", *args)

# Core parsing (pangea-js inspired)
def parse_literal(text: str) -> Any:
    """Parse JSON literals (numbers, strings, booleans)"""
    try:
        return json.loads(text)
    except:
        return None

def is_literal(word: str) -> bool:
    """Check if word is a literal value"""
    return parse_literal(word) is not None

def handle_plus_encoding(word: str) -> str:
    """Handle pangea-js + encoding for spaces in strings"""
    if not isinstance(parse_literal(word), str):
        return word
    
    text = parse_literal(word)
    parts = text.split("(+)")
    parts = [part.replace("+", " ") for part in parts]
    result = "+".join(parts)
    return json.dumps(result)

def parse_code(code: str) -> List[str]:
    """Parse code into words (pangea-js style)"""
    words = code.split()
    words = [handle_plus_encoding(word) for word in words]
    return words

# Phrase length calculation (core pangea-js innovation)
def word_arity(word: str) -> Optional[int]:
    """Get the arity of a word"""
    # Function definitions with #
    if "#" in word and not isinstance(parse_literal(word), str):
        return 0  # Function definitions take no args during definition
    
    # Check namespace
    entry = namespace.get(word) or namespace['arities'].get(word)
    if entry:
        return entry.get('arity')
    
    return None

def phrase_length(word_index: int, skip_operator: bool = False) -> int:
    """Calculate phrase length starting at word_index (pangea-js core)"""
    if skip_operator == False:
        if word_index < len(phrase_lengths) and phrase_lengths[word_index] is not None:
            return phrase_lengths[word_index]
    
    if word_index >= len(words):
        return 0
    
    length = 1
    word = words[word_index]
    
    if word is None:
        debug_print(f"ERROR: wrong word_index: {word_index}")
        return 0
    
    def next_index():
        return word_index + length
    
    # Single value (literals)
    if is_literal(word):
        pass  # length = 1
    
    # Block structures
    elif word in ["{", "[", "("]:
        matching_parens = {"{": "}", "[": "]", "(": ")"}
        while True:
            if next_index() >= len(words):
                break  # Close sequence at end
            if words[next_index()] == matching_parens[word]:
                length += 1
                break
            else:
                length += phrase_length(next_index())
    
    # Functions and operators (nested)
    else:
        arity = word_arity(word)
        if arity is not None:
            for i in range(arity):
                if next_index() < len(words):
                    length += phrase_length(next_index())
        else:
            debug_print(f"Word not in namespace: {word}")
    
    # Check for postfix/infix operators
    next_word_index = word_index + length
    if next_word_index < len(words) and not skip_operator:
        next_word = words[next_word_index]
        entry = namespace.get(next_word)
        if entry and entry.get('operator') in ['postfix', 'infix']:
            length += phrase_length(next_word_index)
    
    # Cache result
    if not skip_operator:
        # Extend phrase_lengths if needed
        while len(phrase_lengths) <= word_index:
            phrase_lengths.append(None)
        phrase_lengths[word_index] = length
    
    return length

# Word execution (pangea-js core)
def word_exec(word_index: int, skip_operator: bool = False) -> Any:
    """Execute word at index (pangea-js core function)"""
    if word_index >= len(words):
        debug_print(f"ERROR: wrong word_index: {word_index}")
        return None
    
    word = words[word_index]
    
    def next_index(skip_op: bool = False):
        return word_index + phrase_length(word_index, skip_op)
    
    # Check for postfix/infix operators first (pangea-js style)
    next_word_index = next_index(True)
    if next_word_index < len(words) and not skip_operator:
        next_word = words[next_word_index]
        entry = namespace.get(next_word)
        
        if entry and entry.get('operator') == 'postfix':
            return entry['func']([word_index])
        
        if entry and entry.get('operator') == 'infix':
            arity = entry['arity']
            params = [word_index]  # 1st operand (implicit)
            current_index = word_index + phrase_length(word_index, True)  # skip operand
            current_index += 1  # skip operator
            
            for i in range(arity):
                params.append(current_index)
                current_index += phrase_length(current_index)
            
            return entry['func'](params)
    
    # Single value (literals)
    if is_literal(word):
        return parse_literal(word)
    
    # Block structures
    elif word == "(":
        # Parentheses block - execute all, return last
        result = None
        current_index = word_index + 1
        while current_index < len(words) and words[current_index] != ")":
            result = word_exec(current_index)
            if result is not None:
                pass  # Keep last non-None result
            current_index += phrase_length(current_index)
        return result
    
    elif word == "[":
        # Array literal
        result = []
        current_index = word_index + 1
        while current_index < len(words) and words[current_index] != "]":
            element = word_exec(current_index)
            result.append(element)
            current_index += phrase_length(current_index)
        return result
    
    elif word == "{":
        # Object literal (key-value pairs)
        result = {}
        current_index = word_index + 1
        mode = "key"
        key = None
        while current_index < len(words) and words[current_index] != "}":
            element = word_exec(current_index)
            if mode == "key":
                key = element
                mode = "value"
            else:  # mode == "value"
                result[key] = element
                mode = "key"
            current_index += phrase_length(current_index)
        return result
    
    # Function calls and built-ins
    else:
        # Extract function name (handle func#arity notation)
        func_id = word.split("#")[0] if "#" in word else word
        
        current = namespace.get(func_id)
        if current is None:
            debug_print(f"Undefined function: {func_id}")
            return None
        
        if isinstance(current, dict) and 'func' in current:
            arity = current['arity']
            func = current['func']
            
            # Collect parameters (word indices)
            params = []
            current_index = word_index + 1
            for i in range(arity):
                if current_index < len(words):
                    params.append(current_index)
                    current_index += phrase_length(current_index)
            
            return func(params)
        
        debug_print(f"Not handled: {word}")
        return None

# Operator factory (pangea-js style)
def binary_operator(name: str, symbol: str, operation: Callable[[Any, Any], Any]):
    """Create binary infix operator"""
    def operator_func(params):
        left = word_exec(params[0], True)  # Skip operator on left operand
        right = word_exec(params[1])
        return operation(left, right)
    
    # Set function attributes
    operator_func.name = name
    operator_func.operator = "infix"
    operator_func.arity = 1  # For infix: left operand + 1 explicit operand
    operator_func.aliases = [symbol]
    
    return operator_func

# Initialize namespace with operators and built-ins
def init_namespace():
    """Initialize the namespace with core functions and operators"""
    
    # Built-in functions
    def print_func(params):
        output = word_exec(params[0])
        print(output)
        return output
    
    def arg_func(params):
        index = word_exec(params[0])
        stack = namespace['stack']
        if stack and 'args' in stack[-1]:
            args = stack[-1]['args']
            if 1 <= index <= len(args):
                return args[index - 1]  # 1-based indexing
        return None
    
    def def_func(params):
        word = words[params[0]].split("#")
        func_id = word[0]
        arity = int(word[1])
        
        func_body_index = params[1]
        
        def user_func(func_params):
            # Evaluate arguments
            args = [word_exec(p) for p in func_params]
            
            # Push context
            namespace['stack'].append({'args': args})
            
            # Execute function body
            result = word_exec(func_body_index)
            
            # Pop context
            namespace['stack'].pop()
            
            return result
        
        # Register function
        namespace[func_id] = {
            'arity': arity,
            'func': user_func
        }
        
        return None
    
    def when_func(params):
        """Pangea-js when operator: value when condition else-value"""
        condition = word_exec(params[1])
        if condition:
            return word_exec(params[0], True)  # Return value
        else:
            return word_exec(params[2])  # Return else-value
    
    def times_func(params):
        """Times loop with stack management"""
        count = word_exec(params[0], True)
        
        namespace['times_stack'].append(1)
        result = None
        
        try:
            for i in range(count):
                namespace['times_stack'][-1] = i + 1
                result = word_exec(params[1])
        finally:
            namespace['times_stack'].pop()
        
        return result
    
    def times_count_func(params):
        """Get current loop counter with depth"""
        depth = word_exec(params[0])
        stack = namespace['times_stack']
        if stack and 1 <= depth <= len(stack):
            return stack[-depth]
        return 0
    
    # Register built-in functions
    namespace.update({
        'print': {'arity': 1, 'func': print_func},
        'arg': {'arity': 1, 'func': arg_func},
        'def': {'arity': 2, 'func': def_func},
        'when': {'arity': 2, 'operator': 'infix', 'func': when_func},
        'times': {'arity': 1, 'operator': 'infix', 'func': times_func},
        'times_count': {'arity': 1, 'func': times_count_func},
    })
    
    # Register binary operators
    operators = [
        ('add', '+', lambda a, b: a + b),
        ('subtract', '-', lambda a, b: a - b),
        ('multiply', '*', lambda a, b: a * b),
        ('divide', '/', lambda a, b: a / b),
        ('modulus', '%', lambda a, b: a % b),
        ('equal', '==', lambda a, b: a == b),
        ('not_equal', '!=', lambda a, b: a != b),
        ('less_than', '<', lambda a, b: a < b),
        ('greater_than', '>', lambda a, b: a > b),
        ('less_equal', '<=', lambda a, b: a <= b),
        ('greater_equal', '>=', lambda a, b: a >= b),
    ]
    
    for name, symbol, operation in operators:
        op_func = binary_operator(name, symbol, operation)
        namespace[name] = {
            'arity': op_func.arity,
            'operator': op_func.operator,
            'func': op_func
        }
        # Register alias
        namespace[symbol] = namespace[name]

# Main execution function (pangea-js style)
def exec_code(code: str) -> Any:
    """Execute code with pangea-js architecture"""
    global words, phrase_lengths
    
    # Initialize namespace
    init_namespace()
    
    # Parse code
    previous_length = len(words)
    parsed_words = parse_code(code)
    words.extend(parsed_words)
    
    debug_print("Words:", words)
    
    # Pre-scan for function definitions (pangea-js style)
    for word in words:
        if "#" in word and not isinstance(parse_literal(word), str):
            parts = word.split("#")
            func_id = parts[0]
            arity = int(parts[1])
            
            namespace['arities'][func_id] = {
                'arity': arity,
                'word': word
            }
    
    # Pre-calculate phrase lengths
    phrase_lengths = [None] * len(words)
    for i in range(len(words)):
        if phrase_lengths[i] is None:
            phrase_length(i)
    
    debug_print("Phrase lengths:", phrase_lengths)
    
    # Execute the new code
    if previous_length < len(words):
        result = word_exec(previous_length)
        return result
    
    return None

# Compatibility functions
def evaluate_plan(plan_words: List[str]) -> None:
    """Compatibility wrapper for existing Plan Language code"""
    global words, phrase_lengths
    words = ["("] + plan_words  # Begin with ( like pangea-js
    
    # Execute
    exec_code(" ".join(plan_words))

def set_debug(enabled: bool):
    """Enable/disable debug output"""
    global debug_enabled
    debug_enabled = enabled
