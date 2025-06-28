# Plan Language - Correct phraseLength Implementation
# Demonstrating the critical importance of skipOperator parameter

from typing import List, Any, Optional, Dict
import json

# Global state
words: List[str] = []
phrase_lengths: List[Optional[int]] = []
namespace = {
    'arities': {},
    'stack': [{}],
}

def debug_print(*args):
    print("debug:", *args)

def parse_literal(text: str) -> Any:
    """Parse JSON literals (pangea-js style)"""
    try:
        return json.loads(text)
    except:
        return None

def is_literal(word: str) -> bool:
    """Check if word is a literal value"""
    return parse_literal(word) is not None

def word_arity(word: str) -> Optional[int]:
    """Get the arity of a word (pangea-js style)"""
    # Function definitions with #
    if "#" in word and not isinstance(parse_literal(word), str):
        return 0
    
    # Check namespace
    entry = namespace.get(word) or namespace['arities'].get(word)
    if entry:
        return entry.get('arity')
    
    return None

def phrase_length(word_index: int, skip_operator: bool = False) -> int:
    """
    CRITICAL FUNCTION: Calculate phrase length with proper skipOperator handling
    This is the heart of pangea-js's operator precedence system
    """
    
    # Cache check - ONLY when not skipping operators
    if skip_operator == False:
        if word_index < len(phrase_lengths) and phrase_lengths[word_index] is not None:
            return phrase_lengths[word_index]
    
    if word_index >= len(words):
        debug_print(f"ERROR: wrong word_index: {word_index}")
        return 0
    
    length = 1
    word = words[word_index]
    
    if word is None:
        debug_print(f"ERROR: wrong word_index: {word_index}")
        return 0
    
    def next_index():
        return word_index + length
    
    # Single value (literals) - length = 1
    if parse_literal(word) is not None:
        pass  # length = 1
    
    # Block structures: {}, [], ()
    elif word in ["{", "[", "("]:
        matching_parens = {"{": "}", "[": "]", "(": ")"}
        while True:
            if next_index() >= len(words):
                break  # Close sequence at end
            if words[next_index()] == matching_parens[word]:
                # Set phrase length for closing paren
                if next_index() < len(phrase_lengths):
                    phrase_lengths[next_index()] = 1
                length += 1
                break
            else:
                length += phrase_length(next_index())
    
    # Functions and operators (nested)
    else:
        arity = word_arity(word)
        if arity is not None:
            for i in range(arity):
                if next_index() < len(words):
                    length += phrase_length(next_index())
        else:
            debug_print(f"Word not in namespace: {word}")
    
    # CRITICAL: Check for postfix/infix operators
    # This is where skipOperator becomes essential
    next_word_index = next_index()
    if next_word_index < len(words) and skip_operator == False:
        next_word = words[next_word_index]
        entry = namespace.get(next_word)
        
        if entry and entry.get('operator') in ['postfix', 'infix']:
            # Recursively include the operator phrase
            length += phrase_length(next_word_index)
    
    # Cache result - ONLY when not skipping operators
    if skip_operator == False:
        # Extend phrase_lengths if needed
        while len(phrase_lengths) <= word_index:
            phrase_lengths.append(None)
        phrase_lengths[word_index] = length
    
    return length

def word_exec(word_index: int, skip_operator: bool = False) -> Any:
    """
    Execute word at index with proper skipOperator handling
    The skipOperator parameter is CRITICAL for preventing infinite recursion
    """
    if word_index >= len(words):
        debug_print(f"ERROR: wrong word_index: {word_index}")
        return None
    
    word = words[word_index]
    
    def next_index(skip_op: bool = False):
        return word_index + phrase_length(word_index, skip_op)
    
    # CRITICAL: Check for postfix/infix operators FIRST
    # But only if we're not already skipping operators
    next_word_index = next_index(True)  # Skip operator for this calculation
    if next_word_index < len(words) and not skip_operator:
        next_word = words[next_word_index]
        entry = namespace.get(next_word)
        
        if entry and entry.get('operator') == 'postfix':
            # Postfix operator: execute it with current word as operand
            return entry['func']([word_index])
        
        if entry and entry.get('operator') == 'infix':
            # Infix operator: this word is left operand
            left_val = word_exec(word_index, True)  # CRITICAL: skip_operator=True
            op_arity = entry.get('arity', 1)
            
            # Collect right operands
            params = [left_val]
            current_index = next_word_index + 1
            for i in range(op_arity):
                if current_index < len(words):
                    right_val = word_exec(current_index)
                    params.append(right_val)
                    current_index += phrase_length(current_index)
            
            return entry['func'](params)
    
    # Handle literals
    if parse_literal(word) is not None:
        return parse_literal(word)
    
    # Handle functions
    entry = namespace.get(word)
    if entry and 'func' in entry:
        arity = entry['arity']
        func = entry['func']
        
        # Collect parameters
        params = []
        current_index = word_index + 1
        for i in range(arity):
            if current_index < len(words):
                params.append(current_index)
                current_index += phrase_length(current_index)
        
        return func(params)
    
    debug_print(f"Unknown word: {word}")
    return word

