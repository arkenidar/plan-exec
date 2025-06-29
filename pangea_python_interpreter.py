#!/usr/bin/env python3
"""
Pangea Python Interpreter
A Python translation of the Pangea JavaScript interpreter from pangea-js

This interpreter implements a stack-based language with:
- Function definitions with arity
- Infix, prefix, and postfix operators
- Control flow (if, times, each)
- Arrays and objects
- Function calls with arguments
"""

import re
import json
from typing import List, Dict, Any, Optional, Union, Callable


class PangeaInterpreter:
    def __init__(self):
        self.words: List[str] = ["("]  # Begin sequence
        self.phrase_lengths: List[int] = []
        self.namespace = {
            'arities': {},
            'stack': [{}],
            'times_stack': [],
            'each_stack': [],
        }
        
        # Initialize built-in functions
        self._init_builtin_functions()
    
    def _init_builtin_functions(self):
        """Initialize all built-in functions and operators"""
        
        # Basic functions
        builtin_funcs = {
            'print': {'func': self._print, 'arity': 1},
            'when': {'func': self._when, 'arity': 2, 'operator': 'infix'},
            'times': {'func': self._times, 'arity': 1, 'operator': 'infix'},
            'def': {'func': self._def, 'arity': 2},
            'arg': {'func': self._arg, 'arity': 1},
            'if': {'func': self._if3, 'arity': 3},
            'unless': {'func': self._unless, 'arity': 1, 'operator': 'infix'},
            'dont': {'func': self._dont, 'arity': 1},
            'pass': {'func': self._pass, 'arity': 0},
            'times_count': {'func': self._times_count, 'arity': 1},
            'greater': {'func': self._greater, 'arity': 1, 'operator': 'infix'},
            'squared': {'func': self._squared, 'arity': 0, 'operator': 'postfix'},
            'each': {'func': self._each, 'arity': 1, 'operator': 'infix'},
            'each_item': {'func': self._each_item, 'arity': 0},
            'each_item_i': {'func': self._each_item_i, 'arity': 1},
            'each_key': {'func': self._each_key, 'arity': 0},
            'each_key_i': {'func': self._each_key_i, 'arity': 1},
            'each_break': {'func': self._each_break, 'arity': 0},
        }
        
        # Add aliases
        builtin_funcs['comment'] = builtin_funcs['dont']
        builtin_funcs['>'] = builtin_funcs['greater']
        
        # Binary operators
        self._add_binary_operator('add', '+', lambda a, b: a + b)
        self._add_binary_operator('subtract', '-', lambda a, b: a - b)
        self._add_binary_operator('multiply', '*', lambda a, b: a * b)
        self._add_binary_operator('equal', '==', lambda a, b: a == b)
        self._add_binary_operator('lesser', '<', lambda a, b: a < b)
        self._add_binary_operator('lesserOrEqual', '<=', lambda a, b: a <= b)
        self._add_binary_operator('modulus', '%', lambda a, b: a % b)
        
        # Exponent operator
        builtin_funcs['exponent'] = {'func': self._exponent, 'arity': 1, 'operator': 'infix'}
        builtin_funcs['**'] = builtin_funcs['exponent']
        
        # Initialize namespace
        for name, entry in builtin_funcs.items():
            self.namespace[name] = entry
    
    def _add_binary_operator(self, name: str, symbol: str, operation: Callable):
        """Add a binary operator to the namespace"""
        def operator_func(params):
            left = self.word_exec(params[0], skip_operator=True)
            right = self.word_exec(params[1])
            return operation(left, right)
        
        entry = {
            'func': operator_func,
            'arity': 1,
            'operator': 'infix'
        }
        
        self.namespace[name] = entry
        self.namespace[symbol] = entry
    
    def parse_code(self, code: str) -> List[str]:
        """Parse code into words, handling special string formatting and comments"""
        # Remove comments (lines starting with #)
        lines = code.split('\n')
        filtered_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                filtered_lines.append(line)
        
        code = ' '.join(filtered_lines)
        
        # Parse words while preserving quoted strings
        words = []
        in_string = False
        current_word = ""
        i = 0
        
        while i < len(code):
            char = code[i]
            
            if char == '"' and not in_string:
                # Start of string
                in_string = True
                current_word = '"'
            elif char == '"' and in_string:
                # End of string
                in_string = False
                current_word += '"'
                words.append(current_word)
                current_word = ""
            elif in_string:
                # Inside string
                current_word += char
            elif char.isspace():
                # Space outside string
                if current_word:
                    words.append(current_word)
                    current_word = ""
            else:
                # Regular character
                current_word += char
            
            i += 1
        
        # Add final word if any
        if current_word:
            words.append(current_word)
        
        return [self._handle_plus(word) for word in words if word]
    
    def _handle_plus(self, word: str) -> str:
        """Handle special string formatting with (+) syntax"""
        if not self._is_string(word):
            return word
        
        try:
            parsed = json.loads(word)
            parts = parsed.split("(+)")
            parts = [part.replace("+", " ") for part in parts]
            result = "+".join(parts)
            return json.dumps(result)
        except:
            return word
    
    def exec(self, code: str) -> Any:
        """Execute Pangea code"""
        print(f"Executing: {code}")
        
        previous_length = len(self.words)
        parsed_words = self.parse_code(code)
        self.words.extend(parsed_words)
        
        print(f"Words: {self.words}")
        
        # Pre-scan for arity definitions
        for word in self.words:
            if "#" in word and not self._is_string(word):
                parts = word.split("#")
                if len(parts) == 2:
                    try:
                        arity = int(parts[1])
                        entry = {'arity': arity, 'word': word}
                        self.namespace['arities'][parts[0]] = entry
                    except ValueError:
                        pass
        
        # Calculate phrase lengths
        self.phrase_lengths = [0] * len(self.words)
        self._phrase_length(0)
        
        print(f"Phrase lengths: {self.phrase_lengths}")
        
        # Execute the new code
        print("[begin]")
        current_idx = previous_length
        result = None
        
        # Execute all statements at the top level
        while current_idx < len(self.words):
            if self.words[current_idx] == ")":
                break
            result = self.word_exec(current_idx)
            current_idx += self._phrase_length(current_idx)
        
        print("[end]")
        return result
    
    def word_exec(self, word_index: int, skip_operator: bool = False) -> Any:
        """Execute a word at the given index"""
        if word_index >= len(self.words):
            print(f"Error: wrong word_index: {word_index}")
            return None
        
        word = self.words[word_index]
        
        def next_index(skip_op: bool = False) -> int:
            return word_index + self._phrase_length(word_index, skip_op)
        
        # Handle postfix and infix operators
        if not skip_operator:
            next_word_idx = next_index(True)
            if next_word_idx < len(self.words):
                next_word = self.words[next_word_idx]
                entry = self.namespace.get(next_word)
                
                if entry and entry.get('operator') == 'postfix':
                    return entry['func']([word_index])
                
                if entry and entry.get('operator') == 'infix':
                    arity = entry['arity']
                    params = [word_index]  # First operand
                    current_idx = word_index + self._phrase_length(word_index, True)
                    current_idx += 1  # Skip operator
                    
                    for _ in range(arity):
                        params.append(current_idx)
                        current_idx += self._phrase_length(current_idx)
                    
                    return entry['func'](params)
        
        # Single value (literal)
        parsed = self._parse(word)
        if parsed is not None:
            return parsed
        
        # Parentheses blocks
        if word == "(":
            result = None
            current_idx = word_index + 1
            while current_idx < len(self.words) and self.words[current_idx] != ")":
                exec_result = self.word_exec(current_idx)
                if exec_result is not None:
                    result = exec_result
                current_idx += self._phrase_length(current_idx)
            return result
        
        # Array blocks
        if word == "[":
            result = []
            current_idx = word_index + 1
            while current_idx < len(self.words) and self.words[current_idx] != "]":
                element = self.word_exec(current_idx)
                result.append(element)
                current_idx += self._phrase_length(current_idx)
            return result
        
        # Object blocks
        if word == "{":
            result = {}
            current_idx = word_index + 1
            mode = "key"
            key = None
            
            while current_idx < len(self.words) and self.words[current_idx] != "}":
                element = self.word_exec(current_idx)
                if mode == "key":
                    key = element
                    mode = "value"
                else:
                    result[key] = element
                    mode = "key"
                current_idx += self._phrase_length(current_idx)
            return result
        
        # Function calls
        word_id = word.split("#")[0] if "#" in word else word
        entry = self.namespace.get(word_id)
        
        if entry is None:
            print(f"Undefined id: {word_id}")
            return None
        
        if isinstance(entry, dict) and 'func' in entry:
            arity = entry['arity']
            func = entry['func']
            params = []
            current_idx = word_index + 1
            
            for _ in range(arity):
                params.append(current_idx)
                current_idx += self._phrase_length(current_idx)
            
            return func(params)
        
        print(f"Not handled, word: {word}")
        return None
    
    def _phrase_length(self, word_index: int, skip_operator: bool = False) -> int:
        """Calculate the length of a phrase starting at word_index"""
        if not skip_operator and word_index < len(self.phrase_lengths) and self.phrase_lengths[word_index] > 0:
            return self.phrase_lengths[word_index]
        
        if word_index >= len(self.words):
            print(f"Error: wrong word_index in phrase_length: {word_index}")
            return 0
        
        word = self.words[word_index]
        length = 1
        
        def next_index() -> int:
            return word_index + length
        
        def word_arity(w: str) -> Optional[int]:
            if "#" in w:
                return 0
            
            entry = self.namespace.get(w) or self.namespace.get('arities', {}).get(w)
            if entry is None:
                print(f"Word not in namespace: {w}")
                return None
            return entry.get('arity', 0)
        
        # Single value
        if self._parse(word) is not None:
            pass  # length remains 1
        
        # Blocks
        elif word in ["{", "[", "("]:
            matching_parens = {"{": "}", "[": "]", "(": ")"}
            while True:
                if next_index() >= len(self.words):
                    break
                if self.words[next_index()] == matching_parens[word]:
                    if next_index() < len(self.phrase_lengths):
                        self.phrase_lengths[next_index()] = 1
                    length += 1
                    break
                else:
                    length += self._phrase_length(next_index())
        
        # Function calls
        else:
            arity = word_arity(word)
            if arity is not None:
                for _ in range(arity):
                    length += self._phrase_length(next_index())
        
        # Handle postfix/infix operators
        if not skip_operator:
            next_word_idx = next_index()
            if next_word_idx < len(self.words):
                next_word = self.words[next_word_idx]
                entry = self.namespace.get(next_word)
                if entry and entry.get('operator') in ['postfix', 'infix']:
                    length += self._phrase_length(next_word_idx)
        
        if not skip_operator and word_index < len(self.phrase_lengths):
            self.phrase_lengths[word_index] = length
        
        return length
    
    def _parse(self, text: str) -> Any:
        """Parse a literal value"""
        try:
            return json.loads(text)
        except:
            return None
    
    def _is_number(self, text: str) -> bool:
        """Check if text represents a number"""
        return isinstance(self._parse(text), (int, float))
    
    def _is_string(self, text: str) -> bool:
        """Check if text represents a string"""
        return isinstance(self._parse(text), str)
    
    # Built-in function implementations
    def _print(self, params: List[int]) -> Any:
        """Print function"""
        output = self.word_exec(params[0])
        print(output)
        return output
    
    def _when(self, params: List[int]) -> Any:
        """When function: what when condition else-what"""
        condition = self.word_exec(params[1])
        return self.word_exec(params[0], True) if condition else self.word_exec(params[2])
    
    def _times(self, params: List[int]) -> Any:
        """Times function"""
        count = self.word_exec(params[0], True)
        result = None
        
        self.namespace['times_stack'].append(1)
        
        for i in range(int(count)):
            result = self.word_exec(params[1])
            self.namespace['times_stack'][-1] += 1
        
        self.namespace['times_stack'].pop()
        return result
    
    def _times_count(self, params: List[int]) -> int:
        """Get current times counter"""
        depth = self.word_exec(params[0])
        stack = self.namespace['times_stack']
        return stack[-depth] if stack else 0
    
    def _def(self, params: List[int]) -> None:
        """Define a function"""
        word_parts = self.words[params[0]].split("#")
        func_id = word_parts[0]
        arity = int(word_parts[1])
        word_index = params[1]
        
        def user_func(func_params):
            # Evaluate parameters
            args = [self.word_exec(p) for p in func_params]
            
            # Push args to stack
            self.namespace['stack'].append({'args': args})
            
            # Execute function body
            result = self.word_exec(word_index)
            
            # Pop stack
            self.namespace['stack'].pop()
            
            return result
        
        self.namespace[func_id] = {
            'arity': arity,
            'func': user_func
        }
    
    def _arg(self, params: List[int]) -> Any:
        """Get function argument"""
        index = self.word_exec(params[0])
        stack = self.namespace['stack']
        if stack:
            args = stack[-1].get('args', [])
            return args[index - 1] if 0 < index <= len(args) else None
        return None
    
    def _if3(self, params: List[int]) -> Any:
        """If function with 3 parameters"""
        condition = self.word_exec(params[0])
        return self.word_exec(params[1] if condition else params[2])
    
    def _unless(self, params: List[int]) -> Any:
        """Unless function"""
        condition = self.word_exec(params[1])
        if not condition:
            return self.word_exec(params[0], True)
    
    def _dont(self, params: List[int]) -> None:
        """Comment/dont function - does nothing"""
        pass
    
    def _pass(self, params: List[int]) -> None:
        """Pass function - does nothing"""
        pass
    
    def _greater(self, params: List[int]) -> bool:
        """Greater than operator"""
        left = self.word_exec(params[0], True)
        right = self.word_exec(params[1])
        return left > right
    
    def _squared(self, params: List[int]) -> float:
        """Squared postfix operator"""
        n = self.word_exec(params[0], True)
        return n ** 2
    
    def _exponent(self, params: List[int]) -> float:
        """Exponent infix operator"""
        base = self.word_exec(params[0], True)
        exp = self.word_exec(params[1])
        return base ** exp
    
    def _each(self, params: List[int]) -> Any:
        """Each iterator function"""
        iterable = self.word_exec(params[0], True)
        result = None
        
        self.namespace['each_stack'].append({'stop': False})
        
        if isinstance(iterable, dict):
            items = iterable.items()
        elif isinstance(iterable, list):
            items = enumerate(iterable)
        else:
            items = []
        
        for key, item in items:
            if self.namespace['each_stack'][-1]['stop']:
                break
            
            self.namespace['each_stack'][-1]['iter'] = {'v': item, 'k': key}
            result = self.word_exec(params[1])
        
        self.namespace['each_stack'].pop()
        return result
    
    def _each_item(self, params: List[int]) -> Any:
        """Get current iteration item"""
        return self._each_item_gen(1, 'v')
    
    def _each_item_i(self, params: List[int]) -> Any:
        """Get iteration item at depth"""
        depth = self.word_exec(params[0])
        return self._each_item_gen(depth, 'v')
    
    def _each_key(self, params: List[int]) -> Any:
        """Get current iteration key"""
        return self._each_item_gen(1, 'k')
    
    def _each_key_i(self, params: List[int]) -> Any:
        """Get iteration key at depth"""
        depth = self.word_exec(params[0])
        return self._each_item_gen(depth, 'k')
    
    def _each_item_gen(self, depth: int, attribute: str = 'v') -> Any:
        """Internal function to get iteration value"""
        stack = self.namespace['each_stack']
        if stack and len(stack) >= depth:
            return stack[-depth]['iter'][attribute]
        return None
    
    def _each_break(self, params: List[int]) -> None:
        """Break from each loop"""
        stack = self.namespace['each_stack']
        if stack:
            stack[-1]['stop'] = True


def main():
    """Main function for testing"""
    interpreter = PangeaInterpreter()
    
    # Test basic functionality
    print("=== Testing Basic Print ===")
    interpreter.exec('print "hello+world!"')
    
    print("\n=== Testing Times ===")
    interpreter.exec('2 times print "repeated"')
    
    print("\n=== Testing Function Definition ===")
    interpreter.exec('( def f1#1 print arg 1   f1 111 )')
    interpreter.exec('f1 222')
    
    print("\n=== Testing Factorial ===")
    interpreter.exec('''( def factorial#1
     if ( arg 1 ) == 0
      1
      ( arg 1 ) * factorial ( arg 1 ) - 1 
    print factorial 3 )''')
    
    print("\n=== Testing FizzBuzz ===")
    interpreter.exec('''( print "fizz-buzz+game"

    def multiple#2
    0 == ( ( arg 1 ) % ( arg 2 ) )

    def i#0
    times_count 1

    def multiple_of#1
    multiple i arg 1

    20 times (
        
        print
        "fizz-buzz" when multiple_of 15
        "fizz" when multiple_of 3
        "buzz" when multiple_of 5
        i
    )
        
    )''')


if __name__ == "__main__":
    main()