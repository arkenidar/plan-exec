# Plan Language - Enhanced Version Inspired by Pangea-js
# Unified operator system with phrase length calculation and improved context management

plan_eval_debug_flag = False

# Core namespace system (pangea-js inspired)
namespace = {
    'functions': {},      # User-defined functions
    'operators': {},      # Operators (prefix, infix, postfix)
    'stack': [{}],        # Function call stack
    'times_stack': [],    # Loop counter stack
    'phrase_lengths': []  # Pre-calculated phrase boundaries
}

def debug_print(*args):
    if plan_eval_debug_flag:
        print("debug:", *args)

# Phrase length calculation (pangea-js core innovation)
def calculate_phrase_length(words, word_index):
    """Calculate the length of a phrase starting at word_index"""
    if word_index >= len(words):
        return 0
    
    # Check if already calculated
    if word_index < len(namespace['phrase_lengths']) and namespace['phrase_lengths'][word_index] is not None:
        return namespace['phrase_lengths'][word_index]
    
    # Extend phrase_lengths array if needed
    while len(namespace['phrase_lengths']) <= word_index:
        namespace['phrase_lengths'].append(None)
    
    word = words[word_index]
    length = 1
    
    # Literals (numbers, strings, booleans)
    if is_literal(word):
        namespace['phrase_lengths'][word_index] = 1
        return 1
    
    # Block structures
    if word in ['{', '[', '(']:
        closing = {'{': '}', '[': ']', '(': ')'}[word]
        current_index = word_index + 1
        while current_index < len(words) and words[current_index] != closing:
            current_index += calculate_phrase_length(words, current_index)
        length = current_index - word_index + 1
        namespace['phrase_lengths'][word_index] = length
        return length
    
    # Functions and operators
    arity = get_word_arity(word)
    if arity is not None:
        for i in range(arity):
            next_index = word_index + length
            if next_index < len(words):
                length += calculate_phrase_length(words, next_index)
    
    # Check for postfix/infix operators
    next_word_index = word_index + length
    if next_word_index < len(words):
        next_word = words[next_word_index]
        if is_operator(next_word) and get_operator_type(next_word) in ['postfix', 'infix']:
            op_arity = get_word_arity(next_word)
            length += 1  # for the operator itself
            if get_operator_type(next_word) == 'infix' and op_arity:
                for i in range(op_arity):
                    next_index = word_index + length
                    if next_index < len(words):
                        length += calculate_phrase_length(words, next_index)
    
    namespace['phrase_lengths'][word_index] = length
    return length

def is_literal(word):
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

def get_word_arity(word):
    """Get the arity of a word (how many arguments it takes)"""
    # Function definitions with #
    if '#' in word and not word.startswith('"'):
        return 0  # Function definitions take no arguments during definition
    
    # Built-in operators
    if word in namespace['operators']:
        return namespace['operators'][word]['arity']
    
    # User-defined functions
    func_name = word.split('#')[0] if '#' in word else word
    if func_name in namespace['functions']:
        return namespace['functions'][func_name]['arity']
    
    # Built-in functions
    builtin_arities = {
        'writeln': 1, 'write': 1, 'print': 1, 'eval': 1,
        'if': 2, 'times': 1, 'def': 2,
        'arg': 1, 'times_count': 0
    }
    
    return builtin_arities.get(word)

def is_operator(word):
    """Check if word is an operator"""
    return word in namespace['operators']

def get_operator_type(word):
    """Get operator type: prefix, infix, or postfix"""
    if word in namespace['operators']:
        return namespace['operators'][word]['type']
    return 'prefix'  # default

# Initialize operators (pangea-js style)
def init_operators():
    """Initialize the operator namespace"""
    operators = {
        # Arithmetic operators (infix)
        '+': {'type': 'infix', 'arity': 1, 'func': lambda a, b: a + b},
        '-': {'type': 'infix', 'arity': 1, 'func': lambda a, b: a - b},
        '*': {'type': 'infix', 'arity': 1, 'func': lambda a, b: a * b},
        '/': {'type': 'infix', 'arity': 1, 'func': lambda a, b: a / b},
        '%': {'type': 'infix', 'arity': 1, 'func': lambda a, b: a % b},
        
        # Comparison operators (infix)
        '==': {'type': 'infix', 'arity': 1, 'func': lambda a, b: a == b},
        '!=': {'type': 'infix', 'arity': 1, 'func': lambda a, b: a != b},
        '<': {'type': 'infix', 'arity': 1, 'func': lambda a, b: a < b},
        '>': {'type': 'infix', 'arity': 1, 'func': lambda a, b: a > b},
        '<=': {'type': 'infix', 'arity': 1, 'func': lambda a, b: a <= b},
        '>=': {'type': 'infix', 'arity': 1, 'func': lambda a, b: a >= b},
        
        # Special operators
        'when': {'type': 'infix', 'arity': 2, 'func': lambda val, cond, alt=None: val if cond else alt},
    }
    
    namespace['operators'] = operators

