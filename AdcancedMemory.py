from z3 import *

def memory_safety_checker():
    print("\n=== Z3 Memory Safety Checker ===")
    
    # Create solver
    solver = Solver()
    
    # Define memory model
    # We'll use integers to represent memory addresses
    # We'll track allocation status in a separate map
    memory_size = 100  # Maximum memory size
    
    # Memory allocation tracking
    # For each address, we track:
    # - is_allocated: whether the memory is currently allocated
    # - allocated_size: how many bytes were allocated at this address
    is_allocated = Function('is_allocated', IntSort(), BoolSort())
    allocated_size = Function('allocated_size', IntSort(), IntSort())
    
    # Helper functions for memory operations
    def allocate_memory(addr, size):
        # Allocation creates constraints that:
        # 1. The address is now allocated
        # 2. The allocation has a specific size
        # 3. The allocated memory fits within our memory bounds
        return And(
            is_allocated(addr) == True,
            allocated_size(addr) == size,
            addr >= 0,
            addr + size <= memory_size
        )
    
    def free_memory(addr):
        # Free operation just marks memory as not allocated
        return is_allocated(addr) == False
    
    # Memory safety checks
    def check_null_pointer(addr):
        print("\nChecking for null pointer dereference...")
        # A null pointer has address 0
        solver.push()
        solver.add(addr == 0)
        
        if solver.check() == sat:
            model = solver.model()
            print("⚠️ Null pointer dereference detected!")
            print(f"   Address: {model.eval(addr)}")
        else:
            print("✅ No null pointer dereference possible")
        
        solver.pop()
    
    def check_use_after_free(addr):
        print("\nChecking for use-after-free...")
        # Use after free means using a pointer that's not allocated
        solver.push()
        solver.add(Not(is_allocated(addr)))
        
        if solver.check() == sat:
            model = solver.model()
            print("⚠️ Use-after-free detected!")
            print(f"   Address: {model.eval(addr)}")
        else:
            print("✅ No use-after-free possible")
        
        solver.pop()
    
    def check_buffer_overflow(addr, access_size):
        print("\nChecking for buffer overflow...")
        # Buffer overflow means accessing beyond allocated size
        solver.push()
        solver.add(is_allocated(addr))  # Must be allocated
        solver.add(access_size > allocated_size(addr))  # Accessing more than allocated
        
        if solver.check() == sat:
            model = solver.model()
            addr_val = model.eval(addr).as_long()
            alloc_size = model.eval(allocated_size(addr)).as_long()
            access = model.eval(access_size).as_long()
            overflow = access - alloc_size
            
            print("⚠️ Buffer overflow detected!")
            print(f"   Address: {addr_val}")
            print(f"   Allocated size: {alloc_size} bytes")
            print(f"   Access size: {access} bytes")
            print(f"   Overflow: {overflow} bytes")
        else:
            print("✅ No buffer overflow possible")
            
        solver.pop()
    
    def check_double_free(addr):
        print("\nChecking for double free...")
        # Double free means freeing an address that's already free
        solver.push()
        solver.add(Not(is_allocated(addr)))  # Already free
        
        if solver.check() == sat:
            model = solver.model()
            print("⚠️ Double free detected!")
            print(f"   Address: {model.eval(addr)}")
        else:
            print("✅ No double free possible")
            
        solver.pop()
    
    # Test different memory safety scenarios
    def test_scenarios():
        # Create symbolic values for testing
        addr = Int('addr')
        size = Int('size')
        access_size = Int('access_size')
        
        # Scenario 1: Simulate allocation
        print("\n--- Scenario 1: Memory Allocation ---")
        solver.push()
        # Allocate memory of size 10 at address 5
        solver.add(allocate_memory(5, 10))
        
        # Check if we can detect null pointer issues
        check_null_pointer(addr)
        
        # Check if use-after-free is possible (should not be for valid allocation)
        solver.add(addr == 5)  # Use allocated address
        check_use_after_free(addr)
        
        # Check if buffer overflow is possible
        solver.add(access_size == 15)  # Try to access more than allocated
        check_buffer_overflow(addr, access_size)
        
        solver.pop()
        
        # Scenario 2: Use-after-free test
        print("\n--- Scenario 2: Use-after-free Test ---")
        solver.push()
        
        # First allocate memory
        solver.add(allocate_memory(10, 20))
        
        # Then free it
        solver.add(free_memory(10))
        
        # Now try to use it
        solver.add(addr == 10)
        check_use_after_free(addr)
        
        solver.pop()
        
        # Scenario 3: Double free test
        print("\n--- Scenario 3: Double Free Test ---")
        solver.push()
        
        # Allocate and then free memory
        solver.add(allocate_memory(15, 5))
        solver.add(free_memory(15))
        
        # Try to free again
        solver.add(addr == 15)
        check_double_free(addr)
        
        solver.pop()
        
        # Scenario 4: Complex example with symbolic addresses
        print("\n--- Scenario 4: Symbolic Execution ---")
        solver.push()
        
        # Constrain addr to be a valid memory location
        solver.add(addr >= 0, addr < memory_size)
        
        # Allocate with symbolic size (but reasonable)
        solver.add(size > 0, size < 50)
        solver.add(allocate_memory(addr, size))
        
        # Try to access with potentially larger size
        solver.add(access_size >= size)
        check_buffer_overflow(addr, access_size)
        
        solver.pop()
    
    # Run all tests
    test_scenarios()

if __name__ == "__main__":
    memory_safety_checker()