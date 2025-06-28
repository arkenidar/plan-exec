# Plan Language - Advanced Evaluator with Improved Namespacing
# Builds upon pangea-js unified namespace with practical improvements

from advanced_namespace import namespace_manager
from typing import List, Tuple, Any, Optional

plan_eval_debug_flag = False

def debug_print(*args):
    if plan_eval_debug_flag:
        print("debug:", *args)

def is_literal(word: str) -> bool:
    """Check if word is a literal value"""
    if word in ['true', 'false']:
        return True
    if word.startswith('"') and word.endswith('"'):
        return True
    try:
        float(word)
        return True
    except:
        return False

def parse_literal(word: str) -> Any:
    """Parse a literal value"""
    if word == 'true':
        return True
    elif word == 'false':
        return False
    elif word.startswith('"') and word.endswith('"'):
        return word[1:-1]
    else:
        try:
            if '.' in word:
                return float(word)
            else:
                return int(word)
        except:
            return word

def calculate_phrase_length(words: List[str], word_index: int) -> int:
    """Calculate phrase length (pangea-js style, improved)"""
    if word_index >= len(words):
        return 0
    
    # Extend phrase_lengths if needed
    phrase_lengths = namespace_manager.namespaces['meta']['phrase_lengths']
    while len(phrase_lengths) <= word_index:
        phrase_lengths.append(None)
    
    # Return cached result
    if phrase_lengths[word_index] is not None:
        return phrase_lengths[word_index]
    
    word = words[word_index]
    length = 1
    
    # Literals
    if is_literal(word):
        phrase_lengths[word_index] = 1
        return 1
    
    # Block structures
    if word in ['{', '[', '(']:
        closing = {'{': '}', '[': ']', '(': ')'}[word]
        current_index = word_index + 1
        while current_index < len(words) and words[current_index] != closing:
            current_index += calculate_phrase_length(words, current_index)
        length = current_index - word_index + 1
        phrase_lengths[word_index] = length
        return length
    
    # Get word info from namespace
    word_info = namespace_manager.lookup_word(word)
    
    if word_info:
        arity = word_info.get('arity', 0)
        
        # Handle variable arity (like print)
        if arity == -1:
            # Variable arity - consume until block or major keyword
            while word_index + length < len(words):
                next_word = words[word_index + length]
                if next_word in ['{', '}'] or namespace_manager.get_word_type(next_word) in ['control']:
                    break
                length += calculate_phrase_length(words, word_index + length)
        else:
            # Fixed arity
            for i in range(arity):
                next_index = word_index + length
                if next_index < len(words):
                    length += calculate_phrase_length(words, next_index)
    
    # Check for postfix/infix operators
    next_word_index = word_index + length
    if next_word_index < len(words):
        next_word = words[next_word_index]
        next_word_info = namespace_manager.lookup_word(next_word)
        
        if next_word_info and next_word_info.get('type') == 'operator':
            op_type = next_word_info.get('type')
            if op_type in ['postfix', 'infix']:
                op_arity = next_word_info.get('arity', 0)
                length += 1  # for the operator itself
                
                # For infix operators, add operands
                if op_type == 'infix':
                    for i in range(op_arity):
                        next_index = word_index + length
                        if next_index < len(words):
                            length += calculate_phrase_length(words, next_index)
    
    phrase_lengths[word_index] = length
    return length

def execute_word(words: List[str], word_index: int) -> Tuple[Any, int]:
    """Execute a word using the advanced namespace system"""
    if word_index >= len(words):
        return None, word_index
    
    word = words[word_index]
    debug_print(f"Executing: {word} at index {word_index}")
    
    # Check if it's a literal
    if is_literal(word):
        return parse_literal(word), word_index + 1
    
    # Look up word in namespace
    word_info = namespace_manager.lookup_word(word)
    
    if not word_info:
        debug_print(f"Unknown word: {word}")
        return word, word_index + 1
    
    word_type = word_info['type']
    
    # Handle different word types
    if word_type == 'literal':
        return word_info['value'], word_index + 1
    
    elif word_type == 'operator':
        return execute_operator(words, word_index, word_info)
    
    elif word_type == 'control':
        return execute_control_structure(words, word_index, word)
    
    elif word_type == 'user_function':
        return execute_user_function(words, word_index, word)
    
    elif word_type == 'function_definition':
        return execute_function_definition(words, word_index)
    
    else:
        debug_print(f"Unhandled word type: {word_type} for word: {word}")
        return word, word_index + 1

