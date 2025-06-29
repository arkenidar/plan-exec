#!/usr/bin/env python3
"""
Pangea REPL - Interactive command line interface for the Pangea interpreter
"""

import sys
import argparse
from pangea_python_interpreter import PangeaInterpreter


def run_file(filename):
    """Run a Pangea file"""
    try:
        with open(filename, 'r') as f:
            code = f.read()
        
        interpreter = PangeaInterpreter()
        interpreter.exec(code)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error executing file: {e}")
        sys.exit(1)


def run_repl():
    """Run interactive REPL"""
    print("Pangea Python Interpreter REPL")
    print("Type 'help' for help, 'exit' to quit")
    print("=" * 40)
    
    interpreter = PangeaInterpreter()
    
    while True:
        try:
            code = input("pangea> ").strip()
            
            if not code:
                continue
            
            if code.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if code.lower() == 'help':
                print_help()
                continue
            
            if code.lower() == 'reset':
                interpreter = PangeaInterpreter()
                print("Interpreter reset.")
                continue
            
            if code.lower() == 'examples':
                show_examples()
                continue
            
            # Execute the code
            interpreter.exec(code)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def print_help():
    """Print help information"""
    help_text = """
Pangea Language Help
===================

Basic Commands:
  help      - Show this help
  exit/quit - Exit the interpreter
  reset     - Reset interpreter state
  examples  - Show example code

Basic Syntax:
  print "hello"           - Print a string
  print 2 + 3            - Print arithmetic result
  5 times print "hi"     - Repeat action
  def func#1 print arg 1 - Define function
  func "test"            - Call function

Data Types:
  Numbers: 42, 3.14, -5
  Strings: "hello", "hello+world"
  Arrays:  [ 1 2 3 ]
  Objects: { "key" "value" }
  
Control Flow:
  if condition then else
  times count block
  when condition value
  unless condition block
  
Functions:
  def name#arity body    - Define function
  arg n                  - Get nth argument (1-indexed)
  
Built-in Functions:
  print, times, if, when, unless, def, arg
  each, each_item, each_key, each_break
  Mathematical: +, -, *, **, %, ==, <, >, <=, squared
"""
    print(help_text)


def show_examples():
    """Show example code"""
    examples = """
Example Code
============

1. Hello World:
   print "Hello+World!"

2. Arithmetic:
   print 2 + 3 * 4
   print 5 squared

3. Function Definition:
   def greet#1 print "Hello," print arg 1
   greet "Alice"

4. Loops:
   5 times print "Hello"
   3 times ( print "Count:" print times_count 1 )

5. Conditionals:
   print "positive" when 5 > 0
   if true print "yes" print "no"

6. Factorial (Recursive):
   def factorial#1 if ( arg 1 ) == 0 1 ( arg 1 ) * factorial ( arg 1 ) - 1
   print factorial 5

7. Arrays and Objects:
   print [ 1 2 3 4 5 ]
   print { "name" "John" "age" 30 }

8. Iteration:
   [ 1 2 3 ] each print each_item

Try copying and pasting these examples!
"""
    print(examples)


def run_code(code):
    """Run a single line of code"""
    interpreter = PangeaInterpreter()
    interpreter.exec(code)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Pangea Python Interpreter')
    parser.add_argument('file', nargs='?', help='Pangea file to execute')
    parser.add_argument('-c', '--code', help='Execute code directly')
    parser.add_argument('-i', '--interactive', action='store_true', 
                       help='Start interactive REPL after running file/code')
    
    args = parser.parse_args()
    
    # Execute file if provided
    if args.file:
        run_file(args.file)
    
    # Execute code if provided
    elif args.code:
        run_code(args.code)
    
    # Start REPL if requested or no other action
    if args.interactive or (not args.file and not args.code):
        run_repl()


if __name__ == "__main__":
    main()
