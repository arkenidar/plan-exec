#!/usr/bin/env python3
"""
Test the current evaluator with original user-authored plan files
"""

import plan_words_parsing
import plan_words_evaluation
import traceback

def test_plan_file(filepath):
    print(f"\n{'='*50}")
    print(f"Testing: {filepath}")
    print('='*50)
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        print("Plan content:")
        print(content[:300] + ("..." if len(content) > 300 else ""))
        print()
        
        plan_words = plan_words_parsing.words_parse(content)
        print(f"Parsed {len(plan_words)} words")
        print()
        
        print("Executing plan...")
        result = plan_words_evaluation.evaluate_plan(plan_words)
        print(f"\nExecution completed. Result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

def main():
    print("Testing Plan Language with original user files")
    
    # Test files in order of complexity
    test_files = [
        "js_version/user_sample.plan",
        "example_plans/testing.plan", 
        "example_plans/fizzbuzz.plan"
    ]
    
    for test_file in test_files:
        test_plan_file(test_file)
    
    print(f"\n{'='*50}")
    print("All tests completed")
    print('='*50)

if __name__ == "__main__":
    main()
