# Plan Language - Publication Ready Version
# A Domain Specific Language for structured execution

# Core evaluation system with boolean literals and basic operators

plan_eval_debug_flag = False

# Global state
function_registry = {}
times_count = 0
call_stack = []

# Operator definitions
infix_operators = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '%': lambda a, b: a % b,
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '<': lambda a, b: a < b,
    '>': lambda a, b: a > b,
    '<=': lambda a, b: a <= b,
    '>=': lambda a, b: a >= b,
}

def debug_print(*args):
    if plan_eval_debug_flag:
        print("debug:", *args)

def skip_block(plan_words, start_i):
    nested_level = 0
    current_i = start_i
    while current_i < len(plan_words):
        word = plan_words[current_i]
        if word == "{":
            nested_level += 1
        elif word == "}":
            nested_level -= 1
            if nested_level == 0:
                return current_i + 1
        current_i += 1
    return current_i

def evaluate_block(plan_words, start_i):
    evaluated_word = None
    current_i = start_i + 1
    while current_i < len(plan_words):
        word = plan_words[current_i]
        if word == "}":
            return evaluated_word, current_i + 1
        evaluated_word, current_i = evaluate_word(plan_words, current_i)
    return evaluated_word, current_i

def handle_infix_operator(plan_words, current_i):
    """Handle infix operators safely"""
    if current_i + 2 < len(plan_words):
        left_word = plan_words[current_i]
        operator = plan_words[current_i + 1]
        right_word = plan_words[current_i + 2]
        
        # Safe evaluation of operands
        try:
            left_val = eval(left_word) if left_word.replace('.', '').replace('-', '').isdigit() else left_word
        except:
            left_val = left_word
            
        try:
            right_val = eval(right_word) if right_word.replace('.', '').replace('-', '').isdigit() else right_word
        except:
            right_val = right_word
        
        if operator in infix_operators:
            try:
                result = infix_operators[operator](left_val, right_val)
                debug_print(f"Infix: {left_val} {operator} {right_val} = {result}")
                return result, current_i + 3
            except Exception as e:
                debug_print(f"Infix error: {e}")
    return None, None

def evaluate_word(plan_words, current_i):
    global times_count
    
    if current_i >= len(plan_words):
        return None, current_i
    
    word = plan_words[current_i]
    debug_print("evaluating:", word)
    next_i = current_i + 1
    
    # Boolean literals
    if word == "true":
        return True, next_i
    elif word == "false":
        return False, next_i
    
    # Basic output
    elif word == "writeln" or word == "write":
        if next_i < len(plan_words):
            value, next_i = evaluate_word(plan_words, next_i)
            end_char = "\n" if word == "writeln" else ""
            print(value, end=end_char)
            return value, next_i
        return None, next_i
    
    # Expression evaluation
    elif word == "eval":
        if next_i < len(plan_words):
            expr, next_i = evaluate_word(plan_words, next_i)
            try:
                return eval(str(expr)), next_i
            except:
                return expr, next_i
        return None, next_i
    
    # Conditionals
    elif word == "if":
        if next_i < len(plan_words):
            condition, next_i = evaluate_word(plan_words, next_i)
            if next_i < len(plan_words) and plan_words[next_i] == "{":
                if condition:
                    result, next_i = evaluate_block(plan_words, next_i)
                    return result, next_i
                else:
                    return None, skip_block(plan_words, next_i)
        return None, next_i
    
    # Loops
    elif word == "times":
        # Check for infix: N times { block }
        if current_i > 0:
            prev_word = plan_words[current_i - 1]
            if prev_word.isdigit() and next_i < len(plan_words) and plan_words[next_i] == "{":
                count = int(prev_word)
                old_times_count = times_count
                result = None
                for i in range(count):
                    times_count = i + 1
                    result, next_i = evaluate_block(plan_words, next_i)
                times_count = old_times_count
                return result, next_i
        
        # Prefix: times N { block }
        if next_i < len(plan_words):
            count, next_i = evaluate_word(plan_words, next_i)
            if isinstance(count, int) and next_i < len(plan_words) and plan_words[next_i] == "{":
                old_times_count = times_count
                result = None
                for i in range(count):
                    times_count = i + 1
                    result, next_i = evaluate_block(plan_words, next_i)
                times_count = old_times_count
                return result, next_i
        return None, next_i
    
    # Times counter
    elif word == "times_count":
        return times_count, next_i
    
    # Function definition
    elif word == "def":
        if next_i < len(plan_words):
            func_def = plan_words[next_i]
            next_i += 1
            if "#" in func_def:
                func_name, arg_count_str = func_def.split("#")
                arg_count = int(arg_count_str)
                
                # Read function body until next function keyword or control structure
                func_body = []
                while (next_i < len(plan_words) and 
                       plan_words[next_i] not in ["def", "times", "if", "writeln", "write", "print"] and
                       not plan_words[next_i] in function_registry):
                    if plan_words[next_i] == "{":
                        break
                    func_body.append(plan_words[next_i])
                    next_i += 1
                
                function_registry[func_name] = {
                    'arg_count': arg_count,
                    'body': func_body
                }
                debug_print(f"Defined function: {func_name} with body: {func_body}")
                return None, next_i
        return None, next_i
    
    # Function call check
    elif word in function_registry:
        func_def = function_registry[word]
        args = []
        for i in range(func_def['arg_count']):
            if next_i < len(plan_words):
                arg_value, next_i = evaluate_word(plan_words, next_i)
                args.append(arg_value)
        
        # Execute function body with arguments
        old_stack = call_stack.copy()
        call_stack.clear()
        call_stack.extend(args)
        
        result = None
        # Create a simple expression evaluator for function bodies
        func_body_str = ' '.join(func_def['body'])
        
        # Replace arg references
        for i in range(len(args)):
            func_body_str = func_body_str.replace(f'arg {i+1}', str(args[i]))
        
        # Try to evaluate as expression
        try:
            result = eval(func_body_str)
        except:
            # Fall back to simple parsing
            result = func_body_str
        
        call_stack.clear()
        call_stack.extend(old_stack)
        return result, next_i
    
    # Infix operator check
    elif current_i + 1 < len(plan_words) and plan_words[current_i + 1] in infix_operators:
        result, next_i = handle_infix_operator(plan_words, current_i)
        if result is not None:
            return result, next_i
    
    # Literals
    try:
        # Try to parse as number
        if word.replace('.', '').replace('-', '').isdigit():
            return eval(word), next_i
        # Try to parse as string
        elif word.startswith('"') and word.endswith('"'):
            return word[1:-1], next_i
        # Try to parse as other literal
        else:
            return eval(word), next_i
    except:
        # Unknown word
        debug_print(f"Unknown word: {word}")
        return word, next_i

def evaluate_plan(plan_words):
    """Main evaluation function"""
    current_i = 0
    while current_i < len(plan_words):
        try:
            _, current_i = evaluate_word(plan_words, current_i)
            if current_i is None:
                break
        except Exception as e:
            debug_print(f"Evaluation error: {e}")
            break

# Compatibility function for existing code
def handle_print_with_conditionals(plan_words, start_i):
    return start_i
