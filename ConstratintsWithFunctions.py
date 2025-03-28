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

   

    # =============================================
    # Run All Analyses
    # =============================================
    division_by_zero_analysis()
    

if __name__ == "__main__":
    analyze_program_with_functions()