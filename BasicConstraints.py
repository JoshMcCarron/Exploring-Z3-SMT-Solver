from z3 import *

def detect_bugs():
    # Initialize Z3 solver
    solver = Solver()

    # Example 1: Division by zero detection
    def detect_division_by_zero():
        x = Int('x')
        solver.push()
        solver.add(x == 0)  # Potential division by zero
        condition = Not(x == 0)  # Safe condition: x ≠ 0
        solver.add(Not(condition))  # Check if x can be 0
        if solver.check() == sat:
            print("⚠️ Division by zero possible! (x = 0)")
        else:
            print("✅ No division by zero detected.")
        solver.pop()

    # Example 2: Array out-of-bounds detection
    def detect_array_oob():
        arr_size = 10
        index = Int('index')
        solver.push()
        solver.add(index < 0)  # Check negative index
        if solver.check() == sat:
            print(f"⚠️ Array out-of-bounds (negative index: {solver.model()[index]})")
        solver.pop()
        
        solver.push()
        solver.add(index >= arr_size)  # Check index ≥ array size
        if solver.check() == sat:
            print(f"⚠️ Array out-of-bounds (index too large: {solver.model()[index]})")
        solver.pop()

   

    # Run all checks
    detect_division_by_zero()
    detect_array_oob()


if __name__ == "__main__":
    detect_bugs()