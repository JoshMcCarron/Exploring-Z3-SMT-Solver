from z3 import *

def analyze_program_with_functions():
    solver = Solver()
    
    # Example 1: Division by zero detection across function calls
    def division_by_zero_analysis():
        print("\n=== Division by Zero Across Functions ===")
        x, y = Ints('x y')
        
        # Function: divide(a, b) returns a/b
        def divide(a, b):
            solver.push()
            solver.add(b == 0)  # Check if denominator can be zero
            if solver.check() == sat:
                print(f"⚠️ Division by zero in divide({a}, {b}) when {b} = 0")
            solver.pop()
            return a / b
        
        # Test case
        solver.add(x > 5)
        result = divide(x, y)  # Function call
        solver.add(y == x - 5)  # Relationship between x and y
        
        if solver.check() == sat:
            m = solver.model()
            print(f"✅ Safe division example: divide({m[x]}, {m[y]}) = {m[x].as_long() / m[y].as_long()}")
        else:
            print("No valid solution found")

   
    # Example 2: Array out-of-bounds detection in nested
    def array_bounds_analysis():
        print("\n=== Array Bounds in Nested Functions ===")
        arr_size = 10
        index1, index2 = Ints('index1 index2')
        arr = Array('arr', IntSort(), IntSort())
        
        # Function: get_element(arr, i) returns arr[i]
        def get_element(array, i):
            solver.push()
            solver.add(Or(i < 0, i >= arr_size))  # Check OOB access
            if solver.check() == sat:
                m = solver.model()
                print(f"⚠️ Array OOB in get_element(arr, {i}) when i = {m[i]}")
            solver.pop()
            return array[i]
        
        # Nested function call
        def process_array(idx1, idx2):
            val1 = get_element(arr, idx1)
            val2 = get_element(arr, idx2)
            return val1 + val2
        
        # Test case
        solver.add(index1 == 15)  # Will trigger OOB
        solver.add(index2 == 3)   # Safe index
        total = process_array(index1, index2)
        
        if solver.check() == sat:
            print(f"Array access result: {total} (but OOB detected above)")


    # Example 3: Assertion Failures Through Call Chains
    def assertion_propagation_analysis():
        print("\n=== Assertion Failure Propagation ===")
        a, b = Ints('a b')
        
        # Function with assertion
        def validate_positive(x):
            solver.push()
            solver.add(x <= 0)  # Check assertion violation
            if solver.check() == sat:
                print(f"⚠️ Assertion failed in validate_positive({x}) when x = {solver.model()[x]}")
            solver.pop()
            return x > 0
        
        # Calling function
        def process_values(x, y):
            check1 = validate_positive(x)
            check2 = validate_positive(y)
            return And(check1, check2)
        
        # Test case
        solver.add(a == 5)
        solver.add(b == -3)  # Will trigger assertion
        result = process_values(a, b)
        
        if solver.check() == sat:
            print(f"Final validation result: {result} (but assertion failed above)")


    # Example 4: Dead Code Detection in Function Flow
    def dead_code_analysis():
        print("\n=== Dead Code Detection ===")
        x, y = Ints('x y')
        
        # Function with unreachable branch
        def process(x, y):
            if x > 10:
                if y < 5:
                    return "Case 1"
                else:
                    return "Case 2"
            else:
                return "Case 3"
            
            # This code is unreachable
            return "Dead Code"
        
        # Analyze reachability
        solver.push()
        solver.add(Not(Or(x > 10, x <= 10)))  # Make entire function unreachable
        if solver.check() == unsat:
            print("✅ No dead code in main function branches")
        else:
            print("⚠️ Dead code detected in function")
        solver.pop()
        
        # Check specific unreachable segment
        solver.push()
        solver.add(And(x > 10, y < 5, y > 10))  # Impossible condition
        if solver.check() == unsat:
            print("⚠️ Dead code detected in nested conditional")
        solver.pop()

    # =============================================
    # Run All Analyses
    # =============================================
    division_by_zero_analysis()
    array_bounds_analysis()
    assertion_propagation_analysis()
    dead_code_analysis()

if __name__ == "__main__":
    analyze_program_with_functions()

# Expected Output:
# === Division by Zero Across Functions ===
# ⚠️ Division by zero in divide(x, y) when y = 0
# ✅ Safe division example: divide(6, 1) = 6.0

# === Array Bounds in Nested Functions ===
# ⚠️ Array OOB in get_element(arr, index1) when i = 15
# Array access result: arr[index1] + arr[index2] (but OOB detected above)

# === Assertion Failure Propagation ===
# ⚠️ Assertion failed in validate_positive(b) when x = -3
# Final validation result: And(a > 0, b > 0) (but assertion failed above)

# === Dead Code Detection ===
# ✅ No dead code in main function branches
# ⚠️ Dead code detected in nested conditional