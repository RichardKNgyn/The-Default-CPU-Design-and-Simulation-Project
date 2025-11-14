from decoder import InstructionDecoder

def test_decoder():
    decoder = InstructionDecoder()
    
    print("Testing Instruction Decoder")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    # Test 1: R-type (ADD)
    print("\nTest 1: R-type ADD instruction")
    decoded = decoder.decode(0x002081B3)  # add x3, x1, x2
    if decoded['type'] == 'R' and decoded['rd'] == 3 and decoded['rs1'] == 1 and decoded['rs2'] == 2:
        print("PASS")
        passed += 1
    else:
        print("FAIL")
        failed += 1
    
    # Test 2: I-type (ADDI)
    print("\nTest 2: I-type ADDI instruction")
    decoded = decoder.decode(0x00500093)  # addi x1, x0, 5
    if decoded['type'] == 'I' and decoded['imm'] == 5:
        print("PASS")
        passed += 1
    else:
        print("FAIL")
        failed += 1
    
    # Test 3: I-type negative immediate
    print("\nTest 3: I-type with negative immediate")
    decoded = decoder.decode(0xFFF00113)  # addi x2, x0, -1
    if decoded['imm'] == -1:
        print("PASS - negative immediate works")
        passed += 1
    else:
        print(f"FAIL - got {decoded['imm']}, expected -1")
        failed += 1
    
    # Test 4: S-type (SW)
    print("\nTest 4: S-type SW instruction")
    decoded = decoder.decode(0x0032A023)  # sw x3, 0(x5)
    if decoded['type'] == 'S' and decoded['rs1'] == 5 and decoded['rs2'] == 3:
        print("PASS")
        passed += 1
    else:
        print("FAIL")
        failed += 1
    
    # Test 5: B-type (BEQ)
    print("\nTest 5: B-type BEQ instruction")
    decoded = decoder.decode(0x00418463)  # beq x3, x4, 8
    if decoded['type'] == 'B' and decoded['imm'] == 8:
        print("PASS - branch offset = 8")
        passed += 1
    else:
        print(f"FAIL - got offset {decoded['imm']}, expected 8")
        failed += 1
    
    # Test 6: U-type (LUI)
    print("\nTest 6: U-type LUI instruction")
    decoded = decoder.decode(0x000102B7)  # lui x5, 0x00010
    if decoded['type'] == 'U' and decoded['imm'] == 0x00010000:
        print("PASS")
        passed += 1
    else:
        print("FAIL")
        failed += 1
    
    # Test 7: J-type (JAL)
    print("\nTest 7: J-type JAL instruction")
    decoded = decoder.decode(0x0000006F)  # jal x0, 0
    if decoded['type'] == 'J' and decoded['imm'] == 0:
        print("PASS")
        passed += 1
    else:
        print("FAIL")
        failed += 1
    
    # Test 8: Instruction names
    print("\nTest 8: Instruction name detection")
    test_names = [
        (0x002081B3, "ADD"),
        (0x00500093, "ADDI"),
        (0x0032A023, "SW"),
        (0x0002A203, "LW"),
    ]
    
    names_ok = True
    for inst, expected_name in test_names:
        decoded = decoder.decode(inst)
        name = decoder.get_name(decoded)
        if name != expected_name:
            print(f"FAIL - {inst:08X} should be {expected_name}, got {name}")
            names_ok = False
    
    if names_ok:
        print("PASS - all instruction names correct")
        passed += 1
    else:
        failed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    print("=" * 50)
    
    if failed == 0:
        print("All tests passed!")
    
    return failed == 0


if __name__ == "__main__":
    success = test_decoder()
    exit(0 if success else 1)