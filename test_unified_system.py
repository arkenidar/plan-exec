#!/usr/bin/env python3

# test_unified_system.py - Test the new unified operator and function system

import sys
sys.path.insert(0, '.')

from plan_words_evaluation_unified import exec_plan, debug_print, plan_eval_debug_flag

def test_unified_system():
    """Test the unified operator and function system"""
    global plan_eval_debug_flag
    plan_eval_debug_flag = True
    
    print("🧪 Testing Unified Plan Language System\n")
    
    # Test 1: Basic literals and output
    print("TEST 1: Basic output")
    try:
        exec_plan('writeln "Hello, World!"')
        exec_plan('writeln 42')
        print("✅ PASS\n")
    except Exception as e:
        print(f"❌ FAIL: {e}\n")
    
    # Test 2: Boolean literals
    print("TEST 2: Boolean literals")
    try:
        exec_plan('writeln true')
        exec_plan('writeln false')
        print("✅ PASS\n")
    except Exception as e:
        print(f"❌ FAIL: {e}\n")
    
    # Test 3: Arithmetic operations (infix)
    print("TEST 3: Arithmetic operations")
    try:
        exec_plan('writeln 3 + 4')
        exec_plan('writeln 10 - 3')
        exec_plan('writeln 5 * 6')
        print("✅ PASS\n")
    except Exception as e:
        print(f"❌ FAIL: {e}\n")
    
    # Test 4: Function definition and calling
    print("TEST 4: Function definition and calling")
    try:
        exec_plan('def add#2 ( arg 1 ) + ( arg 2 )')
        exec_plan('writeln add 5 3')
        print("✅ PASS\n")
    except Exception as e:
        print(f"❌ FAIL: {e}\n")
    
    # Test 5: Times loop with infix operator
    print("TEST 5: Times loop")
    try:
        exec_plan('3 times ( writeln "Loop iteration" )')
        print("✅ PASS\n")
    except Exception as e:
        print(f"❌ FAIL: {e}\n")
    
    # Test 6: Times counter
    print("TEST 6: Times counter")
    try:
        exec_plan('3 times ( writeln times_count 1 )')
        print("✅ PASS\n")
    except Exception as e:
        print(f"❌ FAIL: {e}\n")
    
    # Test 7: Conditionals with boolean literals
    print("TEST 7: Conditionals")
    try:
        exec_plan('if true ( writeln "True branch" ) ( writeln "False branch" )')
        exec_plan('if false ( writeln "True branch" ) ( writeln "False branch" )')
        print("✅ PASS\n")
    except Exception as e:
        print(f"❌ FAIL: {e}\n")

if __name__ == "__main__":
    test_unified_system()
