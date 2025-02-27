# extract the words of a plan
def extract_words_from_plan(plan):

    # split the plan into words
    plan_words = []

    # split the plan into lines
    for line in plan.split("\n"):

        # remove leading and trailing whitespaces
        line = line.strip()

        # skip empty lines
        if line == "":
            continue

        # split the line into words
        words = line.split(" ")

        # remove empty words
        words = [word for word in words if word != ""]

        # check for comments
        if "#" in words:
            # remove the words after the comment
            words = words[: words.index("#")]

        # add the words to the plan
        plan_words.extend(words)

    # return the words of the plan
    return plan_words


# join the words of a string into a string
def join_string_words(plan_words):

    # join the words of a string into a string
    joined_plan_words = []  # joined words

    # check for strings
    in_string = False  # string flag
    # string accumulator
    string = ""
    # join the words of a string into a string
    for word in plan_words:

        # check for strings

        # start of a string
        if word[0] == '"' and in_string == False:
            # start of a string
            in_string = True
            string = word

            # check for a single word string
            if word[-1] == '"' and len(word) >= 2:
                # end of a string
                in_string = False
                joined_plan_words.append(string)

        # end of a string
        elif word[-1] == '"' and in_string == True:
            # end of a string
            in_string = False
            # add the string to the joined words
            string += " " + word
            joined_plan_words.append(string)

        # middle of a string
        elif in_string == True:
            # middle of a string
            # add the word to the string
            string += " " + word

        # normal word
        else:
            # normal word
            joined_plan_words.append(word)

    # return the joined words
    return joined_plan_words


def words_parse(plan_string):
    plan_words = extract_words_from_plan(plan_string)
    plan_words = join_string_words(plan_words)
    return plan_words
