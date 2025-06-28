#!/usr/bin/env python3

# Minimal test to check if our boolean literals work
import sys
sys.path.insert(0, '.')

try:
    from plan_words_evaluation import evaluate_word
    
    # Test boolean evaluation directly
    plan_words = ['true']
    result, next_i = evaluate_word(plan_words, 0)
    print(f"true -> {result} (type: {type(result)})")
    
    plan_words = ['false']
    result, next_i = evaluate_word(plan_words, 0)
    print(f"false -> {result} (type: {type(result)})")
    
    # Test if statement with boolean
    plan_words = ['if', 'true', '{', 'writeln', '"test"', '}']
    print("Testing if statement...")
    result, next_i = evaluate_word(plan_words, 0)
    print(f"if statement result: {result}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
