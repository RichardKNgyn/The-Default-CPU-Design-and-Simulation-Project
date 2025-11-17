from decoder import InstructionDecoder

def run_test(condition, test_name):
    """Helper to run a single test"""
    if condition:
        print(f"  PASS: {test_name}")
        return True
    else:
        print(f"  FAIL: {test_name}")
        return False

def test_r_type():
    """Test R-type instruction decoding"""
    print("\n=== Testing R-type ===")
    decoder = InstructionDecoder()
    passed = 0
    
    # add x3, x1, x2 (0x002081B3)
    decoded = decoder.decode(0x002081B3)
    passed += run_test(decoded['type'] == 'R', "Type is R")
    passed += run_test(decoded['rd'] == 3, "rd = 3")
    passed += run_test(decoded['rs1'] == 1, "rs1 = 1")
    passed += run_test(decoded['rs2'] == 2, "rs2 = 2")
    passed += run_test(decoded['funct3'] == 0x0, "funct3 = 0")
    passed += run_test(decoded['funct7'] == 0x00, "funct7 = 0x00 (ADD)")
    passed += run_test(decoder.get_name(decoded) == "ADD", "Name is ADD")
    
    # sub x4, x2, x1 (0x40110233)
    decoded = decoder.decode(0x40110233)
    passed += run_test(decoded['funct7'] == 0x20, "funct7 = 0x20 (SUB)")
    passed += run_test(decoder.get_name(decoded) == "SUB", "Name is SUB")
    
    return passed, 9

def test_i_type():
    """Test I-type instruction decoding"""
    print("\n=== Testing I-type ===")
    decoder = InstructionDecoder()
    passed = 0
    
    # addi x1, x0, 5 (0x00500093)
    decoded = decoder.decode(0x00500093)
    passed += run_test(decoded['type'] == 'I', "Type is I")
    passed += run_test(decoded['rd'] == 1, "rd = 1")
    passed += run_test(decoded['rs1'] == 0, "rs1 = 0")
    passed += run_test(decoded['imm'] == 5, "imm = 5")
    passed += run_test(decoder.get_name(decoded) == "ADDI", "Name is ADDI")
    
    # Test negative immediate: addi x2, x0, -1 (0xFFF00113)
    decoded = decoder.decode(0xFFF00113)
    passed += run_test(decoded['imm'] == -1, "Negative immediate = -1")
    
    # lw x4, 0(x5) (0x0002A203)
    decoded = decoder.decode(0x0002A203)
    passed += run_test(decoded['opcode'] == 0x03, "Load opcode")
    passed += run_test(decoder.get_name(decoded) == "LW", "Name is LW")
    
    return passed, 8

def test_s_type():
    """Test S-type instruction decoding"""
    print("\n=== Testing S-type ===")
    decoder = InstructionDecoder()
    passed = 0
    
    # sw x3, 0(x5) (0x0032A023)
    decoded = decoder.decode(0x0032A023)
    passed += run_test(decoded['type'] == 'S', "Type is S")
    passed += run_test(decoded['rs1'] == 5, "rs1 (base) = 5")
    passed += run_test(decoded['rs2'] == 3, "rs2 (source) = 3")
    passed += run_test(decoded['imm'] == 0, "imm (offset) = 0")
    passed += run_test(decoder.get_name(decoded) == "SW", "Name is SW")
    
    return passed, 5

def test_b_type():
    """Test B-type instruction decoding"""
    print("\n=== Testing B-type ===")
    decoder = InstructionDecoder()
    passed = 0
    
    # beq x3, x4, 8 (0x00418463)
    decoded = decoder.decode(0x00418463)
    passed += run_test(decoded['type'] == 'B', "Type is B")
    passed += run_test(decoded['rs1'] == 3, "rs1 = 3")
    passed += run_test(decoded['rs2'] == 4, "rs2 = 4")
    passed += run_test(decoded['imm'] == 8, "Branch offset = 8")
    passed += run_test(decoder.get_name(decoded) == "BEQ", "Name is BEQ")
    
    return passed, 5