# Example demonstrating the critical nature of skipOperator
def demonstrate_skip_operator_importance():
    """Show why skipOperator is absolutely critical"""
    global words, phrase_lengths, namespace
    
    # Initialize namespace with operators
    namespace.update({
        '+': {'arity': 1, 'operator': 'infix', 'func': lambda params: params[0] + params[1]},
        '*': {'arity': 1, 'operator': 'infix', 'func': lambda params: params[0] * params[1]},
        'when': {'arity': 2, 'operator': 'infix', 'func': lambda params: params[0] if params[1] else (params[2] if len(params) > 2 else None)},
    })
    
    # Test case: "5 + 3 * 2"
    words = ["5", "+", "3", "*", "2"]
    phrase_lengths = [None] * len(words)
    
    print("=== Demonstrating skipOperator importance ===")
    print(f"Expression: {' '.join(words)}")
    
    # Calculate phrase lengths
    for i in range(len(words)):
        if phrase_lengths[i] is None:
            length = phrase_length(i)
            print(f"phrase_length({i}, skip_operator=False) = {length}")
    
    print(f"Final phrase_lengths: {phrase_lengths}")
    
    # Show what happens with skipOperator=True for operands
    print("\nWith skipOperator=True (for operand parsing):")
    for i in [0, 2, 4]:  # Just the operands
        length_skip = phrase_length(i, skip_operator=True)
        print(f"phrase_length({i}, skip_operator=True) = {length_skip}")
    
    print("\n=== Test case: 'value when condition' ===")
    # Test when operator
    words = ['"fizz"', 'when', 'true']
    phrase_lengths = [None] * len(words)
    
    for i in range(len(words)):
        if phrase_lengths[i] is None:
            length = phrase_length(i)
            print(f"phrase_length({i}) = {length}")
    
    print(f"Phrase lengths: {phrase_lengths}")
    
    # Execute the when expression
    result = word_exec(0)
    print(f"Result: {result}")

def test_fizzbuzz_when_structure():
    """Test the structure from the user's selected code"""
    global words, phrase_lengths, namespace
    
    print("\n=== Testing FizzBuzz When Structure ===")
    
    # Initialize namespace for the test
    namespace.update({
        'def': {'arity': 2, 'func': None},  # Special handling
        'times_count': {'arity': 1, 'func': lambda params: 1},  # Simplified
        'when': {'arity': 2, 'operator': 'infix', 'func': lambda params: params[0] if params[1] else None},
        'multiple_of': {'arity': 1, 'func': lambda params: True},  # Simplified
    })
    
    # Test the specific structure: "fizz-buzz" when multiple_of 15
    words = ['"fizz-buzz"', 'when', 'multiple_of', '15']
    phrase_lengths = [None] * len(words)
    
    print(f"Expression: {' '.join(words)}")
    
    # Calculate phrase lengths with debug
    for i in range(len(words)):
        if phrase_lengths[i] is None:
            length = phrase_length(i)
            print(f"phrase_length({i}) = {length} (word: '{words[i]}')")
    
    print(f"Final phrase_lengths: {phrase_lengths}")
    
    # This should parse as: "fizz-buzz" when (multiple_of 15)
    # Where "multiple_of 15" is a function call that returns true/false

if __name__ == "__main__":
    demonstrate_skip_operator_importance()
    test_fizzbuzz_when_structure()