def execute_operator(words: List[str], word_index: int, op_info: dict) -> Tuple[Any, int]:
    """Execute an operator with proper precedence handling"""
    op_type = op_info.get('type', 'prefix')
    
    if op_type == 'infix':
        return execute_infix_operator(words, word_index, op_info)
    elif op_type == 'postfix':
        return execute_postfix_operator(words, word_index, op_info)
    else:  # prefix
        return execute_prefix_operator(words, word_index, op_info)

def execute_infix_operator(words: List[str], word_index: int, op_info: dict) -> Tuple[Any, int]:
    """Execute infix operator (improved from pangea-js)"""
    # This should be called when we're at the left operand
    # The operator is at word_index + 1
    
    if word_index + 1 >= len(words):
        return None, word_index + 1
    
    operator_word = words[word_index + 1]
    if operator_word not in namespace_manager.namespaces['core']['operators']:
        return None, word_index + 1
    
    # Get left operand
    left_val, _ = execute_word(words, word_index)
    
    # Get operator info
    op_info = namespace_manager.namespaces['core']['operators'][operator_word]
    arity = op_info['arity']
    op_func = op_info['func']
    
    # Get right operand(s)
    next_i = word_index + 2
    args = [left_val]
    
    for i in range(arity):
        if next_i < len(words):
            arg_val, next_i = execute_word(words, next_i)
            args.append(arg_val)
    
    # Execute operator
    try:
        result = op_func(*args)
        debug_print(f"Infix operation: {args[0]} {operator_word} {args[1:]} = {result}")
        return result, next_i
    except Exception as e:
        debug_print(f"Operator error: {e}")
        return None, next_i

def execute_control_structure(words: List[str], word_index: int, word: str) -> Tuple[Any, int]:
    """Execute control structures with improved handling"""
    
    if word in ['writeln', 'write']:
        if word_index + 1 < len(words):
            value, next_i = execute_word(words, word_index + 1)
            end_char = '\n' if word == 'writeln' else ''
            print(value, end=end_char)
            return value, next_i
        return None, word_index + 1
    
    elif word == 'print':
        return execute_multiline_print(words, word_index)
    
    elif word == 'eval':
        if word_index + 1 < len(words):
            expr, next_i = execute_word(words, word_index + 1)
            try:
                return eval(str(expr)), next_i
            except:
                return expr, next_i
        return None, word_index + 1
    
    elif word == 'if':
        return execute_conditional(words, word_index)
    
    elif word == 'times':
        return execute_times_loop(words, word_index)
    
    elif word == 'times_count':
        if word_index + 1 < len(words):
            depth, next_i = execute_word(words, word_index + 1)
            return namespace_manager.get_loop_counter(depth), next_i
        return namespace_manager.get_loop_counter(1), word_index + 1
    
    elif word == 'arg':
        if word_index + 1 < len(words):
            arg_num, next_i = execute_word(words, word_index + 1)
            call_stack = namespace_manager.namespaces['runtime']['call_stack']
            if call_stack and 'args' in call_stack[-1] and arg_num <= len(call_stack[-1]['args']):
                return call_stack[-1]['args'][arg_num - 1], next_i
        return None, word_index + 1
    
    else:
        debug_print(f"Unhandled control structure: {word}")
        return None, word_index + 1

def execute_multiline_print(words: List[str], word_index: int) -> Tuple[Any, int]:
    """Execute multi-line print with when expressions (pangea-js style)"""
    result_values = []
    current_i = word_index + 1
    
    # Collect all expressions until block end or major keyword
    while current_i < len(words):
        word = words[current_i]
        
        # Stop at major keywords or block endings
        if word in ['}', 'def', 'times', 'if'] or namespace_manager.get_word_type(word) == 'control':
            break
        
        # Execute the expression
        value, current_i = execute_word(words, current_i)
        if value is not None:
            result_values.append(value)
    
    # Print the first non-None value (pangea-js behavior)
    if result_values:
        print(result_values[0])
        return result_values[0], current_i
    
    return None, current_i

def execute_conditional(words: List[str], word_index: int) -> Tuple[Any, int]:
    """Execute if statement"""
    if word_index + 1 >= len(words):
        return None, word_index + 1
    
    condition, next_i = execute_word(words, word_index + 1)
    
    if next_i < len(words) and words[next_i] == '{':
        if condition:
            result, next_i = execute_code_block(words, next_i)
            return result, next_i
        else:
            # Skip the true block
            next_i = skip_to_matching_brace(words, next_i) + 1
            # Check for else block
            if next_i < len(words) and words[next_i] == '{':
                result, next_i = execute_code_block(words, next_i)
                return result, next_i
            return None, next_i
    
    return None, next_i

