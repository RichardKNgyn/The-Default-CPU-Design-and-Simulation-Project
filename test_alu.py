from alu import ALU

def run_test(alu, operation, a, b, expected, test_name):
    """Helper function to run a single test"""
    result = alu.execute(operation, a, b)
    if result == expected:
        print(f"  PASS: {test_name}")
        return True
    else:
        print(f"  FAIL: {test_name}")
        print(f"    Expected: 0x{expected:08X} ({expected})")
        print(f"    Got:      0x{result:08X} ({result})")
        return False

def test_add():
    """Test ADD operation"""
    print("\n=== Testing ADD ===")
    alu = ALU()
    passed = 0
    
    tests = [
        (5, 10, 15, "ADD: 5 + 10 = 15"),
        (100, 0, 100, "ADD: 100 + 0 = 100"),
        (0xFFFFFFFF, 1, 0, "ADD: 0xFFFFFFFF + 1 = 0 (overflow)"),
        (0x7FFFFFFF, 1, 0x80000000, "ADD: Max positive + 1"),
    ]
    
    for a, b, expected, name in tests:
        if run_test(alu, 'ADD', a, b, expected, name):
            passed += 1
    
    return passed, len(tests)

def test_sub():
    """Test SUB operation"""
    print("\n=== Testing SUB ===")
    alu = ALU()
    passed = 0
    
    tests = [
        (10, 5, 5, "SUB: 10 - 5 = 5"),
        (0, 1, 0xFFFFFFFF, "SUB: 0 - 1 = 0xFFFFFFFF (underflow)"),
        (42, 42, 0, "SUB: 42 - 42 = 0"),
        (100, 50, 50, "SUB: 100 - 50 = 50"),
    ]
    
    for a, b, expected, name in tests:
        if run_test(alu, 'SUB', a, b, expected, name):
            passed += 1
    
    return passed, len(tests)

def test_and():
    """Test AND operation"""
    print("\n=== Testing AND ===")
    alu = ALU()
    passed = 0
    
    tests = [
        (0xFF, 0x0F, 0x0F, "AND: 0xFF & 0x0F = 0x0F"),
        (0xFFFFFFFF, 0, 0, "AND: anything & 0 = 0"),
        (0x12345678, 0x12345678, 0x12345678, "AND: x & x = x"),
        (0xFF00FF00, 0x00FF00FF, 0, "AND: Non-overlapping bits = 0"),
    ]
    
    for a, b, expected, name in tests:
        if run_test(alu, 'AND', a, b, expected, name):
            passed += 1
    
    return passed, len(tests)

def test_or():
    """Test OR operation"""
    print("\n=== Testing OR ===")
    alu = ALU()
    passed = 0
    
    tests = [
        (0xF0, 0x0F, 0xFF, "OR: 0xF0 | 0x0F = 0xFF"),
        (0x12345678, 0, 0x12345678, "OR: x | 0 = x"),
        (0x12345678, 0xFFFFFFFF, 0xFFFFFFFF, "OR: x | 0xFFFFFFFF = 0xFFFFFFFF"),
        (0, 0, 0, "OR: 0 | 0 = 0"),
    ]
    
    for a, b, expected, name in tests:
        if run_test(alu, 'OR', a, b, expected, name):
            passed += 1
    
    return passed, len(tests)

def test_xor():
    """Test XOR operation"""
    print("\n=== Testing XOR ===")
    alu = ALU()
    passed = 0
    
    tests = [
        (0xFF, 0x0F, 0xF0, "XOR: 0xFF ^ 0x0F = 0xF0"),
        (0x12345678, 0x12345678, 0, "XOR: x ^ x = 0"),
        (0xABCDEF01, 0, 0xABCDEF01, "XOR: x ^ 0 = x"),
        (0xFF00FF00, 0xFFFFFFFF, 0x00FF00FF, "XOR: Bit inversion"),
    ]
    
    for a, b, expected, name in tests:
        if run_test(alu, 'XOR', a, b, expected, name):
            passed += 1
    
    return passed, len(tests)

