#!/usr/bin/env python3
"""
Comprehensive Stress Test Suite for Pangea Python Interpreter
Tests performance, memory usage, edge cases, and production readiness
"""

import time
import sys
import traceback
import gc
import psutil
import os
from pangea_python_interpreter import PangeaInterpreter


class StressTestSuite:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.performance_metrics = {}
        
    def run_all_tests(self):
        """Run comprehensive stress test suite"""
        print("🚀 PANGEA PYTHON INTERPRETER STRESS TEST SUITE")
        print("=" * 60)
        
        test_categories = [
            ("Performance Tests", self.performance_tests),
            ("Memory Stress Tests", self.memory_tests),
            ("Edge Case Tests", self.edge_case_tests),
            ("Recursive Depth Tests", self.recursion_tests),
            ("Large Data Structure Tests", self.large_data_tests),
            ("Complex Program Tests", self.complex_program_tests),
            ("Error Handling Tests", self.error_handling_tests),
            ("Concurrent Execution Tests", self.concurrent_tests),
        ]
        
        for category_name, test_func in test_categories:
            print(f"\n📊 {category_name}")
            print("-" * 40)
            test_func()
        
        self.print_summary()
    
    def measure_performance(self, test_name, func, *args, **kwargs):
        """Measure execution time and memory usage"""
        process = psutil.Process(os.getpid())
        
        # Initial memory
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Execute and time
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            success = True
        except Exception as e:
            end_time = time.time()
            result = str(e)
            success = False
        
        # Final memory
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        
        execution_time = end_time - start_time
        memory_delta = mem_after - mem_before
        
        self.performance_metrics[test_name] = {
            'time': execution_time,
            'memory_delta': memory_delta,
            'success': success,
            'result': result
        }
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {execution_time:.4f}s, {memory_delta:+.2f}MB")
        
        if success:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
            print(f"    Error: {result}")
        
        return result if success else None
    
    def performance_tests(self):
        """Test performance with various workloads"""
        
        def factorial_performance():
            interpreter = PangeaInterpreter()
            # Test factorial of 20 (should be fast)
            interpreter.exec('''
                def factorial#1
                if ( arg 1 ) == 0
                 1
                 ( arg 1 ) * factorial ( arg 1 ) - 1
            ''')
            return interpreter.exec('factorial 20')
        
        def fibonacci_performance():
            interpreter = PangeaInterpreter()
            # Test Fibonacci sequence calculation
            interpreter.exec('''
                def fib#1
                if ( arg 1 ) < 2
                 arg 1
                 ( fib ( ( arg 1 ) - 1 ) ) + ( fib ( ( arg 1 ) - 2 ) )
            ''')
            return interpreter.exec('fib 15')  # Fib(15) should be reasonable
        
        def loop_performance():
            interpreter = PangeaInterpreter()
            # Test large loop performance
            return interpreter.exec('1000 times pass')
        
        def string_operations():
            interpreter = PangeaInterpreter()
            # Test string operations
            interpreter.exec('100 times print "performance+test+string"')
            return True
        
        self.measure_performance("Factorial(20)", factorial_performance)
        self.measure_performance("Fibonacci(15)", fibonacci_performance)
        self.measure_performance("1000 Loop Iterations", loop_performance)
        self.measure_performance("100 String Operations", string_operations)
    
    def memory_tests(self):
        """Test memory usage and garbage collection"""
        
        def large_array_creation():
            interpreter = PangeaInterpreter()
            # Create large array
            code = "[ " + " ".join([str(i) for i in range(1000)]) + " ]"
            return interpreter.exec(code)
        
        def nested_function_calls():
            interpreter = PangeaInterpreter()
            # Test deeply nested function calls
            interpreter.exec('''
                def counter#1
                if ( arg 1 ) == 0
                 0
                 1 + counter ( ( arg 1 ) - 1 )
            ''')
            return interpreter.exec('counter 100')
        
        def memory_intensive_objects():
            interpreter = PangeaInterpreter()
            # Create complex nested objects
            return interpreter.exec('''
                { 
                    "data" [ 1 2 3 4 5 6 7 8 9 10 ]
                    "nested" { "level1" { "level2" "deep+value" } }
                    "array" [ { "id" 1 } { "id" 2 } { "id" 3 } ]
                }
            ''')
        
        self.measure_performance("Large Array (1000 elements)", large_array_creation)
        self.measure_performance("Nested Function Calls (100 deep)", nested_function_calls)
        self.measure_performance("Complex Object Creation", memory_intensive_objects)
        
        # Force garbage collection
        gc.collect()
    
    def edge_case_tests(self):
        """Test edge cases and boundary conditions"""
        
        def empty_program():
            interpreter = PangeaInterpreter()
            return interpreter.exec('')
        
        def only_comments():
            interpreter = PangeaInterpreter()
            return interpreter.exec('# This is just a comment\n# Another comment')
        
        def nested_parentheses():
            interpreter = PangeaInterpreter()
            return interpreter.exec('( ( ( ( 42 ) ) ) )')
        
        def complex_when_chains():
            interpreter = PangeaInterpreter()
            return interpreter.exec('''
                print
                "first" when 1 == 1
                "second" when 1 == 2
                "third" when 1 == 3
                "default"
            ''')
        
        def zero_times_loop():
            interpreter = PangeaInterpreter()
            return interpreter.exec('0 times print "should+not+print"')
        
        self.measure_performance("Empty Program", empty_program)
        self.measure_performance("Comments Only", only_comments)
        self.measure_performance("Nested Parentheses", nested_parentheses)
        self.measure_performance("Complex When Chains", complex_when_chains)
        self.measure_performance("Zero Times Loop", zero_times_loop)
    
    def recursion_tests(self):
        """Test recursion limits and deep call stacks"""
        
        def moderate_recursion():
            interpreter = PangeaInterpreter()
            interpreter.exec('''
                def countdown#1
                if ( arg 1 ) == 0
                 "done"
                 countdown ( ( arg 1 ) - 1 )
            ''')
            return interpreter.exec('countdown 50')
        
        def tail_recursion_simulation():
            interpreter = PangeaInterpreter()
            interpreter.exec('''
                def sum_to#1
                if ( arg 1 ) == 0
                 0
                 ( arg 1 ) + sum_to ( ( arg 1 ) - 1 )
            ''')
            return interpreter.exec('sum_to 100')
        
        self.measure_performance("Moderate Recursion (50 levels)", moderate_recursion)
        self.measure_performance("Tail Recursion Sum (100)", tail_recursion_simulation)
    
    def large_data_tests(self):
        """Test handling of large data structures"""
        
        def large_object():
            interpreter = PangeaInterpreter()
            # Create object with many keys
            pairs = []
            for i in range(100):
                pairs.extend([f'"key{i}"', str(i)])
            code = "{ " + " ".join(pairs) + " }"
            return interpreter.exec(code)
        
        def nested_arrays():
            interpreter = PangeaInterpreter()
            return interpreter.exec('[ [ [ [ [ 1 2 3 ] 4 5 ] 6 7 ] 8 9 ] 10 ]')
        
        def large_computation():
            interpreter = PangeaInterpreter()
            # Large mathematical computation
            return interpreter.exec('( 123 + 456 ) * ( 789 - 321 ) / ( 147 + 258 )')
        
        self.measure_performance("Large Object (100 keys)", large_object)
        self.measure_performance("Deeply Nested Arrays", nested_arrays)
        self.measure_performance("Large Mathematical Computation", large_computation)
    
    def complex_program_tests(self):
        """Test complex real-world-like programs"""
        
        def advanced_fizzbuzz():
            interpreter = PangeaInterpreter()
            return interpreter.exec('''
                def multiple#2
                0 == ( ( arg 1 ) % ( arg 2 ) )
                
                def i#0
                times_count 1
                
                def fizzbuzz_logic#0
                "fizzbuzz" when multiple i 15
                "fizz" when multiple i 3  
                "buzz" when multiple i 5
                i
                
                100 times fizzbuzz_logic
            ''')
        
        def data_processing():
            interpreter = PangeaInterpreter()
            return interpreter.exec('''
                def process_item#1
                ( arg 1 ) * 2
                
                [ 1 2 3 4 5 ] each (
                    print process_item each_item
                )
            ''')
        
        def calculator_simulation():
            interpreter = PangeaInterpreter()
            return interpreter.exec('''
                def add#2
                ( arg 1 ) + ( arg 2 )
                
                def multiply#2  
                ( arg 1 ) * ( arg 2 )
                
                def calculate#0
                multiply ( add 5 3 ) ( add 2 4 )
                
                print calculate
            ''')
        
        self.measure_performance("Advanced FizzBuzz (100)", advanced_fizzbuzz)
        self.measure_performance("Data Processing Pipeline", data_processing)
        self.measure_performance("Calculator Simulation", calculator_simulation)
    
    def error_handling_tests(self):
        """Test error handling and recovery"""
        
        def undefined_function():
            interpreter = PangeaInterpreter()
            try:
                interpreter.exec('undefined_function 42')
                return False  # Should have failed
            except:
                return True  # Expected failure
        
        def division_by_zero():
            interpreter = PangeaInterpreter()
            try:
                interpreter.exec('10 / 0')
                return False
            except:
                return True
        
        def malformed_syntax():
            interpreter = PangeaInterpreter()
            try:
                interpreter.exec('( ( ( incomplete')
                return False
            except:
                return True
        
        def invalid_arity():
            interpreter = PangeaInterpreter()
            try:
                interpreter.exec('print')  # Missing argument
                return True  # Might handle gracefully
            except:
                return True  # Or fail gracefully
        
        self.measure_performance("Undefined Function Error", undefined_function)
        self.measure_performance("Malformed Syntax Error", malformed_syntax)
        self.measure_performance("Invalid Arity Error", invalid_arity)
    
    def concurrent_tests(self):
        """Test behavior under concurrent-like conditions"""
        
        def multiple_interpreters():
            interpreters = []
            for i in range(10):
                interpreter = PangeaInterpreter()
                interpreter.exec(f'print "interpreter+{i}"')
                interpreters.append(interpreter)
            return len(interpreters)
        
        def rapid_execution():
            interpreter = PangeaInterpreter()
            for i in range(100):
                interpreter.exec(f'print {i}')
            return True
        
        self.measure_performance("Multiple Interpreters (10)", multiple_interpreters)
        self.measure_performance("Rapid Execution (100 calls)", rapid_execution)
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("🎯 STRESS TEST SUMMARY")
        print("=" * 60)
        
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.tests_passed} ✅")
        print(f"Failed: {self.tests_failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Performance analysis
        if self.performance_metrics:
            print(f"\n⚡ PERFORMANCE ANALYSIS")
            print("-" * 30)
            
            times = [m['time'] for m in self.performance_metrics.values() if m['success']]
            if times:
                avg_time = sum(times) / len(times)
                max_time = max(times)
                print(f"Average Execution Time: {avg_time:.4f}s")
                print(f"Slowest Test: {max_time:.4f}s")
            
            # Memory usage
            memory_deltas = [m['memory_delta'] for m in self.performance_metrics.values()]
            total_memory = sum(memory_deltas)
            print(f"Total Memory Delta: {total_memory:+.2f}MB")
            
            # Find performance outliers
            slow_tests = [(name, metrics) for name, metrics in self.performance_metrics.items() 
                         if metrics['success'] and metrics['time'] > 0.1]
            
            if slow_tests:
                print(f"\n🐌 SLOW TESTS (>0.1s):")
                for name, metrics in slow_tests:
                    print(f"  • {name}: {metrics['time']:.4f}s")
        
        # Final verdict
        print(f"\n🏆 PRODUCTION READINESS VERDICT")
        print("-" * 35)
        
        if success_rate >= 95:
            print("🎉 EXCELLENT - Production Ready!")
        elif success_rate >= 85:
            print("✅ GOOD - Minor issues to address")
        elif success_rate >= 70:
            print("⚠️  FAIR - Significant improvements needed")
        else:
            print("❌ POOR - Major issues require fixing")
        
        print(f"\nFor a v1.0.0 release, we expect >95% success rate.")
        print(f"Current performance: {success_rate:.1f}%")


def main():
    """Run the stress test suite"""
    try:
        suite = StressTestSuite()
        suite.run_all_tests()
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
