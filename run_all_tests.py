#!/usr/bin/env python3
"""
Master Test Runner for Pangea Python Interpreter
Executes comprehensive stress testing suite to validate production readiness
"""

import sys
import time
import subprocess
import os
import traceback
from pathlib import Path


class MasterTestRunner:
    def __init__(self):
        self.test_results = {}
        self.overall_start_time = time.time()
        
    def run_comprehensive_testing(self):
        """Run all stress tests and validation suites"""
        print("🚀 PANGEA PYTHON INTERPRETER - COMPREHENSIVE TESTING SUITE")
        print("=" * 70)
        print(f"Testing environment: Python {sys.version}")
        print(f"Working directory: {os.getcwd()}")
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Test suites to run
        test_suites = [
            {
                'name': 'Production Readiness Validation',
                'file': 'production_readiness_validator.py',
                'description': 'Validates production readiness checklist',
                'critical': True
            },
            {
                'name': 'Core Functionality Tests',
                'file': 'test_pangea_interpreter.py',
                'description': 'Tests basic interpreter functionality',
                'critical': True
            },
            {
                'name': 'Stress Testing Suite',
                'file': 'stress_test_suite.py',
                'description': 'Comprehensive stress testing scenarios',
                'critical': False
            },
            {
                'name': 'Performance Benchmarks',
                'file': 'performance_benchmark.py',
                'description': 'Performance analysis and benchmarking',
                'critical': False
            },
            {
                'name': 'Load Testing Suite',
                'file': 'load_test_suite.py',
                'description': 'Load testing and concurrent execution',
                'critical': False
            }
        ]
        
        # Execute each test suite
        for suite in test_suites:
            self.run_test_suite(suite)
        
        # Generate final report
        self.generate_master_report()
    
    def run_test_suite(self, suite_config):
        """Run an individual test suite"""
        name = suite_config['name']
        file = suite_config['file']
        description = suite_config['description']
        critical = suite_config['critical']
        
        print(f"\n{'🔴' if critical else '🟡'} {name}")
        print("-" * 50)
        print(f"Description: {description}")
        print(f"File: {file}")
        print(f"Critical: {'Yes' if critical else 'No'}")
        
        if not os.path.exists(file):
            result = {
                'status': 'MISSING',
                'exit_code': -1,
                'duration': 0,
                'output': f"Test file {file} not found",
                'critical': critical
            }
            print(f"❌ MISSING: Test file {file} not found")
        else:
            result = self.execute_test_file(file, critical)
        
        self.test_results[name] = result
        
        # Print result summary
        status_symbol = {
            'PASS': '✅',
            'FAIL': '❌',
            'ERROR': '💥',
            'MISSING': '📄'
        }.get(result['status'], '❓')
        
        print(f"\n{status_symbol} {result['status']}: {name}")
        print(f"   Duration: {result['duration']:.2f}s")
        if result['exit_code'] != 0:
            print(f"   Exit code: {result['exit_code']}")
    
    def execute_test_file(self, file_path, critical):
        """Execute a test file and capture results"""
        print(f"Executing: python3 {file_path}")
        
        start_time = time.time()
        
        try:
            # Run the test with timeout
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=os.getcwd()
            )
            
            duration = time.time() - start_time
            
            # Determine status based on exit code
            if result.returncode == 0:
                status = 'PASS'
            else:
                status = 'FAIL'
            
            return {
                'status': status,
                'exit_code': result.returncode,
                'duration': duration,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'critical': critical
            }
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            print(f"⏰ Test timed out after {duration:.1f}s")
            
            return {
                'status': 'ERROR',
                'exit_code': -2,
                'duration': duration,
                'output': 'Test timed out',
                'critical': critical
            }
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"💥 Test execution failed: {e}")
            
            return {
                'status': 'ERROR',
                'exit_code': -3,
                'duration': duration,
                'output': str(e),
                'critical': critical
            }
    
    def generate_master_report(self):
        """Generate comprehensive master testing report"""
        total_duration = time.time() - self.overall_start_time
        
        print("\n" + "=" * 70)
        print("🏆 MASTER TESTING REPORT")
        print("=" * 70)
        
        # Overall statistics
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results.values() if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results.values() if r['status'] == 'FAIL'])
        error_tests = len([r for r in self.test_results.values() if r['status'] == 'ERROR'])
        missing_tests = len([r for r in self.test_results.values() if r['status'] == 'MISSING'])
        
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"Total Test Suites: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Errors: {error_tests} 💥")
        print(f"Missing: {missing_tests} 📄")
        print(f"Total Duration: {total_duration:.2f}s")
        
        # Success rate
        if total_tests > 0:
            success_rate = (passed_tests / total_tests) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        # Critical tests analysis
        critical_tests = {name: result for name, result in self.test_results.items() if result['critical']}
        critical_passed = len([r for r in critical_tests.values() if r['status'] == 'PASS'])
        critical_total = len(critical_tests)
        
        print(f"\n🔴 CRITICAL TESTS:")
        print(f"Critical Passed: {critical_passed}/{critical_total}")
        
        if critical_total > 0:
            critical_success_rate = (critical_passed / critical_total) * 100
            print(f"Critical Success Rate: {critical_success_rate:.1f}%")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for name, result in self.test_results.items():
            status_symbol = {
                'PASS': '✅',
                'FAIL': '❌', 
                'ERROR': '💥',
                'MISSING': '📄'
            }.get(result['status'], '❓')
            
            critical_marker = "🔴" if result['critical'] else "🟡"
            print(f"  {status_symbol} {critical_marker} {name}: {result['status']} ({result['duration']:.2f}s)")
            
            # Show errors for failed tests
            if result['status'] in ['FAIL', 'ERROR'] and 'stderr' in result and result['stderr']:
                error_lines = result['stderr'].split('\n')[:3]  # First 3 lines of error
                for line in error_lines:
                    if line.strip():
                        print(f"      {line.strip()}")
        
        # Final verdict
        print(f"\n🎯 PRODUCTION READINESS VERDICT:")
        
        all_critical_passed = all(r['status'] == 'PASS' for r in critical_tests.values())
        overall_success = success_rate >= 80 if total_tests > 0 else False
        
        if all_critical_passed and overall_success:
            verdict = "🚀 PRODUCTION READY"
            recommendation = "All critical tests passed. Ready for v1.0.0 release!"
        elif all_critical_passed:
            verdict = "⚠️  MOSTLY READY"
            recommendation = "Critical tests passed, but some non-critical issues exist."
        elif critical_success_rate >= 50:
            verdict = "🔧 NEEDS WORK"
            recommendation = "Some critical issues need to be addressed before release."
        else:
            verdict = "❌ NOT READY"
            recommendation = "Major critical issues must be fixed before release."
        
        print(f"{verdict}")
        print(f"Recommendation: {recommendation}")
        
        # Performance summary
        avg_duration = sum(r['duration'] for r in self.test_results.values()) / len(self.test_results)
        print(f"\n⚡ PERFORMANCE SUMMARY:")
        print(f"Average test duration: {avg_duration:.2f}s")
        print(f"Longest test: {max(r['duration'] for r in self.test_results.values()):.2f}s")
        print(f"Shortest test: {min(r['duration'] for r in self.test_results.values()):.2f}s")
        
        # Save detailed report
        self.save_detailed_report()
        
        print(f"\n💾 Detailed report saved to: master_test_report.json")
        print(f"📊 Test logs available in individual test output files")
        
        # Exit with appropriate code
        if all_critical_passed and overall_success:
            print(f"\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
            return 0
        else:
            print(f"\n⚠️  SOME TESTS FAILED - Review results above")
            return 1
    
    def save_detailed_report(self):
        """Save detailed test results to JSON file"""
        import json
        
        report_data = {
            'timestamp': time.time(),
            'total_duration': time.time() - self.overall_start_time,
            'python_version': sys.version,
            'working_directory': os.getcwd(),
            'test_results': {}
        }
        
        # Convert results to JSON-serializable format
        for name, result in self.test_results.items():
            report_data['test_results'][name] = {
                'status': result['status'],
                'exit_code': result['exit_code'],
                'duration': result['duration'],
                'critical': result['critical'],
                'has_stdout': 'stdout' in result and bool(result.get('stdout')),
                'has_stderr': 'stderr' in result and bool(result.get('stderr'))
            }
        
        with open('master_test_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
    
    def run_quick_smoke_test(self):
        """Run quick smoke test to verify basic functionality"""
        print("🔥 QUICK SMOKE TEST")
        print("-" * 30)
        
        try:
            from pangea_python_interpreter import PangeaInterpreter
            
            interpreter = PangeaInterpreter()
            
            # Basic tests
            tests = [
                ('Basic print', 'print "smoke test"'),
                ('Arithmetic', '2 + 3'),
                ('Function def', 'def test#1 arg 1'),
                ('Times loop', '3 times pass'),
            ]
            
            for test_name, code in tests:
                try:
                    result = interpreter.exec(code)
                    print(f"✅ {test_name}: OK")
                except Exception as e:
                    print(f"❌ {test_name}: {e}")
                    return False
            
            print("🚀 Smoke test passed - basic functionality working!")
            return True
            
        except ImportError as e:
            print(f"❌ Cannot import interpreter: {e}")
            return False
        except Exception as e:
            print(f"❌ Smoke test failed: {e}")
            return False


def main():
    """Main function - run comprehensive testing"""
    if len(sys.argv) > 1 and sys.argv[1] == '--smoke':
        # Quick smoke test mode
        runner = MasterTestRunner()
        success = runner.run_quick_smoke_test()
        sys.exit(0 if success else 1)
    else:
        # Full comprehensive testing
        try:
            runner = MasterTestRunner()
            exit_code = runner.run_comprehensive_testing()
            sys.exit(exit_code)
        except KeyboardInterrupt:
            print("\n⚠️  Testing interrupted by user")
            sys.exit(130)
        except Exception as e:
            print(f"\n💥 Master test runner crashed: {e}")
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()
