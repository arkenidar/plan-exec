# description: This module contains the functions to evaluate the plan words

# plan_words_evaluation.py

# debugging related

plan_eval_debug_flag = False


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

    evaluated_word = None
    next_i = None

    word = plan_words[current_i]
    debug_print("word:", word)
    next_i = current_i + 1

    if word == "pass":
        next_i = current_i + 1
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
        times_count = evaluated_word
        assert type(times_count) is int, "ERROR: times_count value must be an integer"
        # check the block start
        assert plan_words[next_i_block_start] == "{"  # block start
        for times_i in range(times_count):
            debug_print("times_i:", times_i)
            # evaluate the block
            evaluated_word, next_i = evaluate_block(plan_words, next_i_block_start)
            debug_print("evaluated_word:", evaluated_word)
        if times_count <= 0:
            # skip the block
            next_i = skip_block(plan_words, next_i_block_start)
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

    # return the evaluated word and the next index
    return evaluated_word, next_i


def evaluate_plan(plan_words):
    current_i = 0
    while current_i != None and current_i < len(plan_words):
        evaluated_word, current_i = evaluate_word(plan_words, current_i)
