from z3 import *

def recursion_analyzer():
    print("\n=== Z3 Recursion Analysis ===")
    
    # Create solver
    solver = Solver()
    
    # Define common recursion patterns
    def factorial_model(n, depth):
        """Model for factorial recursion: fact(n) = n * fact(n-1)"""
        return If(n <= 0, 
                 1,  # Base case
                 n * factorial_model(n - 1, depth + 1))  # Recursive case
    
    def fibonacci_model(n, depth):
        """Model for fibonacci recursion: fib(n) = fib(n-1) + fib(n-2)"""
        return If(n <= 1, 
                 n,  # Base case
                 fibonacci_model(n - 1, depth + 1) + fibonacci_model(n - 2, depth + 1))  # Recursive case
    
    def array_traversal_model(array_size, index, depth):
        """Model for recursive array traversal"""
        return If(index >= array_size,
                 0,  # Base case (end of array)
                 1 + array_traversal_model(array_size, index + 1, depth + 1))  # Recursive case
    
    # Recursion checks
    def check_infinite_recursion(func_name, condition, max_depth):
        print(f"\nChecking for infinite recursion in {func_name}...")
        
        # Symbolic variables
        n = Int('n')
        depth = Int('depth')
        
        # Check if recursion goes beyond max_depth
        solver.push()
        solver.add(depth > max_depth)
        solver.add(condition)
        
        if solver.check() == sat:
            model = solver.model()
            actual_depth = model.eval(depth).as_long()
            input_val = model.eval(n).as_long()
            
            print(f"⚠️ Potential infinite recursion detected!")
            print(f"   Function: {func_name}")
            print(f"   Input value: n = {input_val}")
            print(f"   Recursion depth: {actual_depth}")
            print(f"   Exceeds maximum allowed depth: {max_depth}")
        else:
            print(f"✅ No infinite recursion possible within depth {max_depth}")
            
        solver.pop()
    
    def check_missing_base_case(func_name, condition):
        print(f"\nChecking for missing base cases in {func_name}...")
        
        # Symbolic variable
        n = Int('n')
        
        # Check if there are inputs that would miss all base cases
        solver.push()
        solver.add(condition)
        
        if solver.check() == sat:
            model = solver.model()
            problematic_input = model.eval(n).as_long()
            
            print(f"⚠️ Missing base case detected!")
            print(f"   Function: {func_name}")
            print(f"   Problematic input: n = {problematic_input}")
            print(f"   This input may not terminate correctly")
        else:
            print(f"✅ Base cases are comprehensive")
            
        solver.pop()
    
    def check_stack_overflow_risk(func_name, condition, stack_limit):
        print(f"\nChecking for stack overflow risk in {func_name}...")
        
        # Symbolic variables
        n = Int('n')
        depth = Int('depth')
        
        # Stack overflow occurs when recursion depth exceeds stack limit
        solver.push()
        solver.add(depth >= stack_limit)
        solver.add(condition)
        
        if solver.check() == sat:
            model = solver.model()
            overflow_depth = model.eval(depth).as_long()
            input_val = model.eval(n).as_long()
            
            print(f"⚠️ Stack overflow risk detected!")
            print(f"   Function: {func_name}")
            print(f"   Input value: n = {input_val}")
            print(f"   Estimated stack frames: {overflow_depth}")
            print(f"   Exceeds typical stack limit: {stack_limit}")
        else:
            print(f"✅ No stack overflow risk detected within limit {stack_limit}")
            
        solver.pop()
    
    def check_exponential_growth(func_name, condition):
        print(f"\nChecking for exponential call tree growth in {func_name}...")
        
        # Symbolic variables
        n = Int('n')
        calls = Int('calls')
        
        # Exponential growth check
        solver.push()
        solver.add(calls > 100)  # Arbitrary threshold for "many" calls
        solver.add(n < 20)       # With a relatively small input
        solver.add(condition)    # Additional conditions
        
        if solver.check() == sat:
            model = solver.model()
            explosive_input = model.eval(n).as_long()
            estimated_calls = model.eval(calls).as_long()
            
            print(f"⚠️ Exponential call growth detected!")
            print(f"   Function: {func_name}")
            print(f"   Input value: n = {explosive_input}")
            print(f"   Estimated function calls: {estimated_calls}")
            print(f"   This may cause performance issues")
        else:
            print(f"✅ No problematic exponential growth detected")
            
        solver.pop()
    
    # Test different recursion scenarios
    def test_recursion_scenarios():
        # Common variables for all tests
        n = Int('n')
        depth = Int('depth')
        calls = Int('calls')  # Declare 'calls' before using it
        
        # Scenario 1: Factorial recursion
        print("\n--- Scenario 1: Factorial Recursion ---")
        
        # Check for infinite recursion with various conditions
        check_infinite_recursion("factorial", And(n >= 0, depth == n), 100)
        check_infinite_recursion("factorial", n < 0, 10)
        
        # Check for missing base cases
        check_missing_base_case("factorial", And(n != 0, n != 1, n < 0))
        
        # Check for stack overflow
        check_stack_overflow_risk("factorial", And(n >= 0, depth == n), 1000)
        
        # Scenario 2: Fibonacci recursion
        print("\n--- Scenario 2: Fibonacci Recursion ---")
        
        # Fibonacci has exponential growth in naive implementation
        check_exponential_growth("fibonacci", And(n >= 10, calls >= 2**n))  # 'calls' is now defined
        
        # Check for infinite recursion
        check_infinite_recursion("fibonacci", n < 0, 10)

        # Scenario 3: Tree recursion
        print("\n--- Scenario 3: Binary Tree Traversal ---")
        
        # Define symbolic tree depth
        tree_depth = Int('tree_depth')
        tree_nodes = Int('tree_nodes')
        
        # Check for stack overflow in balanced tree traversal
        solver.push()
        solver.add(tree_nodes == 2**tree_depth - 1)  # Nodes in complete binary tree
        check_stack_overflow_risk("tree_traversal",And(tree_depth >= 5, depth == tree_depth), 1000)
        solver.pop()
        
        # Scenario 4: Mutual recursion
        print("\n--- Scenario 4: Mutual Recursion ---")
        
        # Mutual recursion can be hard to analyze
        # Simplify by checking termination conditions
        check_missing_base_case("even_odd_mutual", And(n % 2 == 0, n < 0))
    
    # Run all tests
    test_recursion_scenarios()

if __name__ == "__main__":
    recursion_analyzer()