def test_u_type():
    """Test U-type instruction decoding"""
    print("\n=== Testing U-type ===")
    decoder = InstructionDecoder()
    passed = 0
    
    # lui x5, 0x00010 (0x000102B7)
    decoded = decoder.decode(0x000102B7)
    passed += run_test(decoded['type'] == 'U', "Type is U")
    passed += run_test(decoded['rd'] == 5, "rd = 5")
    passed += run_test(decoded['imm'] == 0x00010000, "Upper immediate = 0x00010000")
    passed += run_test(decoder.get_name(decoded) == "LUI", "Name is LUI")
    
    return passed, 4

def test_j_type():
    """Test J-type instruction decoding"""
    print("\n=== Testing J-type ===")
    decoder = InstructionDecoder()
    passed = 0
    
    # jal x0, 0 (0x0000006F) - infinite loop
    decoded = decoder.decode(0x0000006F)
    passed += run_test(decoded['type'] == 'J', "Type is J")
    passed += run_test(decoded['rd'] == 0, "rd = 0")
    passed += run_test(decoded['imm'] == 0, "Jump offset = 0")
    passed += run_test(decoder.get_name(decoded) == "JAL", "Name is JAL")
    
    return passed, 4

def test_all_instructions():
    """Test instruction name detection for all types"""
    print("\n=== Testing All Instruction Names ===")
    decoder = InstructionDecoder()
    passed = 0
    
    tests = [
        (0x002081B3, "ADD"),     # add x3, x1, x2
        (0x40110233, "SUB"),     # sub x4, x2, x1
        (0x00500093, "ADDI"),    # addi x1, x0, 5
        (0x0032A023, "SW"),      # sw x3, 0(x5)
        (0x0002A203, "LW"),      # lw x4, 0(x5)
        (0x00418463, "BEQ"),     # beq x3, x4, 8
        (0x000102B7, "LUI"),     # lui x5, 0x00010
        (0x0000006F, "JAL"),     # jal x0, 0
    ]
    
    for inst, expected_name in tests:
        decoded = decoder.decode(inst)
        name = decoder.get_name(decoded)
        passed += run_test(name == expected_name, 
                          f"0x{inst:08X} -> {expected_name}")
    
    return passed, len(tests)

def test_immediate_sign_extension():
    """Test sign extension of immediate values"""
    print("\n=== Testing Immediate Sign Extension ===")
    decoder = InstructionDecoder()
    passed = 0
    
    # I-type negative immediate
    decoded = decoder.decode(0xFFF00113)  # addi x2, x0, -1
    passed += run_test(decoded['imm'] == -1, "I-type: -1")
    
    # I-type positive immediate
    decoded = decoder.decode(0x7FF00113)  # addi x2, x0, 2047
    passed += run_test(decoded['imm'] == 2047, "I-type: +2047")
    
    # B-type positive offset
    decoded = decoder.decode(0x00418463)  # beq x3, x4, 8
    passed += run_test(decoded['imm'] == 8, "B-type: +8")
    
    return passed, 3

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n=== Testing Edge Cases ===")
    decoder = InstructionDecoder()
    passed = 0
    
    # All zeros
    decoded = decoder.decode(0x00000000)
    passed += run_test(decoded['opcode'] != None, "Decode all zeros")
    
    # All ones
    decoded = decoder.decode(0xFFFFFFFF)
    passed += run_test(decoded['opcode'] != None, "Decode all ones")
    
    # Maximum positive I-type immediate (2047)
    decoded = decoder.decode(0x7FF00093)  # addi x1, x0, 2047
    passed += run_test(decoded['imm'] == 2047, "Max positive I-imm")
    
    # Minimum negative I-type immediate (-2048)
    decoded = decoder.decode(0x80000093)  # addi x1, x0, -2048
    passed += run_test(decoded['imm'] == -2048, "Min negative I-imm")
    
    return passed, 4

def run_all_tests():
    """Run all decoder tests"""
    print("=" * 60)
    print("Instruction Decoder Tests")
    print("=" * 60)
    
    total_passed = 0
    total_tests = 0
    
    test_functions = [
        test_r_type,
        test_i_type,
        test_s_type,
        test_b_type,
        test_u_type,
        test_j_type,
        test_all_instructions,
        test_immediate_sign_extension,
        test_edge_cases,
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