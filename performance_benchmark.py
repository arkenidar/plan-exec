#!/usr/bin/env python3
"""
Performance Benchmark Suite for Pangea Python Interpreter
Detailed performance analysis and comparison with baseline expectations
"""

import time
import statistics
import matplotlib.pyplot as plt
import json
from pangea_python_interpreter import PangeaInterpreter


class PerformanceBenchmark:
    def __init__(self):
        self.results = {}
        self.baseline_expectations = {
            # Expected maximum times for production readiness (seconds)
            'simple_print': 0.001,
            'factorial_10': 0.01,
            'fibonacci_15': 0.1,
            'fizzbuzz_100': 0.05,
            'loop_1000': 0.02,
            'large_array_100': 0.01,
            'nested_objects': 0.005,
            'recursive_50': 0.02,
        }
    
    def benchmark_function(self, name, func, iterations=10):
        """Benchmark a function multiple times for statistical accuracy"""
        times = []
        
        for i in range(iterations):
            start_time = time.perf_counter()
            try:
                result = func()
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            except Exception as e:
                print(f"❌ {name} failed on iteration {i+1}: {e}")
                return None
        
        # Calculate statistics
        stats = {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times),
            'iterations': iterations,
            'raw_times': times
        }
        
        self.results[name] = stats
        
        # Check against baseline
        baseline = self.baseline_expectations.get(name)
        status = "✅" if baseline and stats['mean'] <= baseline else "⚠️" if baseline else "ℹ️"
        
        print(f"{status} {name}:")
        print(f"    Mean: {stats['mean']:.6f}s ± {stats['stdev']:.6f}s")
        print(f"    Range: {stats['min']:.6f}s - {stats['max']:.6f}s")
        if baseline:
            ratio = stats['mean'] / baseline
            print(f"    vs Baseline: {ratio:.2f}x ({'PASS' if ratio <= 1 else 'SLOW'})")
        
        return stats
    
    def run_all_benchmarks(self):
        """Run comprehensive performance benchmarks"""
        print("🏁 PANGEA PERFORMANCE BENCHMARK SUITE")
        print("=" * 50)
        
        # Basic operations
        print("\n📊 Basic Operations")
        print("-" * 25)
        
        self.benchmark_function("simple_print", lambda: self.simple_print())
        self.benchmark_function("arithmetic_ops", lambda: self.arithmetic_operations())
        self.benchmark_function("string_ops", lambda: self.string_operations())
        
        # Algorithmic tests
        print("\n🧮 Algorithmic Performance")
        print("-" * 30)
        
        self.benchmark_function("factorial_10", lambda: self.factorial_test(10))
        self.benchmark_function("fibonacci_15", lambda: self.fibonacci_test(15))
        self.benchmark_function("fizzbuzz_100", lambda: self.fizzbuzz_test(100))
        
        # Data structure tests
        print("\n📦 Data Structure Performance")
        print("-" * 35)
        
        self.benchmark_function("large_array_100", lambda: self.large_array_test(100))
        self.benchmark_function("nested_objects", lambda: self.nested_objects_test())
        self.benchmark_function("array_iteration", lambda: self.array_iteration_test())
        
        # Control flow tests
        print("\n🔄 Control Flow Performance")
        print("-" * 32)
        
        self.benchmark_function("loop_1000", lambda: self.loop_test(1000))
        self.benchmark_function("recursive_50", lambda: self.recursive_test(50))
        self.benchmark_function("conditional_chains", lambda: self.conditional_test())
        
        # Memory intensive tests
        print("\n💾 Memory Performance")
        print("-" * 25)
        
        self.benchmark_function("large_computation", lambda: self.large_computation_test())
        self.benchmark_function("function_definitions", lambda: self.function_definition_test())
        
        self.generate_report()
    
    # Individual benchmark functions
    def simple_print(self):
        interpreter = PangeaInterpreter()
        return interpreter.exec('print "hello"')
    
    def arithmetic_operations(self):
        interpreter = PangeaInterpreter()
        return interpreter.exec('( 42 + 13 ) * ( 7 - 3 ) / 2')
    
    def string_operations(self):
        interpreter = PangeaInterpreter()
        return interpreter.exec('print "test+string+with+plus+signs"')
    
    def factorial_test(self, n):
        interpreter = PangeaInterpreter()
        interpreter.exec('''
            def factorial#1
            if ( arg 1 ) == 0
             1
             ( arg 1 ) * factorial ( ( arg 1 ) - 1 )
        ''')
        return interpreter.exec(f'factorial {n}')
    
    def fibonacci_test(self, n):
        interpreter = PangeaInterpreter()
        interpreter.exec('''
            def fib#1
            if ( arg 1 ) < 2
             arg 1
             ( fib ( ( arg 1 ) - 1 ) ) + ( fib ( ( arg 1 ) - 2 ) )
        ''')
        return interpreter.exec(f'fib {n}')
    
    def fizzbuzz_test(self, n):
        interpreter = PangeaInterpreter()
        interpreter.exec(f'''
            def multiple#2
            0 == ( ( arg 1 ) % ( arg 2 ) )
            
            def i#0
            times_count 1
            
            {n} times (
                "fizzbuzz" when multiple i 15
                "fizz" when multiple i 3
                "buzz" when multiple i 5
                i
            )
        ''')
        return True
    
    def large_array_test(self, size):
        interpreter = PangeaInterpreter()
        elements = " ".join([str(i) for i in range(size)])
        return interpreter.exec(f'[ {elements} ]')
    
    def nested_objects_test(self):
        interpreter = PangeaInterpreter()
        return interpreter.exec('''
            {
                "level1" {
                    "level2" {
                        "level3" {
                            "data" [ 1 2 3 4 5 ]
                            "value" 42
                        }
                    }
                }
                "array" [ { "id" 1 } { "id" 2 } { "id" 3 } ]
            }
        ''')
    
    def array_iteration_test(self):
        interpreter = PangeaInterpreter()
        return interpreter.exec('''
            [ 1 2 3 4 5 6 7 8 9 10 ] each (
                each_item * 2
            )
        ''')
    
    def loop_test(self, iterations):
        interpreter = PangeaInterpreter()
        return interpreter.exec(f'{iterations} times pass')
    
    def recursive_test(self, depth):
        interpreter = PangeaInterpreter()
        interpreter.exec('''
            def countdown#1
            if ( arg 1 ) == 0
             0
             countdown ( ( arg 1 ) - 1 )
        ''')
        return interpreter.exec(f'countdown {depth}')
    
    def conditional_test(self):
        interpreter = PangeaInterpreter()
        return interpreter.exec('''
            print
            "case1" when 1 == 1
            "case2" when 2 == 2  
            "case3" when 3 == 3
            "default"
        ''')
    
    def large_computation_test(self):
        interpreter = PangeaInterpreter()
        # Complex nested computation
        return interpreter.exec('''
            def complex_calc#3
            ( ( arg 1 ) + ( arg 2 ) ) * ( arg 3 ) / 2
            
            complex_calc ( 100 + 200 ) ( 300 - 50 ) ( 75 * 2 )
        ''')
    
    def function_definition_test(self):
        interpreter = PangeaInterpreter()
        # Define multiple functions
        interpreter.exec('''
            def f1#1 arg 1
            def f2#2 ( arg 1 ) + ( arg 2 )
            def f3#3 f2 ( arg 1 ) ( f2 ( arg 2 ) ( arg 3 ) )
        ''')
        return interpreter.exec('f3 1 2 3')
    
    def generate_report(self):
        """Generate detailed performance report"""
        print("\n" + "=" * 50)
        print("📈 PERFORMANCE ANALYSIS REPORT")
        print("=" * 50)
        
        # Overall statistics
        all_times = []
        for result in self.results.values():
            all_times.extend(result['raw_times'])
        
        if all_times:
            print(f"\n📊 Overall Statistics:")
            print(f"Total Tests: {len(self.results)}")
            print(f"Total Measurements: {len(all_times)}")
            print(f"Overall Mean Time: {statistics.mean(all_times):.6f}s")
            print(f"Overall Median Time: {statistics.median(all_times):.6f}s")
        
        # Baseline comparison
        print(f"\n🎯 Baseline Comparison:")
        passed_baselines = 0
        total_baselines = 0
        
        for test_name, baseline_time in self.baseline_expectations.items():
            if test_name in self.results:
                actual_time = self.results[test_name]['mean']
                ratio = actual_time / baseline_time
                status = "PASS" if ratio <= 1.0 else "SLOW"
                print(f"  {test_name}: {ratio:.2f}x baseline ({status})")
                
                if ratio <= 1.0:
                    passed_baselines += 1
                total_baselines += 1
        
        if total_baselines > 0:
            baseline_success_rate = (passed_baselines / total_baselines) * 100
            print(f"\nBaseline Success Rate: {baseline_success_rate:.1f}%")
        
        # Performance recommendations
        print(f"\n💡 Performance Recommendations:")
        
        slow_tests = []
        for name, result in self.results.items():
            baseline = self.baseline_expectations.get(name)
            if baseline and result['mean'] > baseline * 1.5:
                slow_tests.append((name, result['mean'] / baseline))
        
        if slow_tests:
            print("  ⚠️  Tests significantly slower than baseline:")
            for test_name, ratio in slow_tests:
                print(f"    • {test_name}: {ratio:.2f}x slower")
        else:
            print("  ✅ All tests meet or exceed performance expectations!")
        
        # Variability analysis
        high_variability = []
        for name, result in self.results.items():
            if result['stdev'] > result['mean'] * 0.2:  # >20% coefficient of variation
                cv = (result['stdev'] / result['mean']) * 100
                high_variability.append((name, cv))
        
        if high_variability:
            print(f"\n  📊 Tests with high variability (>20% CV):")
            for test_name, cv in high_variability:
                print(f"    • {test_name}: {cv:.1f}% coefficient of variation")
        
        # Save detailed results
        self.save_results_json()
        
        # Final verdict
        print(f"\n🏆 PERFORMANCE VERDICT:")
        
        if baseline_success_rate >= 90:
            print("🚀 EXCELLENT - Ready for production!")
        elif baseline_success_rate >= 75:
            print("✅ GOOD - Minor optimizations recommended")
        elif baseline_success_rate >= 60:
            print("⚠️  FAIR - Performance improvements needed")
        else:
            print("❌ POOR - Significant optimization required")
    
    def save_results_json(self):
        """Save detailed results to JSON file"""
        # Convert results to JSON-serializable format
        json_results = {}
        for name, result in self.results.items():
            json_results[name] = {
                'mean': result['mean'],
                'median': result['median'],
                'stdev': result['stdev'],
                'min': result['min'],
                'max': result['max'],
                'iterations': result['iterations']
            }
        
        # Add metadata
        json_data = {
            'timestamp': time.time(),
            'baseline_expectations': self.baseline_expectations,
            'results': json_results
        }
        
        with open('performance_benchmark_results.json', 'w') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: performance_benchmark_results.json")


def main():
    """Run the performance benchmark suite"""
    try:
        benchmark = PerformanceBenchmark()
        benchmark.run_all_benchmarks()
    except KeyboardInterrupt:
        print("\n⚠️  Benchmark interrupted by user")
    except Exception as e:
        print(f"\n💥 Benchmark suite crashed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
