# plan_words_evaluation_unified.py
# Unified operator and function system inspired by pangea-js

import json
import re

# Global state
plan_eval_debug_flag = False
words = []
phrase_lengths = []

# Namespace system
namespace = {
    'arities': {},      # Function name -> arity mapping
    'functions': {},    # Function implementations 
    'stack': [{}],      # Call stack for function arguments
    'times_stack': [],  # Loop counter stack
    'operators': {}     # Operator definitions
}

def debug_print(*args):
    global plan_eval_debug_flag
    if plan_eval_debug_flag:
        print("debug:", *args)

def parse_literal(text):
    """Parse JSON literals (strings, numbers, booleans)"""
    try:
        return json.loads(text)
    except:
        return None

def is_literal(text):
    """Check if text is a parseable literal"""
    return parse_literal(text) is not None

def phrase_length(word_index, skip_operator=False):
    """Calculate the length of a phrase starting at word_index"""
    global phrase_lengths, words
    
    if not skip_operator and word_index < len(phrase_lengths):
        if phrase_lengths[word_index] is not None:
            return phrase_lengths[word_index]
    
    if word_index >= len(words):
        return 0
        
    length = 1
    word = words[word_index]
    
    def next_index():
        return word_index + length
    
    def word_arity(word):
        """Get arity of a word"""
        if "#" in word:
            return 0  # Composite names have 0 arity during parsing
        
        # Check namespace
        if word in namespace['functions']:
            return namespace['functions'][word].get('arity', 0)
        if word in namespace['arities']:
            return namespace['arities'][word]['arity']
        if word in namespace['operators']:
            return namespace['operators'][word].get('arity', 0)
            
        # Built-in functions
        builtins = {
            'writeln': 1, 'write': 1, 'print': 1, 'eval': 1,
            'if': 3, 'def': 2, 'arg': 1, 'times_count': 1,
            'true': 0, 'false': 0
        }
        return builtins.get(word, None)
    
    # Handle literals
    if is_literal(word):
        pass  # length = 1
    
    # Handle blocks
    elif word in ["{", "[", "("]:
        matching = {"{": "}", "[": "]", "(": ")"}
        while next_index() < len(words):
            if words[next_index()] == matching[word]:
                length += 1
                phrase_lengths[next_index()] = 1
                break
            else:
                length += phrase_length(next_index())
    
    # Handle function calls and operators
    else:
        arity = word_arity(word)
        if arity is not None:
            for i in range(arity):
                if next_index() < len(words):
                    length += phrase_length(next_index())
    
    # Handle postfix and infix operators
    if not skip_operator and next_index() < len(words):
        next_word = words[next_index()]
        if next_word in namespace['operators']:
            op = namespace['operators'][next_word]
            if op.get('type') in ['postfix', 'infix']:
                length += phrase_length(next_index())
    
    if not skip_operator:
        if word_index < len(phrase_lengths):
            phrase_lengths[word_index] = length
    
    return length

def word_exec(word_index, skip_operator=False):
    """Execute a word at the given index"""
    global words, namespace
    
    if word_index >= len(words):
        debug_print("ERROR: word_index out of bounds:", word_index)
        return None
    
    word = words[word_index]
    debug_print(f"Executing word[{word_index}]: {word}")
    
    def next_index(skip_op=False):
        return word_index + phrase_length(word_index, skip_op)
    
    # Handle postfix and infix operators first
    if not skip_operator and next_index(True) < len(words):
        next_word = words[next_index(True)]
        if next_word in namespace['operators']:
            op = namespace['operators'][next_word]
            
            if op.get('type') == 'postfix':
                return op['func']([word_index])
            
            elif op.get('type') == 'infix':
                arity = op.get('arity', 1)
                params = [word_index]  # First operand
                idx = word_index + phrase_length(word_index, True) + 1  # Skip operand and operator
                for i in range(arity):
                    if idx < len(words):
                        params.append(idx)
                        idx += phrase_length(idx)
                return op['func'](params)
    
    # Handle literals
    if is_literal(word):
        return parse_literal(word)
    
    # Handle blocks
    elif word == "(":
        result = None
        idx = word_index + 1
        while idx < len(words) and words[idx] != ")":
            result = word_exec(idx)
            idx += phrase_length(idx)
        return result
    
    elif word == "[":
        result = []
        idx = word_index + 1
        while idx < len(words) and words[idx] != "]":
            element = word_exec(idx)
            result.append(element)
            idx += phrase_length(idx)
        return result
    
    elif word == "{":
        result = {}
        idx = word_index + 1
        mode = "key"
        key = None
        while idx < len(words) and words[idx] != "}":
            element = word_exec(idx)
            if mode == "key":
                key = element
                mode = "value"
            else:
                result[key] = element
                mode = "key"
            idx += phrase_length(idx)
        return result
    
    # Handle function calls
    else:
        # Extract function name (remove #arity if present)
        func_id = word.split("#")[0] if "#" in word else word
        
        # Check if it's a built-in or user-defined function
        if func_id in namespace['functions']:
            func = namespace['functions'][func_id]
            arity = func['arity']
            
            # Collect arguments
            params = []
            idx = word_index + 1
            for i in range(arity):
                if idx < len(words):
                    params.append(idx)
                    idx += phrase_length(idx)
            
            return func['func'](params)
        
        # Handle built-in functions
        elif func_id in ['writeln', 'write', 'print', 'eval', 'if', 'def', 'arg', 'times_count', 'true', 'false', 'times']:
            return handle_builtin(func_id, word_index)
        
        else:
            debug_print(f"ERROR: Unknown word: {word}")
            print(f"ERROR: Unknown word: {word}")
            return None

