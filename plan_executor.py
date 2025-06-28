# plan executor

import sys
import plan_words_parsing
import plan_words_evaluation


# execute the plan
def execute_plan(plan_to_execute):
    plan_words = plan_words_parsing.words_parse(plan_to_execute)
    plan_words_evaluation.evaluate_plan(plan_words)


# entry point
if __name__ == "__main__":
    # check for command line arguments
    if len(sys.argv) > 1:
        plan_file = sys.argv[1]
    else:
        plan_file = "example_plans/testing.plan"
    
    # execute the plan
    try:
        with open(plan_file, 'r') as f:
            execute_plan(f.read())
    except FileNotFoundError:
        print(f"Error: Plan file '{plan_file}' not found.")
    except Exception as e:
        print(f"Error executing plan: {e}")
