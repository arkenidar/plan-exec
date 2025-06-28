# description: This module contains the functions to evaluate the plan words

# plan_words_evaluation.py

# debugging related

plan_eval_debug_flag = False

# function registry and global variables
function_registry = {}
global_variables = {}
times_count = 0  # global variable for tracking loop iterations


def debug_print(*args):
    global plan_eval_debug_flag
    if not plan_eval_debug_flag:
        return
    # debug print
    print("debug:", *args)


# code-blocks handling


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
                next_i = current_i + 1
                return next_i
        current_i += 1


def evaluate_block(plan_words, start_i):
    evaluated_word = None
    current_i = start_i + 1
    while current_i < len(plan_words):
        word = plan_words[current_i]
        if word == "}":
            next_i = current_i + 1
            return evaluated_word, next_i
        evaluated_word, current_i = evaluate_word(plan_words, current_i)


def evaluate_word(plan_words, current_i):
    global times_count  # Declare global at the top of function
    
    evaluated_word = None
    next_i = None

    word = plan_words[current_i]
    debug_print("word:", word)
    next_i = current_i + 1

    if word == "pass":
        next_i = current_i + 1
        evaluated_word = None

    elif word == "def":
        # Handle function definition: def function_name#arg_count
        if next_i < len(plan_words):
            func_def = plan_words[next_i]
            next_i += 1
            
            if "#" in func_def:
                func_name, arg_count_str = func_def.split("#")
                arg_count = int(arg_count_str)
                
                # Read function body until we hit another def, times, if, or end of file
                func_body = []
                while next_i < len(plan_words) and plan_words[next_i] not in ["def", "times", "if", "if-else"]:
                    if plan_words[next_i] == "{":
                        # If we hit a block, we've gone too far
                        break
                    func_body.append(plan_words[next_i])
                    next_i += 1
                
                function_registry[func_name] = {
                    'arg_count': arg_count,
                    'body': func_body
                }
                debug_print(f"Defined function: {func_name} with {arg_count} args, body: {func_body}")
                evaluated_word = None
            else:
                print(f"ERROR: Invalid function definition format: {func_def}")
                evaluated_word = "ERROR: Invalid function definition format"
                next_i = None
        else:
            print("ERROR: Missing function name after def")
            evaluated_word = "ERROR: Missing function name after def"
            next_i = None

    elif word == "arg":
        # Handle function arguments: arg 1, arg 2, etc.
        arg_num, next_i = evaluate_word(plan_words, current_i + 1)
        if hasattr(evaluate_word, 'current_args') and arg_num <= len(evaluate_word.current_args):
            evaluated_word = evaluate_word.current_args[arg_num - 1]
        else:
            evaluated_word = f"arg_{arg_num}"  # fallback
        debug_print(f"Retrieved argument {arg_num}: {evaluated_word}")

    elif word == "times_count":
        evaluated_word = times_count
        debug_print(f"times_count: {evaluated_word}")

    elif word == "print":
        # Handle print with conditional expressions
        next_i = handle_print_with_conditionals(plan_words, current_i + 1)
        evaluated_word = None

    elif word == "eval":
        evaluated_word, next_i = evaluate_word(plan_words, current_i + 1)
        evaluated_word = eval(evaluated_word)

    elif word == "write" or word == "writeln":
        evaluated_word, next_i = evaluate_word(plan_words, current_i + 1)
        end_line = {"write": "", "writeln": "\n"}[word]
        print(evaluated_word, end=end_line)

    elif word == "if" or word == "if-else":
        condition, next_i = evaluate_word(plan_words, next_i)
        debug_print("condition:", condition)
        if condition == True:
            evaluated_word, next_i = evaluate_block(plan_words, next_i)
            if word == "if-else":
                next_i = skip_block(plan_words, next_i)
        elif condition == False:
            next_i = skip_block(plan_words, next_i)
            if word == "if-else":
                evaluated_word, next_i = evaluate_block(plan_words, next_i)
        else:
            print("ERROR: condition must be a boolean value")
            debug_print("Exiting...")
            evaluated_word = "ERROR: condition must be a boolean value"
            next_i = None

    elif word == "times":
        # evaluate the times count
        evaluated_word, next_i_block_start = evaluate_word(plan_words, next_i)
        loop_count = evaluated_word
        assert type(loop_count) is int, "ERROR: times_count value must be an integer"
        # check the block start
        assert plan_words[next_i_block_start] == "{"  # block start
        
        old_times_count = times_count
        
        for times_i in range(loop_count):
            times_count = times_i + 1  # Update global counter (1-based)
            debug_print("times_i:", times_i, "times_count:", times_count)
            # evaluate the block
            evaluated_word, next_i = evaluate_block(plan_words, next_i_block_start)
            debug_print("evaluated_word:", evaluated_word)
        
        times_count = old_times_count  # Restore previous counter
        
        if loop_count <= 0:
            # skip the block
            next_i = skip_block(plan_words, next_i_block_start)
    else:
        # Check if it's a user-defined function first
        if word in function_registry:
            # It's a function call - collect arguments if any
            args = []
            temp_next_i = next_i
            func_def = function_registry[word]
            expected_args = func_def['arg_count']
            
            # Collect the expected number of arguments
            for _ in range(expected_args):
                if temp_next_i < len(plan_words):
                    arg_word = plan_words[temp_next_i]
                    try:
                        # Try to evaluate the argument
                        if arg_word.isdigit():
                            args.append(int(arg_word))
                        elif arg_word in function_registry:
                            args.append(call_function(arg_word, []))
                        else:
                            arg_val, _ = evaluate_word(plan_words, temp_next_i)
                            args.append(arg_val)
                    except:
                        args.append(arg_word)
                    temp_next_i += 1
            
            next_i = temp_next_i
            evaluated_word = call_function(word, args)
            debug_print(f"Function call {word}({args}) = {evaluated_word}")
        
        else:
            try:
                # try to evaluate the word
                evaluated_word = eval(word)
                debug_print("evaluated_word:", evaluated_word)

                if callable(evaluated_word):
                    callable_word = evaluated_word
                    evaluated_word, next_i = evaluate_word(plan_words, current_i + 1)
                    evaluated_word = callable_word(evaluated_word)
                    debug_print("evaluated_word:", evaluated_word)

            except:
                print("ERROR: Unknown word:", word)
                debug_print("Exiting...")
                evaluated_word = "Unknown word: " + word
                next_i = None  # exit
            next_i = None  # exit

    # return the evaluated word and the next index
    return evaluated_word, next_i


