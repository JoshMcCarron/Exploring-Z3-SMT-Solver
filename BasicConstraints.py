from z3 import *

def detect_bugs():
    # Initialize Z3 solver
    solver = Solver()

    # Example 1: Division by zero detection
    #
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



    # Run all checks
    detect_division_by_zero()


if __name__ == "__main__":
    detect_bugs()