def execute_times_loop(words: List[str], word_index: int) -> Tuple[Any, int]:
    """Execute times loop with improved stack management"""
    # Check for infix: N times { block }
    if word_index > 0 and words[word_index - 1].isdigit():
        count = int(words[word_index - 1])
        next_i = word_index + 1
        if next_i < len(words) and words[next_i] == '{':
            return execute_times_with_count(words, next_i, count)
    
    # Prefix: times N { block }
    if word_index + 1 < len(words):
        count, next_i = execute_word(words, word_index + 1)
        if isinstance(count, int) and next_i < len(words) and words[next_i] == '{':
            return execute_times_with_count(words, next_i, count)
    
    return None, word_index + 1

def execute_times_with_count(words: List[str], block_start: int, count: int) -> Tuple[Any, int]:
    """Execute times loop with proper stack management"""
    namespace_manager.push_loop_context()
    result = None
    
    try:
        for i in range(count):
            namespace_manager.update_loop_counter(i + 1)
            debug_print(f"Loop iteration {i + 1}")
            result, _ = execute_code_block(words, block_start)
    finally:
        namespace_manager.pop_loop_context()
    
    return result, skip_to_matching_brace(words, block_start) + 1

def execute_function_definition(words: List[str], word_index: int) -> Tuple[Any, int]:
    """Execute function definition using namespace manager"""
    if word_index + 1 >= len(words):
        return None, word_index + 1
    
    func_def = words[word_index + 1]
    next_i = word_index + 2
    
    if '#' in func_def:
        func_name, arg_count_str = func_def.split('#')
        arg_count = int(arg_count_str)
        
        # Read function body until next major keyword
        func_body = []
        while (next_i < len(words) and 
               words[next_i] not in ['def', 'times', 'if', 'writeln', 'write', 'print'] and
               words[next_i] not in namespace_manager.namespaces['user']['functions']):
            if words[next_i] == '{':
                break
            func_body.append(words[next_i])
            next_i += 1
        
        # Use namespace manager to define function
        namespace_manager.define_function(func_name, arg_count, func_body)
        debug_print(f"Defined function: {func_name}#{arg_count}: {func_body}")
        return None, next_i
    
    return None, next_i

def execute_user_function(words: List[str], word_index: int, func_name: str) -> Tuple[Any, int]:
    """Execute user-defined function using namespace manager"""
    func_info = namespace_manager.namespaces['user']['functions'][func_name]
    arity = func_info['arity']
    
    # Collect arguments
    args = []
    next_i = word_index + 1
    for i in range(arity):
        if next_i < len(words):
            arg_val, next_i = execute_word(words, next_i)
            args.append(arg_val)
    
    # Use namespace manager to call function
    try:
        result = namespace_manager.call_function(func_name, args)
        debug_print(f"Function call: {func_name}({args}) = {result}")
        return result, next_i
    except Exception as e:
        debug_print(f"Function call error: {e}")
        return None, next_i

def execute_code_block(words: List[str], word_index: int) -> Tuple[Any, int]:
    """Execute code block {...}"""
    result = None
    current_i = word_index + 1
    while current_i < len(words) and words[current_i] != '}':
        result, current_i = execute_word(words, current_i)
    return result, current_i + 1

def skip_to_matching_brace(words: List[str], start_index: int) -> int:
    """Skip to matching closing brace"""
    if start_index >= len(words) or words[start_index] != '{':
        return start_index
    
    level = 0
    current_i = start_index
    while current_i < len(words):
        if words[current_i] == '{':
            level += 1
        elif words[current_i] == '}':
            level -= 1
            if level == 0:
                return current_i
        current_i += 1
    return current_i

def evaluate_plan_advanced(words: List[str]):
    """Main evaluation function with advanced namespace system"""
    # Reset namespace for clean execution
    namespace_manager.reset()
    
    # Pre-calculate phrase lengths
    namespace_manager.namespaces['meta']['phrase_lengths'] = [None] * len(words)
    for i in range(len(words)):
        if namespace_manager.namespaces['meta']['phrase_lengths'][i] is None:
            calculate_phrase_length(words, i)
    
    debug_print(f"Phrase lengths: {namespace_manager.namespaces['meta']['phrase_lengths']}")
    
    # Execute the program
    current_i = 0
    while current_i < len(words):
        try:
            result, current_i = execute_word(words, current_i)
            if current_i is None:
                break
        except Exception as e:
            debug_print(f"Execution error: {e}")
            break
    
    if plan_eval_debug_flag:
        print("\n" + namespace_manager.debug_dump())

# Compatibility functions
def evaluate_plan(words: List[str]):
    """Compatibility wrapper for existing code"""
    return evaluate_plan_advanced(words)

def debug_set_flag(flag: bool):
    """Set debug flag"""
    global plan_eval_debug_flag
    plan_eval_debug_flag = flag