def evaluate_plan(plan_words):
    current_i = 0
    while current_i != None and current_i < len(plan_words):
        evaluated_word, current_i = evaluate_word(plan_words, current_i)


# code-blocks handling

def handle_print_with_conditionals(plan_words, start_i):
    """Handle print statements with 'when' conditionals"""
    current_i = start_i
    printed = False
    
    while current_i < len(plan_words):
        word = plan_words[current_i]
        
        if word in ["def", "times", "if", "if-else"]:
            # We've hit the next statement
            break
            
        if word == "when":
            # Parse: "value" when condition
            if current_i >= 2:
                value = plan_words[current_i - 1]
                condition_start = current_i + 1
                
                # Evaluate the condition (simple case - function call)
                if condition_start < len(plan_words):
                    condition_word = plan_words[condition_start]
                    condition_arg = None
                    if condition_start + 1 < len(plan_words):
                        try:
                            condition_arg = int(plan_words[condition_start + 1])
                        except:
                            condition_arg = plan_words[condition_start + 1]
                    
                    # Call the function with the argument
                    if condition_word in function_registry:
                        result = call_function(condition_word, [condition_arg] if condition_arg is not None else [])
                        if result:
                            print(value.strip('"'))
                            printed = True
                            current_i += 2  # skip condition and argument
                            continue
            current_i += 1
        else:
            # If it's not a conditional, it might be a direct value to print
            if not printed and word not in ["when"] and current_i == start_i:
                # Print the value directly
                if word in function_registry:
                    result = call_function(word, [])
                    print(result)
                else:
                    try:
                        # Try to evaluate as a literal
                        value = eval(word) if word.isdigit() else word.strip('"')
                        print(value)
                    except:
                        print(word)
                printed = True
            current_i += 1
    
    return current_i

def call_function(func_name, args):
    """Call a user-defined function"""
    global times_count
    
    if func_name not in function_registry:
        return None
    
    func_def = function_registry[func_name]
    expected_args = func_def['arg_count']
    
    if len(args) != expected_args:
        debug_print(f"Warning: Function {func_name} expects {expected_args} args, got {len(args)}")
    
    # Set up function arguments
    old_args = getattr(call_function, 'current_args', None)
    call_function.current_args = args
    
    # Special handling for built-in variables
    if func_name == "i":
        result = times_count
    else:
        # Execute function body
        result = None
        for word in func_def['body']:
            if word == "times_count":
                result = times_count
            elif word in function_registry:
                result = call_function(word, [])
            elif word.startswith("arg"):
                try:
                    arg_num = int(word.split()[1])
                    if arg_num <= len(args):
                        result = args[arg_num - 1]
                except:
                    pass
            else:
                # Try to evaluate the expression
                try:
                    # Replace function calls in the expression
                    expr = word
                    for other_func in function_registry:
                        if other_func in expr:
                            func_result = call_function(other_func, [])
                            expr = expr.replace(other_func, str(func_result))
                    
                    # Replace arg references
                    for i, arg in enumerate(args):
                        expr = expr.replace(f"arg {i+1}", str(arg))
                    
                    result = eval(expr)
                except:
                    result = word
    
    # Restore previous arguments
    if old_args is not None:
        call_function.current_args = old_args
    elif hasattr(call_function, 'current_args'):
        delattr(call_function, 'current_args')
    
    debug_print(f"Function {func_name}({args}) = {result}")
    return result
