import subprocess

def evaluate_bug_detection():
    # Expected output phrases for each test case.
    expected = {
        "Division by zero": "⚠️ Division by zero possible! (x = 0)",
        "Array out-of-bounds (negative)": "⚠️ Array out-of-bounds (negative index:",
        "Array out-of-bounds (positive)": "⚠️ Array out-of-bounds (index too large:",
        "Assertion failure": "⚠️ Assertion failure detected!",
        "Dead code": "⚠️ Dead code detected (unreachable condition)."
    }
    
    # Run the bug detection script and capture its output.
    result = subprocess.run(["python", "BasicConstraints.py"], capture_output=True, text=True)
    output = result.stdout
    
    print("Bug Detection Output:")
    print(output)
    print("\nEvaluation Results:")
    
    # Check for each expected output in the script's output.
    for test_name, phrase in expected.items():
        if phrase in output:
            print(f"{test_name} test: Passed")
        else:
            print(f"{test_name} test: Failed")

if __name__ == "__main__":
    evaluate_bug_detection()
