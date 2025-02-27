plan_eval_debug_flag = False


def debug_print(*args):
    global plan_eval_debug_flag
    if not plan_eval_debug_flag:
        return
    # debug print
    print("debug:", *args)


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

    elif word == "times":
        evaluated_word, next_i_after_1 = evaluate_word(plan_words, current_i + 1)
        times_count = evaluated_word
        for times_i in range(times_count):
            debug_print("times_i:", times_i)
            evaluated_word, next_i = evaluate_word(plan_words, next_i_after_1)
    else:
        try:
            evaluated_word = eval(word)
            debug_print("evaluated_word:", evaluated_word)

            if callable(evaluated_word):
                callable_word = evaluated_word
                evaluated_word, next_i = evaluate_word(plan_words, current_i + 1)
                evaluated_word = callable_word(evaluated_word)
                debug_print("evaluated_word:", evaluated_word)

        except:
            debug_print("Unknown word:", word)
            debug_print("Exiting...")
            evaluated_word = "Unknown word: " + word
            next_i = None  # exit

    # return the evaluated word and the next index
    return evaluated_word, next_i


def evaluate_plan(plan_words):
    current_i = 0
    while current_i != None and current_i < len(plan_words):
        evaluated_word, current_i = evaluate_word(plan_words, current_i)
