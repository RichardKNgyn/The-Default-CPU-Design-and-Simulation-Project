"""
Test the complete CPU
"""

from cpu import RISCV_CPU

def test_basic_arithmetic():
    """Test if basic math works"""
    print("\n=== Test 1: Basic Arithmetic ===")
    
    cpu = RISCV_CPU()
    
    # AI Start - test program encoding
    # Used RARS assembler to generate these hex values
    # Wrote assembly, assembled it, copied the machine code
    program = [
        "00500093",  # addi x1, x0, 5
        "00A00113",  # addi x2, x0, 10
        "002081B3",  # add x3, x1, x2
        "40110233",  # sub x4, x2, x1
        "0000006F",  # jal x0, 0 (halt)
    ]
    # AI End
    
    # Save to file
    with open("test_arith.hex", "w") as f:
        for inst in program:
            f.write(inst + "\n")
    
    cpu.load_program("test_arith.hex")
    cpu.run(max_cycles=10, verbose=False)
    
    # Check results
    x1 = cpu.registers.read(1)
    x2 = cpu.registers.read(2)
    x3 = cpu.registers.read(3)
    x4 = cpu.registers.read(4)
    
    print(f"x1 = {x1} (should be 5)")
    print(f"x2 = {x2} (should be 10)")
    print(f"x3 = {x3} (should be 15)")
    print(f"x4 = {x4} (should be 5)")
    
    if x1 == 5 and x2 == 10 and x3 == 15 and x4 == 5:
        print("PASS")
        return True
    else:
        print("FAIL")
        return False

def test_memory_ops():
    """Test loading and storing"""
    print("\n=== Test 2: Memory Operations ===")
    
    cpu = RISCV_CPU()
    
    # AI Start - test program encoding
    # Used RARS to generate these
    program = [
        "01400093",  # addi x1, x0, 20
        "00010137",  # lui x2, 0x00010
        "00112023",  # sw x1, 0(x2)
        "00012183",  # lw x3, 0(x2)
        "0000006F",  # halt
    ]
    # AI End
    
    with open("test_mem.hex", "w") as f:
        for inst in program:
            f.write(inst + "\n")
    
    cpu.load_program("test_mem.hex")
    cpu.run(max_cycles=10, verbose=False)
    
    x1 = cpu.registers.read(1)
    x3 = cpu.registers.read(3)
    # AI Start - memory address choice
    # Using 0x10000 because it's far from instruction memory at 0x0
    # Same address convention as test_base.hex
    mem_val = cpu.memory.read_word(0x10000)
    # AI End
    
    print(f"x1 = {x1} (should be 20)")
    print(f"Memory[0x10000] = {mem_val} (should be 20)")
    print(f"x3 = {x3} (should be 20)")
    
    if x1 == 20 and mem_val == 20 and x3 == 20:
        print("PASS")
        return True
    else:
        print("FAIL")
        return False

def test_branches():
    """Test if branches work"""
    print("\n=== Test 3: Branches ===")
    
    cpu = RISCV_CPU()
    
    # AI Start - test program encoding
    # Created this test to verify BEQ skips correctly
    # Used RARS to get machine code
    program = [
        "00500093",  # addi x1, x0, 5
        "00500113",  # addi x2, x0, 5
        "00000193",  # addi x3, x0, 0
        "00208463",  # beq x1, x2, 8 (skip next instruction)
        "00100193",  # addi x3, x0, 1 (this should be skipped)
        "00200193",  # addi x3, x0, 2
        "0000006F",  # halt
    ]
    # AI End
    
    with open("test_branch.hex", "w") as f:
        for inst in program:
            f.write(inst + "\n")
    
    cpu.load_program("test_branch.hex")
    cpu.run(max_cycles=10, verbose=False)
    
    x3 = cpu.registers.read(3)
    
    print(f"x3 = {x3} (should be 2, not 1)")
    
    if x3 == 2:
        print("PASS - branch worked!")
        return True
    else:
        print("FAIL")
        return False

def test_full_program():
    """Test the complete test_base.hex program"""
    print("\n=== Test 4: Full Program (test_base.hex) ===")
    
    cpu = RISCV_CPU()
    cpu.load_program("test_base.hex")
    cpu.run(max_cycles=20, verbose=False)
    
    # AI Start - expected values
    # Figured these out by tracing through test_base.hex manually
    # Also ran in RARS to verify what the final state should be
    x1 = cpu.registers.read(1)
    x2 = cpu.registers.read(2)
    x3 = cpu.registers.read(3)
    x4 = cpu.registers.read(4)
    x5 = cpu.registers.read(5)
    x6 = cpu.registers.read(6)
    mem_val = cpu.memory.read_word(0x10000)
    
    print(f"x1 = {x1} (expected 5)")
    print(f"x2 = {x2} (expected 10)")
    print(f"x3 = {x3} (expected 15)")
    print(f"x4 = {x4} (expected 15)")
    print(f"x5 = 0x{x5:08X} (expected 0x00010000)")
    print(f"x6 = {x6} (expected 2)")
    print(f"mem[0x10000] = {mem_val} (expected 15)")
    
    all_correct = (x1 == 5 and x2 == 10 and x3 == 15 and 
                   x4 == 15 and x5 == 0x10000 and 
                   x6 == 2 and mem_val == 15)
    # AI End
    
    if all_correct:
        print("PASS - Everything correct!")
        return True
    else:
        print("FAIL - Something wrong")
        return False

# Run all tests
if __name__ == "__main__":
    print("=" * 60)
    print("CPU TESTS")
    print("=" * 60)
    
    tests = [
        test_basic_arithmetic,
        test_memory_ops,
        test_branches,
        test_full_program,
    ]
    
    passed = 0
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"FAIL - Test crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{len(tests)} passed")
    print("=" * 60)
    
    if passed == len(tests):
        print("All tests passed!")