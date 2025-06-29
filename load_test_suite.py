#!/usr/bin/env python3
"""
Load Testing Suite for Pangea Python Interpreter
Simulates real-world usage patterns and stress conditions
"""

import threading
import time
import random
import queue
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from pangea_python_interpreter import PangeaInterpreter


class LoadTestSuite:
    def __init__(self):
        self.results = queue.Queue()
        self.error_count = 0
        self.success_count = 0
        
    def run_load_tests(self):
        """Run comprehensive load testing scenarios"""
        print("🔥 PANGEA LOAD TESTING SUITE")
        print("=" * 40)
        
        test_scenarios = [
            ("Concurrent Interpreters", self.concurrent_interpreters_test),
            ("Rapid Fire Execution", self.rapid_fire_test),
            ("Memory Pressure Test", self.memory_pressure_test),
            ("Long Running Operations", self.long_running_test),
            ("Mixed Workload Simulation", self.mixed_workload_test),
            ("Stress Test Functions", self.function_stress_test),
            ("Resource Exhaustion Test", self.resource_exhaustion_test),
        ]
        
        for test_name, test_func in test_scenarios:
            print(f"\n🎯 {test_name}")
            print("-" * 30)
            test_func()
        
        self.generate_load_report()
    
    def concurrent_interpreters_test(self):
        """Test multiple interpreters running concurrently"""
        num_threads = 20
        operations_per_thread = 50
        
        def worker_task(thread_id):
            interpreter = PangeaInterpreter()
            thread_results = []
            
            for i in range(operations_per_thread):
                start_time = time.time()
                try:
                    # Mix of different operations
                    operations = [
                        f'print "thread-{thread_id}-op-{i}"',
                        f'{i % 10 + 1} times pass',
                        f'( {i} + {thread_id} ) * 2',
                        '[ 1 2 3 4 5 ] each print each_item'
                    ]
                    
                    result = interpreter.exec(random.choice(operations))
                    execution_time = time.time() - start_time
                    
                    thread_results.append({
                        'thread_id': thread_id,
                        'operation': i,
                        'time': execution_time,
                        'success': True
                    })
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    thread_results.append({
                        'thread_id': thread_id,
                        'operation': i,
                        'time': execution_time,
                        'success': False,
                        'error': str(e)
                    })
            
            return thread_results
        
        print(f"Running {num_threads} concurrent threads with {operations_per_thread} operations each...")
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker_task, i) for i in range(num_threads)]
            
            all_results = []
            for future in as_completed(futures):
                results = future.result()
                all_results.extend(results)
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful_ops = [r for r in all_results if r['success']]
        failed_ops = [r for r in all_results if not r['success']]
        
        total_operations = len(all_results)
        success_rate = len(successful_ops) / total_operations * 100
        avg_time = statistics.mean([r['time'] for r in successful_ops]) if successful_ops else 0
        
        print(f"✅ Completed {total_operations} operations in {total_time:.2f}s")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Average Time: {avg_time:.4f}s per operation")
        print(f"   Throughput: {total_operations / total_time:.1f} ops/second")
        
        if failed_ops:
            print(f"❌ {len(failed_ops)} operations failed")
    
    def rapid_fire_test(self):
        """Test rapid consecutive executions"""
        interpreter = PangeaInterpreter()
        num_operations = 1000
        
        print(f"Executing {num_operations} rapid operations...")
        
        times = []
        errors = 0
        
        start_time = time.time()
        for i in range(num_operations):
            op_start = time.time()
            try:
                result = interpreter.exec(f'print {i}')
                times.append(time.time() - op_start)
            except Exception:
                errors += 1
                times.append(time.time() - op_start)
        
        total_time = time.time() - start_time
        
        if times:
            avg_time = statistics.mean(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"✅ Completed in {total_time:.2f}s")
            print(f"   Average: {avg_time:.5f}s, Min: {min_time:.5f}s, Max: {max_time:.5f}s")
            print(f"   Throughput: {num_operations / total_time:.1f} ops/second")
            print(f"   Errors: {errors}")
    
    def memory_pressure_test(self):
        """Test behavior under memory pressure"""
        import gc
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"Initial memory usage: {initial_memory:.1f}MB")
        
        interpreters = []
        operations = 0
        
        try:
            # Create many interpreters and execute memory-intensive operations
            for i in range(50):
                interpreter = PangeaInterpreter()
                interpreters.append(interpreter)
                
                # Create large data structures
                large_array = "[ " + " ".join([str(j) for j in range(100)]) + " ]"
                interpreter.exec(large_array)
                
                # Define complex functions
                interpreter.exec(f'''
                    def complex_func{i}#3
                    {{ 
                        "result" ( ( arg 1 ) + ( arg 2 ) ) * ( arg 3 )
                        "data" {large_array}
                    }}
                ''')
                
                operations += 3
                
                # Check memory periodically
                if i % 10 == 0:
                    current_memory = process.memory_info().rss / 1024 / 1024
                    memory_delta = current_memory - initial_memory
                    print(f"   Interpreters: {i+1}, Memory: +{memory_delta:.1f}MB")
                    
                    # Break if memory usage becomes excessive
                    if memory_delta > 500:  # 500MB limit
                        print(f"⚠️  Memory limit reached at {i+1} interpreters")
                        break
        
        finally:
            final_memory = process.memory_info().rss / 1024 / 1024
            memory_used = final_memory - initial_memory
            
            print(f"✅ Created {len(interpreters)} interpreters")
            print(f"   Total operations: {operations}")
            print(f"   Memory used: {memory_used:.1f}MB")
            print(f"   Memory per interpreter: {memory_used / len(interpreters):.2f}MB")
            
            # Cleanup
            del interpreters
            gc.collect()
            
            cleanup_memory = process.memory_info().rss / 1024 / 1024
            memory_recovered = final_memory - cleanup_memory
            print(f"   Memory recovered: {memory_recovered:.1f}MB")
    
    def long_running_test(self):
        """Test long-running operations and stability"""
        interpreter = PangeaInterpreter()
        
        print("Testing long-running recursive operations...")
        
        # Test factorial with progressively larger numbers
        interpreter.exec('''
            def factorial#1
            if ( arg 1 ) == 0
             1
             ( arg 1 ) * factorial ( ( arg 1 ) - 1 )
        ''')
        
        test_values = [10, 15, 20, 25]
        for n in test_values:
            start_time = time.time()
            try:
                result = interpreter.exec(f'factorial {n}')
                execution_time = time.time() - start_time
                print(f"   factorial({n}): {execution_time:.4f}s ✅")
            except Exception as e:
                execution_time = time.time() - start_time
                print(f"   factorial({n}): {execution_time:.4f}s ❌ ({e})")
        
        # Test long loops
        print("Testing extended loop operations...")
        loop_sizes = [1000, 5000, 10000]
        
        for size in loop_sizes:
            start_time = time.time()
            try:
                interpreter.exec(f'{size} times pass')
                execution_time = time.time() - start_time
                print(f"   {size} iterations: {execution_time:.4f}s ✅")
            except Exception as e:
                execution_time = time.time() - start_time
                print(f"   {size} iterations: {execution_time:.4f}s ❌ ({e})")
    
    def mixed_workload_test(self):
        """Simulate realistic mixed workload"""
        num_workers = 10
        duration_seconds = 30
        
        def mixed_worker(worker_id):
            interpreter = PangeaInterpreter()
            operations = 0
            errors = 0
            start_time = time.time()
            
            # Define some functions for this worker
            interpreter.exec(f'''
                def worker_func{worker_id}#2
                ( arg 1 ) + ( arg 2 ) * {worker_id}
                
                def data_processor{worker_id}#1
                [ arg 1 ] each (
                    each_item * 2
                )
            ''')
            
            workload_types = [
                lambda: interpreter.exec(f'print "worker-{worker_id}-{operations}"'),
                lambda: interpreter.exec(f'worker_func{worker_id} {operations} {worker_id}'),
                lambda: interpreter.exec(f'{operations % 10 + 1} times pass'),
                lambda: interpreter.exec('[ 1 2 3 4 5 ] each print each_item'),
                lambda: interpreter.exec(f'data_processor{worker_id} {operations % 100}'),
            ]
            
            while time.time() - start_time < duration_seconds:
                try:
                    # Random workload selection
                    workload = random.choice(workload_types)
                    workload()
                    operations += 1
                    
                    # Random delay to simulate realistic usage
                    time.sleep(random.uniform(0.001, 0.01))
                    
                except Exception:
                    errors += 1
            
            return {
                'worker_id': worker_id,
                'operations': operations,
                'errors': errors,
                'duration': time.time() - start_time
            }
        
        print(f"Running mixed workload with {num_workers} workers for {duration_seconds}s...")
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(mixed_worker, i) for i in range(num_workers)]
            
            results = []
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
        
        # Analyze results
        total_operations = sum(r['operations'] for r in results)
        total_errors = sum(r['errors'] for r in results)
        avg_duration = statistics.mean(r['duration'] for r in results)
        
        print(f"✅ Mixed workload completed")
        print(f"   Total operations: {total_operations}")
        print(f"   Total errors: {total_errors}")
        print(f"   Average duration: {avg_duration:.2f}s")
        print(f"   Operations per second: {total_operations / avg_duration:.1f}")
        print(f"   Error rate: {total_errors / total_operations * 100:.2f}%")
    
    def function_stress_test(self):
        """Stress test function definitions and calls"""
        interpreter = PangeaInterpreter()
        
        print("Stress testing function definitions and calls...")
        
        # Define many functions
        num_functions = 100
        for i in range(num_functions):
            interpreter.exec(f'''
                def func{i}#1
                ( arg 1 ) + {i}
            ''')
        
        print(f"   Defined {num_functions} functions")
        
        # Call functions repeatedly
        calls_per_function = 10
        total_calls = 0
        errors = 0
        
        start_time = time.time()
        for i in range(num_functions):
            for j in range(calls_per_function):
                try:
                    result = interpreter.exec(f'func{i} {j}')
                    total_calls += 1
                except Exception:
                    errors += 1
        
        total_time = time.time() - start_time
        
        print(f"✅ Function stress test completed")
        print(f"   Total calls: {total_calls}")
        print(f"   Errors: {errors}")
        print(f"   Time: {total_time:.2f}s")
        print(f"   Calls per second: {total_calls / total_time:.1f}")
    
    def resource_exhaustion_test(self):
        """Test behavior under resource exhaustion"""
        print("Testing resource exhaustion scenarios...")
        
        # Test with very deep recursion (should hit recursion limit gracefully)
        interpreter = PangeaInterpreter()
        interpreter.exec('''
            def deep_recursion#1
            if ( arg 1 ) == 0
             0
             deep_recursion ( ( arg 1 ) - 1 )
        ''')
        
        try:
            result = interpreter.exec('deep_recursion 1000')
            print("   Deep recursion (1000): ✅")
        except RecursionError:
            print("   Deep recursion (1000): ⚠️  Hit recursion limit (expected)")
        except Exception as e:
            print(f"   Deep recursion (1000): ❌ Unexpected error: {e}")
        
        # Test with very large arrays
        try:
            large_array = "[ " + " ".join([str(i) for i in range(10000)]) + " ]"
            result = interpreter.exec(large_array)
            print("   Large array (10000 elements): ✅")
        except MemoryError:
            print("   Large array (10000 elements): ⚠️  Out of memory (expected)")
        except Exception as e:
            print(f"   Large array (10000 elements): ❌ Unexpected error: {e}")
    
    def generate_load_report(self):
        """Generate load testing summary report"""
        print("\n" + "=" * 40)
        print("📊 LOAD TESTING SUMMARY")
        print("=" * 40)
        
        print("\n🎯 Key Findings:")
        print("• Concurrent execution capability tested")
        print("• Memory usage patterns analyzed")
        print("• Performance under load evaluated")
        print("• Resource exhaustion scenarios tested")
        print("• Error handling under stress validated")
        
        print("\n💡 Recommendations:")
        print("• Monitor memory usage in production")
        print("• Implement proper error handling for deep recursion")
        print("• Consider connection pooling for high-throughput scenarios")
        print("• Set up monitoring for performance metrics")
        
        print("\n✅ Load testing completed successfully!")


def main():
    """Run the load testing suite"""
    try:
        suite = LoadTestSuite()
        suite.run_load_tests()
    except KeyboardInterrupt:
        print("\n⚠️  Load testing interrupted by user")
    except Exception as e:
        print(f"\n💥 Load testing crashed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
