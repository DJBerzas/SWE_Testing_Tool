import ast
import importlib
import os
import sys
import unittest
from copy import deepcopy
from datetime import datetime
import json
import importlib.util

class Mutator:
    def __init__(self, source_file, test_file):
        self.source_file = source_file
        self.test_file = test_file
        with open(source_file, 'r') as f:
            self.source_code = f.read()
        self.original_ast = ast.parse(self.source_code)
        self.mutation_results = []
        self.start_time = None
        self.end_time = None
    
    def create_mutations(self):
        mutations = []
        
        # Define mutation pairs
        operator_mutations = [
            (ast.Add, ast.Sub, '+ to -'),
            (ast.Sub, ast.Add, '- to +'),
            (ast.Mult, ast.Div, '* to /'),
            (ast.Div, ast.Mult, '/ to *'),
            (ast.FloorDiv, ast.Div, '// to /'),
            (ast.Mod, ast.Div, '% to /'),
            (ast.Pow, ast.Mult, '** to *')
        ]
        
        comparison_mutations = [
            (ast.Eq, ast.NotEq, '== to !='),
            (ast.NotEq, ast.Eq, '!= to =='),
            (ast.Lt, ast.Gt, '< to >'),
            (ast.Gt, ast.Lt, '> to <'),
            (ast.LtE, ast.GtE, '<= to >='),
            (ast.GtE, ast.LtE, '>= to <=')
        ]
        
        for node in ast.walk(self.original_ast):
            # Binary operator mutations
            if isinstance(node, ast.BinOp):
                for orig_op, new_op, name in operator_mutations:
                    if isinstance(node.op, orig_op):
                        mutated_ast = deepcopy(self.original_ast)
                        for n in ast.walk(mutated_ast):
                            if isinstance(n, ast.BinOp) and isinstance(n.op, orig_op):
                                n.op = new_op()
                        mutations.append((name, mutated_ast, node.lineno))
            
            # Comparison operator mutations
            if isinstance(node, ast.Compare):
                for i, op in enumerate(node.ops):
                    for orig_op, new_op, name in comparison_mutations:
                        if isinstance(op, orig_op):
                            mutated_ast = deepcopy(self.original_ast)
                            for n in ast.walk(mutated_ast):
                                if isinstance(n, ast.Compare) and len(n.ops) > i:
                                    if isinstance(n.ops[i], orig_op):
                                        n.ops[i] = new_op()
                            mutations.append((name, mutated_ast, node.lineno))
        
        return mutations
    
    def test_mutation(self, mutation_name, mutated_ast, line_number):
        # Create a temporary file with the mutated code
        temp_file = "temp_calculator.py"
        with open(temp_file, 'w') as f:
            f.write(ast.unparse(mutated_ast))
        
        try:
            # Remove any existing imports
            for key in list(sys.modules.keys()):
                if key.startswith('temp_') or key == 'calculator':
                    del sys.modules[key]
            
            # Import the mutated module
            spec = importlib.util.spec_from_file_location("temp_calculator", temp_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules["temp_calculator"] = module
            spec.loader.exec_module(module)
            
            # Modify sys.path to include current directory
            if '.' not in sys.path:
                sys.path.insert(0, '.')
            
            # Run the tests with the mutated module
            test_loader = unittest.TestLoader()
            test_module = __import__('test_calculator')
            importlib.reload(test_module)  # Reload to use new mutated version
            suite = test_loader.loadTestsFromModule(test_module)
            result = unittest.TestResult()
            suite.run(result)
            
            # Record detailed results
            test_result = {
                'mutation': mutation_name,
                'line_number': line_number,
                'caught': not result.wasSuccessful(),
                'failures': len(result.failures),
                'errors': len(result.errors),
                'original_code': self.get_original_line(line_number),
                'mutated_code': self.get_mutated_line(mutated_ast, line_number)
            }
            
            self.mutation_results.append(test_result)
            
            # Print immediate feedback
            status = "CAUGHT" if test_result['caught'] else "NOT CAUGHT"
            print(f"\nMutation '{mutation_name}' at line {line_number} was {status}")
            print(f"Original code: {test_result['original_code'].strip()}")
            print(f"Mutated code: {test_result['mutated_code'].strip()}")
            if test_result['caught']:
                print(f"Test failures: {test_result['failures']}")
                print(f"Test errors: {test_result['errors']}")
        
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
            # Clean up modules
            for key in list(sys.modules.keys()):
                if key.startswith('temp_') or key == 'calculator':
                    del sys.modules[key]
    
    def get_original_line(self, line_number):
        lines = self.source_code.split('\n')
        return lines[line_number - 1] if 0 < line_number <= len(lines) else "Unknown line"
    
    def get_mutated_line(self, mutated_ast, line_number):
        mutated_code = ast.unparse(mutated_ast)
        lines = mutated_code.split('\n')
        return lines[line_number - 1] if 0 < line_number <= len(lines) else "Unknown line"
    
    def generate_report(self):
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        total_mutations = len(self.mutation_results)
        caught_mutations = sum(1 for r in self.mutation_results if r['caught'])
        coverage = (caught_mutations / total_mutations * 100) if total_mutations else 0
        
        report = {
            'timestamp': self.end_time.isoformat(),
            'duration_seconds': duration,
            'source_file': self.source_file,
            'test_file': self.test_file,
            'total_mutations': total_mutations,
            'caught_mutations': caught_mutations,
            'not_caught_mutations': total_mutations - caught_mutations,
            'mutation_coverage': coverage,
            'mutations': self.mutation_results
        }
        
        # Save report to file
        report_file = f"mutation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n=== Mutation Testing Report ===")
        print(f"Total mutations tested: {total_mutations}")
        print(f"Mutations caught: {caught_mutations}")
        print(f"Mutations not caught: {total_mutations - caught_mutations}")
        print(f"Mutation coverage: {coverage:.2f}%")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Detailed report saved to: {report_file}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python mutator.py <source_file> <test_file>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    test_file = sys.argv[2]
    
    mutator = Mutator(source_file, test_file)
    mutator.start_time = datetime.now()
    
    mutations = mutator.create_mutations()
    
    if not mutations:
        print("No mutations could be created for this code.")
        return
    
    print(f"Found {len(mutations)} possible mutations.")
    for mutation_name, mutated_ast, line_number in mutations:
        print(f"\nTesting mutation: {mutation_name}")
        mutator.test_mutation(mutation_name, mutated_ast, line_number)
    
    mutator.generate_report()

if __name__ == '__main__':
    main() 