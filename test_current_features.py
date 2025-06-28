#!/usr/bin/env python3
"""
Test script to validate current Plan Language functionality
"""

import subprocess
import tempfile
import os

def test_plan(plan_code, description, should_succeed=True):
    """Test a piece of plan code"""
    print(f"\n{'='*50}")
    print(f"TEST: {description}")
    print(f"CODE:\n{plan_code}")
    print(f"{'='*50}")
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.plan', delete=False) as f:
        f.write(plan_code)
        temp_file = f.name
    
    try:
        # Run the plan
        result = subprocess.run(
            ['python3', 'plan_executor.py', temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print(f"EXIT CODE: {result.returncode}")
        if result.stdout:
            print(f"OUTPUT:\n{result.stdout}")
        if result.stderr:
            print(f"ERROR:\n{result.stderr}")
            
        success = result.returncode == 0
        if success == should_succeed:
            print("✅ PASS")
        else:
            print("❌ FAIL")
            
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT")
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
    finally:
        # Clean up temp file
        os.unlink(temp_file)

def main():
    print("🧪 Plan Language Feature Test Suite")
    print("Current working directory:", os.getcwd())
    
    # Test 1: Basic output
    test_plan(
        'writeln "Hello, World!"',
        "Basic string output"
    )
    
    # Test 2: Numbers
    test_plan(
        'writeln 42\nwriteln 3.14',
        "Number output"
    )
    
    # Test 3: Simple expressions
    test_plan(
        'writeln eval "2 + 3"',
        "Expression evaluation"
    )
    
    # Test 4: Basic loop
    test_plan(
        '3 times { writeln "Loop iteration" }',
        "Basic times loop"
    )
    
    # Test 5: Loop counter
    test_plan(
        '3 times { writeln times_count }',
        "Loop counter access"
    )
    
    # Test 6: Basic if
    test_plan(
        'if true { writeln "True branch" }',
        "Basic if statement"
    )
    
    # Test 7: If-else
    test_plan(
        'if false { writeln "False" } { writeln "True" }',
        "If-else statement"
    )
    
    # Test 8: Function definition (should parse but not execute)
    test_plan(
        'def test#1\narg 1\nwriteln "After function"',
        "Function definition parsing"
    )
    
    # Test 9: Function call (now working!)
    test_plan(
        'def add#2\narg 1 + arg 2\nwriteln add 5 3',
        "Function call",
        should_succeed=True
    )
    
    # Test 10: FizzBuzz excerpt (now working!)
    test_plan(
        '''def multiple#2
arg 1 % arg 2 == 0

def i#0
times_count 1

writeln multiple 6 2''',
        "FizzBuzz functions", 
        should_succeed=True
    )
    
    print(f"\n{'='*60}")
    print("TEST SUITE COMPLETE")
    print("Check individual test results above")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
