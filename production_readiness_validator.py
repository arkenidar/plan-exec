#!/usr/bin/env python3
"""
Production Readiness Validation for Pangea Python Interpreter
Comprehensive checklist and validation for v1.0.0 release
"""

import os
import sys
import subprocess
import importlib.util
import ast
import json
import time
import gc
from pathlib import Path


class ProductionReadinessValidator:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = []
        self.critical_issues = []
        
    def run_validation(self):
        """Run comprehensive production readiness validation"""
        print("🔍 PRODUCTION READINESS VALIDATION")
        print("=" * 50)
        
        validation_categories = [
            ("Code Quality Checks", self.code_quality_checks),
            ("Documentation Completeness", self.documentation_checks),
            ("Test Coverage Validation", self.test_coverage_checks),
            ("Performance Requirements", self.performance_requirements),
            ("Error Handling Robustness", self.error_handling_checks),
            ("API Stability", self.api_stability_checks),
            ("Security Considerations", self.security_checks),
            ("Deployment Readiness", self.deployment_checks),
        ]
        
        for category_name, check_func in validation_categories:
            print(f"\n📋 {category_name}")
            print("-" * 40)
            check_func()
        
        self.generate_final_report()
    
    def check(self, description, condition, critical=False):
        """Record a validation check result"""
        if condition:
            print(f"✅ {description}")
            self.checks_passed += 1
            return True
        else:
            symbol = "🔴" if critical else "⚠️"
            print(f"{symbol} {description}")
            self.checks_failed += 1
            
            if critical:
                self.critical_issues.append(description)
            else:
                self.warnings.append(description)
            return False
    
    def code_quality_checks(self):
        """Validate code quality standards"""
        
        # Check if main interpreter file exists and is valid Python
        interpreter_path = "pangea_python_interpreter.py"
        main_exists = os.path.exists(interpreter_path)
        self.check("Main interpreter file exists", main_exists, critical=True)
        
        if main_exists:
            # Validate Python syntax
            try:
                with open(interpreter_path, 'r') as f:
                    code = f.read()
                ast.parse(code)
                syntax_valid = True
            except SyntaxError:
                syntax_valid = False
            
            self.check("Python syntax is valid", syntax_valid, critical=True)
            
            # Check for docstrings
            has_module_docstring = '"""' in code and code.strip().startswith('#!/usr/bin/env python3')
            self.check("Module has proper docstring", has_module_docstring)
            
            # Check for type hints
            has_type_hints = "from typing import" in code
            self.check("Uses type hints", has_type_hints)
            
            # Check for error handling
            has_try_except = "try:" in code and "except" in code
            self.check("Contains error handling", has_try_except)
            
            # Check for proper imports
            has_proper_imports = all(lib in code for lib in ["import json", "import re"])
            self.check("Has required imports", has_proper_imports)
        
        # Check CLI exists
        cli_exists = os.path.exists("pangea_cli.py")
        self.check("CLI interface exists", cli_exists)
        
        # Check for test files
        test_exists = os.path.exists("test_pangea_interpreter.py")
        self.check("Test suite exists", test_exists)
    
    def documentation_checks(self):
        """Validate documentation completeness"""
        
        # Core documentation files
        readme_exists = os.path.exists("README.md")
        self.check("README.md exists", readme_exists, critical=True)
        
        changelog_exists = os.path.exists("CHANGELOG.md")
        self.check("CHANGELOG.md exists", changelog_exists)
        
        pangea_readme_exists = os.path.exists("README_PANGEA.md")
        self.check("Pangea-specific README exists", pangea_readme_exists)
        
        # Check README content quality
        if readme_exists:
            with open("README.md", 'r') as f:
                readme_content = f.read()
            
            has_title = "# " in readme_content
            self.check("README has proper title", has_title)
            
            has_examples = "```" in readme_content
            self.check("README contains code examples", has_examples)
            
            has_installation = any(word in readme_content.lower() 
                                 for word in ["install", "setup", "getting started"])
            self.check("README has installation instructions", has_installation)
            
            has_usage = any(word in readme_content.lower() 
                          for word in ["usage", "how to", "example"])
            self.check("README explains usage", has_usage)
        
        # Check for example files
        sample_exists = os.path.exists("sample.pangea")
        self.check("Sample Pangea file exists", sample_exists)
        
        # Development docs
        dev_docs_exist = os.path.exists("DEVELOPMENT.md")
        self.check("Development documentation exists", dev_docs_exist)
        
        contributing_exists = os.path.exists("CONTRIBUTING.md")
        self.check("Contributing guidelines exist", contributing_exists)
    
    def test_coverage_checks(self):
        """Validate test coverage and quality"""
        
        # Test file existence
        test_files = [
            "test_pangea_interpreter.py",
            "stress_test_suite.py",
            "performance_benchmark.py"
        ]
        
        for test_file in test_files:
            exists = os.path.exists(test_file)
            self.check(f"Test file {test_file} exists", exists)
        
        # Try to run basic tests
        try:
            import pangea_python_interpreter
            interpreter = pangea_python_interpreter.PangeaInterpreter()
            
            # Test basic functionality
            result = interpreter.exec('print "test"')
            basic_test_works = True
        except Exception as e:
            basic_test_works = False
        
        self.check("Basic interpreter functionality works", basic_test_works, critical=True)
        
        # Test mathematical operations
        try:
            result = interpreter.exec('2 + 3')
            math_works = True
        except Exception:
            math_works = False
        
        self.check("Mathematical operations work", math_works)
        
        # Test function definitions
        try:
            interpreter.exec('def test#1 arg 1')
            interpreter.exec('test 42')
            functions_work = True
        except Exception:
            functions_work = False
        
        self.check("Function definitions work", functions_work)
        
        # Test control flow
        try:
            interpreter.exec('3 times pass')
            control_flow_works = True
        except Exception:
            control_flow_works = False
        
        self.check("Control flow (times) works", control_flow_works)
    
    def performance_requirements(self):
        """Validate performance meets production requirements"""
        
        try:
            from pangea_python_interpreter import PangeaInterpreter
            import time
            
            # Test startup time
            start_time = time.time()
            interpreter = PangeaInterpreter()
            startup_time = time.time() - start_time
            
            startup_fast = startup_time < 0.1  # Should start in under 100ms
            self.check(f"Fast startup time ({startup_time:.3f}s < 0.1s)", startup_fast)
            
            # Test simple execution speed
            start_time = time.time()
            interpreter.exec('print "performance test"')
            exec_time = time.time() - start_time
            
            exec_fast = exec_time < 0.01  # Should execute simple commands in under 10ms
            self.check(f"Fast execution time ({exec_time:.4f}s < 0.01s)", exec_fast)
            
            # Test memory efficiency (basic check)
            import sys
            initial_objects = len(gc.get_objects()) if 'gc' in sys.modules else 0
            
            # Create multiple interpreters
            interpreters = [PangeaInterpreter() for _ in range(10)]
            final_objects = len(gc.get_objects()) if 'gc' in sys.modules else 0
            
            # Rough memory efficiency check
            memory_reasonable = (final_objects - initial_objects) < 10000
            self.check("Memory usage is reasonable", memory_reasonable)
            
        except ImportError:
            self.check("Performance tests (interpreter import failed)", False, critical=True)
        except Exception as e:
            self.check(f"Performance tests (error: {str(e)})", False)
    
    def error_handling_checks(self):
        """Validate error handling robustness"""
        
        try:
            from pangea_python_interpreter import PangeaInterpreter
            interpreter = PangeaInterpreter()
            
            # Test graceful handling of undefined functions
            try:
                interpreter.exec('undefined_function 42')
                # Should not crash, might print error message
                undefined_handled = True
            except SystemExit:
                undefined_handled = False
            except Exception:
                undefined_handled = True  # Graceful exception is acceptable
            
            self.check("Handles undefined functions gracefully", undefined_handled)
            
            # Test malformed syntax handling
            try:
                interpreter.exec('( ( ( incomplete')
                malformed_handled = True
            except SystemExit:
                malformed_handled = False
            except Exception:
                malformed_handled = True
            
            self.check("Handles malformed syntax gracefully", malformed_handled)
            
            # Test empty input
            try:
                result = interpreter.exec('')
                empty_handled = True
            except Exception:
                empty_handled = False
            
            self.check("Handles empty input gracefully", empty_handled)
            
        except ImportError:
            self.check("Error handling tests (import failed)", False, critical=True)
    
    def api_stability_checks(self):
        """Validate API stability for v1.0.0"""
        
        try:
            from pangea_python_interpreter import PangeaInterpreter
            
            # Check main class exists
            main_class_exists = PangeaInterpreter is not None
            self.check("Main PangeaInterpreter class exists", main_class_exists, critical=True)
            
            if main_class_exists:
                interpreter = PangeaInterpreter()
                
                # Check required methods exist
                required_methods = ['exec', 'parse_code', 'word_exec']
                for method in required_methods:
                    has_method = hasattr(interpreter, method)
                    self.check(f"Has {method} method", has_method, critical=True)
                
                # Check exec method accepts string
                try:
                    interpreter.exec('pass')
                    exec_api_stable = True
                except TypeError:
                    exec_api_stable = False
                
                self.check("exec() method has stable API", exec_api_stable, critical=True)
                
                # Check namespace structure
                has_namespace = hasattr(interpreter, 'namespace')
                self.check("Has namespace attribute", has_namespace)
                
                if has_namespace:
                    ns_has_stack = 'stack' in interpreter.namespace
                    self.check("Namespace has stack", ns_has_stack)
        
        except ImportError:
            self.check("API stability tests (import failed)", False, critical=True)
    
    def security_checks(self):
        """Basic security considerations for production"""
        
        # Check for obvious security issues in code
        if os.path.exists("pangea_python_interpreter.py"):
            with open("pangea_python_interpreter.py", 'r') as f:
                code = f.read()
            
            # Check for dangerous operations
            no_eval = "eval(" not in code
            self.check("Does not use eval()", no_eval)
            
            no_exec = "exec(" not in code  # Built-in exec, not our method
            self.check("Does not use builtin exec()", no_exec)
            
            no_import_star = "import *" not in code
            self.check("No wildcard imports", no_import_star)
            
            # Check for input validation
            has_validation = any(word in code for word in ["isinstance", "type", "validate"])
            self.check("Contains input validation", has_validation)
        
        # Check file permissions (if on Unix-like system)
        if hasattr(os, 'access'):
            files_not_executable = True
            for file in ["pangea_python_interpreter.py", "pangea_cli.py"]:
                if os.path.exists(file):
                    if os.access(file, os.X_OK) and not file.endswith('.py'):
                        files_not_executable = False
            
            self.check("Python files have appropriate permissions", files_not_executable)
    
    def deployment_checks(self):
        """Validate deployment readiness"""
        
        # Check for requirements file or dependency documentation
        has_requirements = any(os.path.exists(f) for f in ["requirements.txt", "pyproject.toml", "setup.py"])
        self.check("Has dependency specification", has_requirements)
        
        # Check Python version compatibility
        import sys
        python_version_ok = sys.version_info >= (3, 6)
        self.check(f"Python version compatible (current: {sys.version})", python_version_ok)
        
        # Check for CLI executable
        cli_exists = os.path.exists("pangea_cli.py")
        if cli_exists:
            with open("pangea_cli.py", 'r') as f:
                cli_content = f.read()
            
            has_shebang = cli_content.startswith("#!/usr/bin/env python3")
            self.check("CLI has proper shebang", has_shebang)
            
            has_main_guard = 'if __name__ == "__main__":' in cli_content
            self.check("CLI has main guard", has_main_guard)
        
        # Check for version information
        version_info_exists = any(
            word in open("README.md", 'r').read() if os.path.exists("README.md") else ""
            for word in ["v1.0.0", "version", "release"]
        )
        self.check("Version information documented", version_info_exists)
        
        # Check git repository status
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, timeout=5)
            git_clean = len(result.stdout.strip()) == 0
            self.check("Git repository is clean", git_clean)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.check("Git repository status (git not available)", None)
        
        # Check for release tag
        try:
            result = subprocess.run(['git', 'tag', '--list'], 
                                  capture_output=True, text=True, timeout=5)
            has_release_tag = 'v1.0.0' in result.stdout
            self.check("Has release tag (v1.0.0)", has_release_tag)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.check("Release tag check (git not available)", None)
    
    def generate_final_report(self):
        """Generate final production readiness report"""
        print("\n" + "=" * 50)
        print("🎯 PRODUCTION READINESS REPORT")
        print("=" * 50)
        
        total_checks = self.checks_passed + self.checks_failed
        success_rate = (self.checks_passed / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n📊 Overall Results:")
        print(f"Total Checks: {total_checks}")
        print(f"Passed: {self.checks_passed} ✅")
        print(f"Failed: {self.checks_failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Critical issues
        if self.critical_issues:
            print(f"\n🔴 CRITICAL ISSUES (Must Fix):")
            for issue in self.critical_issues:
                print(f"  • {issue}")
        
        # Warnings
        if self.warnings:
            print(f"\n⚠️  WARNINGS (Recommended to Fix):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        # Final verdict
        print(f"\n🏆 PRODUCTION READINESS VERDICT:")
        
        if self.critical_issues:
            print("❌ NOT READY - Critical issues must be resolved")
        elif success_rate >= 95:
            print("🚀 PRODUCTION READY - All systems go!")
        elif success_rate >= 85:
            print("✅ MOSTLY READY - Minor issues to address")
        elif success_rate >= 70:
            print("⚠️  NEEDS WORK - Several improvements required")
        else:
            print("❌ NOT READY - Major improvements needed")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if success_rate >= 95:
            print("  🎉 Ready for v1.0.0 release!")
            print("  📦 Proceed with packaging and distribution")
            print("  📢 Prepare release announcement")
        elif success_rate >= 85:
            print("  🔧 Address remaining warnings")
            print("  🧪 Run additional testing")
            print("  📝 Update documentation as needed")
        else:
            print("  🛠️  Focus on critical issues first")
            print("  📋 Create improvement roadmap")
            print("  🔄 Re-run validation after fixes")
        
        # Save report
        report_data = {
            'timestamp': time.time(),
            'total_checks': total_checks,
            'checks_passed': self.checks_passed,
            'checks_failed': self.checks_failed,
            'success_rate': success_rate,
            'critical_issues': self.critical_issues,
            'warnings': self.warnings
        }
        
        with open('production_readiness_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: production_readiness_report.json")


def main():
    """Run production readiness validation"""
    import time
    
    try:
        validator = ProductionReadinessValidator()
        validator.run_validation()
    except KeyboardInterrupt:
        print("\n⚠️  Validation interrupted by user")
    except Exception as e:
        print(f"\n💥 Validation crashed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