def handle_builtin(func_name, word_index):
    """Handle built-in functions"""
    global namespace, words
    
    if func_name == 'true':
        return True
    elif func_name == 'false':
        return False
    
    elif func_name == 'writeln' or func_name == 'write':
        if word_index + 1 < len(words):
            value = word_exec(word_index + 1)
            end_char = "\n" if func_name == 'writeln' else ""
            print(value, end=end_char)
            return value
        return None
    
    elif func_name == 'print':
        if word_index + 1 < len(words):
            value = word_exec(word_index + 1)
            print(value)
            return value
        return None
    
    elif func_name == 'eval':
        if word_index + 1 < len(words):
            expr = word_exec(word_index + 1)
            try:
                return eval(str(expr))
            except:
                debug_print(f"ERROR: Cannot evaluate: {expr}")
                return None
        return None
    
    elif func_name == 'if':
        # if condition true_branch false_branch
        if word_index + 3 < len(words):
            condition = word_exec(word_index + 1)
            if condition:
                return word_exec(word_index + 2)
            else:
                return word_exec(word_index + 3)
        return None
    
    elif func_name == 'def':
        # def function_name#arity body
        if word_index + 2 < len(words):
            func_def_word = words[word_index + 1]
            body_index = word_index + 2
            
            if "#" in func_def_word:
                func_name, arity_str = func_def_word.split("#")
                arity = int(arity_str)
                
                # Store function definition
                namespace['functions'][func_name] = {
                    'arity': arity,
                    'func': lambda params, body_idx=body_index: call_user_function(params, body_idx)
                }
                
                debug_print(f"Defined function: {func_name} with arity {arity}")
                return None
            else:
                debug_print(f"ERROR: Invalid function definition: {func_def_word}")
                return None
        return None
    
    elif func_name == 'arg':
        if word_index + 1 < len(words):
            arg_num = word_exec(word_index + 1)
            stack = namespace['stack']
            if len(stack) > 0 and 'args' in stack[-1]:
                args = stack[-1]['args']
                if 1 <= arg_num <= len(args):
                    return args[arg_num - 1]
            debug_print(f"ERROR: Cannot access arg {arg_num}")
            return f"arg_{arg_num}"  # Fallback
        return None
    
    elif func_name == 'times_count':
        if word_index + 1 < len(words):
            depth = word_exec(word_index + 1)
            stack = namespace['times_stack']
            if len(stack) >= depth:
                return stack[-depth]
            return 1  # Fallback
        return 1
    
    elif func_name == 'times':
        # Handle infix times: count times block
        if word_index - 1 >= 0 and word_index + 1 < len(words):
            # This should be handled by infix operator
            pass
        return None
    
    return None

def call_user_function(params, body_index):
    """Call a user-defined function"""
    global namespace
    
    # Evaluate arguments
    args = [word_exec(param) for param in params]
    
    # Push new call frame
    namespace['stack'].append({'args': args})
    
    # Execute function body
    result = word_exec(body_index)
    
    # Pop call frame
    namespace['stack'].pop()
    
    return result

