# plan executor


import plan_words_parsing
import plan_words_evaluation


# execute the plan
def execute_plan(plan_to_execute):
    plan_words = plan_words_parsing.words_parse(plan_to_execute)
    plan_words_evaluation.evaluate_plan(plan_words)


# entry point
if __name__ == "__main__":
    # execute the plan
    execute_plan(open("example_plans/testing.plan").read())
