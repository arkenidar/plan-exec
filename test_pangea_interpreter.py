#!/usr/bin/env python3
"""
Test script for the Pangea Python Interpreter
"""

from pangea_python_interpreter import PangeaInterpreter


def test_basic_operations():
    """Test basic operations"""
    print("=== Testing Basic Operations ===")
    interpreter = PangeaInterpreter()
    
    # Basic arithmetic
    interpreter.exec('print 3 + 4')
    interpreter.exec('print 10 - 3')
    interpreter.exec('print 5 * 6')
    interpreter.exec('print 2 ** 3')
    
    # Postfix operator
    interpreter.exec('print 5 squared')
    
    # Boolean operations
    interpreter.exec('print 5 > 3')
    interpreter.exec('print 2 == 2')


def test_control_flow():
    """Test control flow constructs"""
    print("\n=== Testing Control Flow ===")
    interpreter = PangeaInterpreter()
    
    # If statement
    interpreter.exec('if true print "condition+is+true" print "never+printed"')
    interpreter.exec('if false print "never+printed" print "condition+is+false"')
    
    # Times loop
    interpreter.exec('3 times print "loop+iteration"')
    
    # When (ternary operator)
    interpreter.exec('print "yes" when true')
    interpreter.exec('print "no" when false')


def test_data_structures():
    """Test arrays and objects"""
    print("\n=== Testing Data Structures ===")
    interpreter = PangeaInterpreter()
    
    # Arrays
    interpreter.exec('print [ 1 2 3 4 5 ]')
    
    # Objects
    interpreter.exec('print { "name" "John" "age" 30 "city" "New+York" }')


def test_functions():
    """Test function definitions and calls"""
    print("\n=== Testing Functions ===")
    interpreter = PangeaInterpreter()
    
    # Simple function
    interpreter.exec('''
    def greet#1 (
        print "Hello," 
        print arg 1
    )
    greet "World"
    ''')
    
    # Function with return value
    interpreter.exec('''
    def add_one#1 ( arg 1 ) + 1
    print add_one 5
    ''')
    
    # Recursive function
    interpreter.exec('''
    def countdown#1 (
        print arg 1
        if ( arg 1 ) > 0
            countdown ( arg 1 ) - 1
            print "Done!"
    )
    countdown 3
    ''')


def test_complex_example():
    """Test a more complex example"""
    print("\n=== Testing Complex Example ===")
    interpreter = PangeaInterpreter()
    
    # Fibonacci sequence
    interpreter.exec('''
    ( 
        def fibonacci#1
        if ( arg 1 ) <= 1
            arg 1
            ( fibonacci ( ( arg 1 ) - 1 ) ) + ( fibonacci ( ( arg 1 ) - 2 ) )
        
        print "Fibonacci+sequence:"
        10 times (
            print fibonacci ( times_count 1 ) - 1
        )
    )
    ''')


def interactive_mode():
    """Interactive REPL mode"""
    print("\n=== Interactive Mode ===")
    print("Enter Pangea code (type 'exit' to quit):")
    
    interpreter = PangeaInterpreter()
    
    while True:
        try:
            code = input("pangea> ")
            if code.strip().lower() == 'exit':
                break
            if code.strip():
                interpreter.exec(code)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main test function"""
    test_basic_operations()
    test_control_flow()
    test_data_structures()
    test_functions()
    test_complex_example()
    
    # Uncomment the next line to run interactive mode
    # interactive_mode()


if __name__ == "__main__":
    main()
