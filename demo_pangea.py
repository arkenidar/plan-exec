#!/usr/bin/env python3
"""
Demo script showing the Pangea interpreter capabilities
"""

from pangea_python_interpreter import PangeaInterpreter

def main():
    print("Pangea Python Interpreter Demo")
    print("=" * 40)
    
    interpreter = PangeaInterpreter()
    
    # Demo 1: Basic arithmetic
    print("\n1. Basic Arithmetic:")
    interpreter.exec('print 2 + 3 * 4')
    interpreter.exec('print 5 squared')
    interpreter.exec('print 2 ** 10')
    
    # Demo 2: Functions
    print("\n2. Function Definition and Calls:")
    interpreter.exec('def double#1 ( arg 1 ) * 2')
    interpreter.exec('print double 21')
    
    # Demo 3: Recursion  
    print("\n3. Recursive Fibonacci:")
    interpreter.exec('''
    def fib#1
    if ( arg 1 ) <= 1
        arg 1
        ( fib ( ( arg 1 ) - 1 ) ) + ( fib ( ( arg 1 ) - 2 ) )
    ''')
    interpreter.exec('print fib 8')
    
    # Demo 4: Control flow
    print("\n4. Control Flow:")
    interpreter.exec('print "positive" when 5 > 0')
    interpreter.exec('if false print "no" print "yes"')
    
    # Demo 5: Loops
    print("\n5. Loops with Times Count:")
    interpreter.exec('3 times ( print "Step" print times_count 1 )')
    
    # Demo 6: Data structures
    print("\n6. Data Structures:")
    interpreter.exec('print [ 10 20 30 ]')
    interpreter.exec('print { "language" "Pangea" "version" "1.0" }')
    
    print("\n" + "=" * 40)
    print("Demo completed successfully!")

if __name__ == "__main__":
    main()