def test_sll():
    """Test Shift Left Logical"""
    print("\n=== Testing SLL ===")
    alu = ALU()
    passed = 0
    
    tests = [
        (1, 4, 16, "SLL: 1 << 4 = 16"),
        (0x12345678, 0, 0x12345678, "SLL: x << 0 = x"),
        (1, 31, 0x80000000, "SLL: 1 << 31 = 0x80000000"),
        (0xFFFFFFFF, 1, 0xFFFFFFFE, "SLL: Shift with overflow"),
        (1, 36, 16, "SLL: Shift amount wraps (36 & 0x1F = 4)"),
    ]
    
    for a, b, expected, name in tests:
        if run_test(alu, 'SLL', a, b, expected, name):
            passed += 1
    
    return passed, len(tests)

def test_srl():
    """Test Shift Right Logical"""
    print("\n=== Testing SRL ===")
    alu = ALU()
    passed = 0
    
    tests = [
        (16, 4, 1, "SRL: 16 >> 4 = 1"),
        (0x12345678, 0, 0x12345678, "SRL: x >> 0 = x"),
        (0x80000000, 1, 0x40000000, "SRL: Logical shift (no sign extension)"),
        (0xFFFFFFFF, 31, 1, "SRL: 0xFFFFFFFF >> 31 = 1"),
    ]
    
    for a, b, expected, name in tests:
        if run_test(alu, 'SRL', a, b, expected, name):
            passed += 1
    
    return passed, len(tests)

def test_sra():
    """Test Shift Right Arithmetic"""
    print("\n=== Testing SRA ===")
    alu = ALU()
    passed = 0
    
    tests = [
        (16, 4, 1, "SRA: 16 >> 4 = 1 (positive)"),
        (0x80000000, 1, 0xC0000000, "SRA: Sign extension for negative"),
        (0xFFFFFFFF, 4, 0xFFFFFFFF, "SRA: -1 >> 4 = -1"),
        (0x80000000, 0, 0x80000000, "SRA: x >> 0 = x"),
        (0x40000000, 1, 0x20000000, "SRA: Positive number (no sign ext)"),
    ]
    
    for a, b, expected, name in tests:
        if run_test(alu, 'SRA', a, b, expected, name):
            passed += 1
    
    return passed, len(tests)

def test_slt():
    """Test Set Less Than (signed)"""
    print("\n=== Testing SLT ===")
    alu = ALU()
    passed = 0
    
    tests = [
        (5, 10, 1, "SLT: 5 < 10 = 1"),
        (10, 5, 0, "SLT: 10 < 5 = 0"),
        (7, 7, 0, "SLT: 7 < 7 = 0"),
        (0xFFFFFFFF, 1, 1, "SLT: -1 < 1 = 1 (signed)"),
        (0xFFFFFFFE, 0xFFFFFFFF, 1, "SLT: -2 < -1 = 1"),
        (1, 0xFFFFFFFF, 0, "SLT: 1 < -1 = 0 (signed)"),
    ]
    
    for a, b, expected, name in tests:
        if run_test(alu, 'SLT', a, b, expected, name):
            passed += 1
    
    return passed, len(tests)

def test_sltu():
    """Test Set Less Than Unsigned"""
    print("\n=== Testing SLTU ===")
    alu = ALU()
    passed = 0
    
    tests = [
        (5, 10, 1, "SLTU: 5 < 10 = 1"),
        (0xFFFFFFFF, 1, 0, "SLTU: 0xFFFFFFFF < 1 = 0 (unsigned)"),
        (100, 100, 0, "SLTU: 100 < 100 = 0"),
        (0, 0xFFFFFFFF, 1, "SLTU: 0 < 0xFFFFFFFF = 1"),
    ]
    
    for a, b, expected, name in tests:
        if run_test(alu, 'SLTU', a, b, expected, name):
            passed += 1
    
    return passed, len(tests)

def run_all_tests():
    """Run all ALU tests"""
    print("=" * 60)
    print("RISC-V ALU Unit Tests")
    print("=" * 60)
    
    total_passed = 0
    total_tests = 0
    
    test_functions = [
        test_add,
        test_sub,
        test_and,
        test_or,
        test_xor,
        test_sll,
        test_srl,
        test_sra,
        test_slt,
        test_sltu,
    ]
    
    for test_func in test_functions:
        passed, total = test_func()
        total_passed += passed
        total_tests += total
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Tests passed: {total_passed}/{total_tests}")
    print("=" * 60)
    
    if total_passed == total_tests:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {total_tests - total_passed} test(s) failed")
        return 1


if __name__ == "__main__":
    import sys
    exit_code = run_all_tests()
    sys.exit(exit_code)