# Enhanced word execution (pangea-js inspired)
def execute_word(words, word_index):
    """Execute a word and return (result, next_index)"""
    if word_index >= len(words):
        return None, word_index
    
    word = words[word_index]
    debug_print(f"Executing: {word} at index {word_index}")
    
    # Boolean literals
    if word == 'true':
        return True, word_index + 1
    elif word == 'false':
        return False, word_index + 1
    
    # String literals
    elif word.startswith('"') and word.endswith('"'):
        return word[1:-1], word_index + 1
    
    # Number literals
    elif is_literal(word) and word not in ['true', 'false']:
        try:
            if '.' in word:
                return float(word), word_index + 1
            else:
                return int(word), word_index + 1
        except:
            return word, word_index + 1
    
    # Check for infix operators first (pangea-js style)
    next_index = word_index + calculate_phrase_length(words, word_index)
    if next_index - 1 > word_index and next_index - 1 < len(words):
        potential_op = words[word_index + 1]
        if is_operator(potential_op) and get_operator_type(potential_op) == 'infix':
            return execute_infix_operation(words, word_index)
    
    # Block structures
    elif word == '(':
        return execute_block(words, word_index, ')')
    elif word == '[':
        return execute_array(words, word_index)
    elif word == '{':
        return execute_code_block(words, word_index)
    
    # Built-in functions
    elif word in ['writeln', 'write']:
        if word_index + 1 < len(words):
            value, next_i = execute_word(words, word_index + 1)
            end_char = '\n' if word == 'writeln' else ''
            print(value, end=end_char)
            return value, next_i
        return None, word_index + 1
    
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
        stack = namespace['times_stack']
        return stack[-1] if stack else 0, word_index + 1
    
    elif word == 'def':
        return execute_function_definition(words, word_index)
    
    elif word == 'arg':
        if word_index + 1 < len(words):
            arg_num, next_i = execute_word(words, word_index + 1)
            stack = namespace['stack']
            if stack and 'args' in stack[-1] and arg_num <= len(stack[-1]['args']):
                return stack[-1]['args'][arg_num - 1], next_i
        return None, word_index + 1
    
    # User-defined function calls
    elif word in namespace['functions']:
        return execute_function_call(words, word_index)
    
    # Unknown word
    else:
        debug_print(f"Unknown word: {word}")
        return word, word_index + 1

def execute_infix_operation(words, word_index):
    """Execute infix operation (pangea-js style)"""
    left_val, _ = execute_word(words, word_index)
    operator = words[word_index + 1]
    right_start = word_index + 2
    right_val, next_i = execute_word(words, right_start)
    
    if operator in namespace['operators']:
        op_func = namespace['operators'][operator]['func']
        result = op_func(left_val, right_val)
        debug_print(f"Infix: {left_val} {operator} {right_val} = {result}")
        return result, next_i
    
    return None, next_i

def execute_block(words, word_index, closing_char):
    """Execute a parentheses block"""
    result = None
    current_i = word_index + 1
    while current_i < len(words) and words[current_i] != closing_char:
        result, current_i = execute_word(words, current_i)
    return result, current_i + 1

def execute_array(words, word_index):
    """Execute array literal [...]"""
    result = []
    current_i = word_index + 1
    while current_i < len(words) and words[current_i] != ']':
        element, current_i = execute_word(words, current_i)
        result.append(element)
    return result, current_i + 1

def execute_code_block(words, word_index):
    """Execute code block {...}"""
    result = None
    current_i = word_index + 1
    while current_i < len(words) and words[current_i] != '}':
        result, current_i = execute_word(words, current_i)
    return result, current_i + 1

def execute_conditional(words, word_index):
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

def execute_times_loop(words, word_index):
    """Execute times loop with stack-based counter"""
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

def execute_times_with_count(words, block_start, count):
    """Execute times loop with proper stack management"""
    namespace['times_stack'].append(1)
    result = None
    
    try:
        for i in range(count):
            namespace['times_stack'][-1] = i + 1
            result, _ = execute_code_block(words, block_start)
    finally:
        namespace['times_stack'].pop()
    
    return result, skip_to_matching_brace(words, block_start) + 1

def execute_function_definition(words, word_index):
    """Execute function definition"""
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
               words[next_i] not in namespace['functions']):
            if words[next_i] == '{':
                break
            func_body.append(words[next_i])
            next_i += 1
        
        namespace['functions'][func_name] = {
            'arity': arg_count,
            'body': func_body
        }
        debug_print(f"Defined function: {func_name} with arity {arg_count}")
        return None, next_i
    
    return None, next_i

def execute_function_call(words, word_index):
    """Execute user-defined function call with proper context"""
    func_name = words[word_index]
    func_def = namespace['functions'][func_name]
    
    # Collect arguments
    args = []
    next_i = word_index + 1
    for i in range(func_def['arity']):
        if next_i < len(words):
            arg_val, next_i = execute_word(words, next_i)
            args.append(arg_val)
    
    # Execute function with new context
    namespace['stack'].append({'args': args})
    
    try:
        # Enhanced function body execution with proper expression evaluation
        func_body_str = ' '.join(func_def['body'])
        
        # Replace arg references
        for i in range(len(args)):
            func_body_str = func_body_str.replace(f'arg {i+1}', str(args[i]))
        
        # Try to evaluate as expression
        try:
            result = eval(func_body_str)
        except:
            # Fall back to word-by-word execution
            result = None
            body_words = func_def['body']
            for word in body_words:
                if word == 'arg':
                    continue  # Skip arg keywords in simple execution
                result = word
    finally:
        namespace['stack'].pop()
    
    return result, next_i

def skip_to_matching_brace(words, start_index):
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

def evaluate_plan_enhanced(words):
    """Main evaluation function with phrase length pre-calculation"""
    # Initialize operators
    init_operators()
    
    # Reset phrase lengths
    namespace['phrase_lengths'] = [None] * len(words)
    
    # Pre-calculate phrase lengths for all words
    for i in range(len(words)):
        if namespace['phrase_lengths'][i] is None:
            calculate_phrase_length(words, i)
    
    debug_print(f"Phrase lengths: {namespace['phrase_lengths']}")
    
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

# Compatibility functions
def evaluate_plan(words):
    """Compatibility wrapper"""
    return evaluate_plan_enhanced(words)

def debug_set_flag(flag):
    """Set debug flag"""
    global plan_eval_debug_flag
    plan_eval_debug_flag = flag