def setup_operators():
    """Set up built-in operators"""
    global namespace
    
    # Infix operators
    def make_binary_op(operation):
        def binary_op(params):
            left = word_exec(params[0], True)
            right = word_exec(params[1])
            return operation(left, right)
        return binary_op
    
    # Arithmetic operators
    namespace['operators']['+'] = {
        'type': 'infix', 'arity': 1,
        'func': make_binary_op(lambda a, b: a + b)
    }
    namespace['operators']['-'] = {
        'type': 'infix', 'arity': 1,
        'func': make_binary_op(lambda a, b: a - b)
    }
    namespace['operators']['*'] = {
        'type': 'infix', 'arity': 1,
        'func': make_binary_op(lambda a, b: a * b)
    }
    namespace['operators']['/'] = {
        'type': 'infix', 'arity': 1,
        'func': make_binary_op(lambda a, b: a / b)
    }
    namespace['operators']['%'] = {
        'type': 'infix', 'arity': 1,
        'func': make_binary_op(lambda a, b: a % b)
    }
    
    # Comparison operators
    namespace['operators']['=='] = {
        'type': 'infix', 'arity': 1,
        'func': make_binary_op(lambda a, b: a == b)
    }
    namespace['operators']['!='] = {
        'type': 'infix', 'arity': 1,
        'func': make_binary_op(lambda a, b: a != b)
    }
    namespace['operators']['<'] = {
        'type': 'infix', 'arity': 1,
        'func': make_binary_op(lambda a, b: a < b)
    }
    namespace['operators']['>'] = {
        'type': 'infix', 'arity': 1,
        'func': make_binary_op(lambda a, b: a > b)
    }
    namespace['operators']['<='] = {
        'type': 'infix', 'arity': 1,
        'func': make_binary_op(lambda a, b: a <= b)
    }
    namespace['operators']['>='] = {
        'type': 'infix', 'arity': 1,
        'func': make_binary_op(lambda a, b: a >= b)
    }
    
    # Times operator (infix)
    def times_op(params):
        count = word_exec(params[0], True)  # Left operand (count)
        block_index = params[1]  # Right operand (block)
        
        result = None
        namespace['times_stack'].append(1)
        
        for i in range(count):
            result = word_exec(block_index)
            namespace['times_stack'][-1] += 1
        
        namespace['times_stack'].pop()
        return result
    
    namespace['operators']['times'] = {
        'type': 'infix', 'arity': 1,
        'func': times_op
    }
    
    # When operator (infix)
    def when_op(params):
        value = word_exec(params[0], True)  # What to return
        condition = word_exec(params[1])    # Condition to check
        else_value = word_exec(params[2]) if len(params) > 2 else None  # Else value
        
        return value if condition else else_value
    
    namespace['operators']['when'] = {
        'type': 'infix', 'arity': 2,
        'func': when_op
    }

def parse_words(code):
    """Parse code into words, similar to pangea-js"""
    # Simple whitespace split for now
    word_list = code.split()
    
    # Filter out empty words
    word_list = [w for w in word_list if w.strip()]
    
    return word_list

def pre_scan_arities(word_list):
    """Pre-scan for function definitions with arities"""
    global namespace
    
    for word in word_list:
        if "#" in word and not is_literal(word):
            parts = word.split("#")
            if len(parts) == 2:
                func_id = parts[0]
                try:
                    arity = int(parts[1])
                    namespace['arities'][func_id] = {
                        'arity': arity,
                        'word': word
                    }
                    debug_print(f"Pre-scanned arity: {func_id} -> {arity}")
                except ValueError:
                    pass

def exec_plan(code):
    """Main execution function, similar to pangea-js exec()"""
    global words, phrase_lengths, namespace
    
    debug_print("Executing code:", code)
    
    # Parse code into words
    new_words = parse_words(code)
    previous_length = len(words)
    words.extend(new_words)
    
    debug_print("Words:", words)
    
    # Pre-scan for function arities
    pre_scan_arities(new_words)
    
    # Setup operators if not already done
    if not namespace['operators']:
        setup_operators()
    
    # Initialize phrase lengths
    phrase_lengths = [None] * len(words)
    
    # Calculate phrase lengths
    for i in range(len(words)):
        phrase_length(i)
    
    debug_print("Phrase lengths:", phrase_lengths)
    
    # Execute the new code
    result = None
    if previous_length < len(words):
        result = word_exec(previous_length)
    
    return result

# Main evaluation function for compatibility with existing code
def evaluate_plan_words(plan_words):
    """Main entry point for plan evaluation"""
    global words
    
    # Reset state
    words = ["("]  # Start with opening paren like pangea-js
    namespace['stack'] = [{}]
    namespace['times_stack'] = []
    
    # Convert plan_words to string and execute
    code = " ".join(plan_words)
    code = f"( {code} )"  # Wrap in parentheses
    
    try:
        return exec_plan(code)
    except Exception as e:
        debug_print(f"ERROR during execution: {e}")
        print(f"ERROR: {e}")
        return None
