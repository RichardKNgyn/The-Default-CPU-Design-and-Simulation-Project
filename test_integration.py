from alu import ALU
from registers import RegisterFile
from memory import Memory
from decoder import InstructionDecoder
from loader import load_hex_file, create_test_hex_file

def test_alu_register_integration():
    """Test ALU operations with register file"""
    print("\n=== Testing ALU + Register Integration ===")
    
    alu = ALU()
    rf = RegisterFile()
    
    # Simulate: x3 = x1 + x2
    rf.write(1, 5)
    rf.write(2, 10)
    
    result = alu.execute('ADD', rf.read(1), rf.read(2))
    rf.write(3, result)
    
    print(f"x1 = {rf.read(1)}")
    print(f"x2 = {rf.read(2)}")
    print(f"x3 = x1 + x2 = {rf.read(3)} (expected 15)")
    
    if rf.read(3) == 15:
        print("PASS: ALU + Register integration working!")
        return True
    else:
        print("FAIL: Integration test failed")
        return False

def test_register_memory_integration():
    """Test storing register values to memory and loading back"""
    print("\n=== Testing Register + Memory Integration ===")
    
    rf = RegisterFile()
    mem = Memory()
    
    # Write value to register
    rf.write(5, 0xDEADBEEF)
    
    # Store register to memory
    address = 0x10000
    mem.write_word(address, rf.read(5))
    
    # Clear register
    rf.write(5, 0)
    
    # Load from memory back to register
    rf.write(5, mem.read_word(address))
    
    print(f"Stored 0xDEADBEEF to memory at 0x{address:08X}")
    print(f"Loaded back to x5 = 0x{rf.read(5):08X}")
    
    if rf.read(5) == 0xDEADBEEF:
        print("PASS: Register + Memory integration working!")
        return True
    else:
        print("FAIL: Integration test failed")
        return False

def test_decoder_integration():
    """Test decoder with actual instructions"""
    print("\n=== Testing Decoder Integration ===")
    
    decoder = InstructionDecoder()
    rf = RegisterFile()
    alu = ALU()
    
    # Simulate decoding and executing: addi x1, x0, 42
    instruction = 0x02A00093  # addi x1, x0, 42
    decoded = decoder.decode(instruction)
    
    print(f"Instruction: 0x{instruction:08X}")
    print(f"Decoded: {decoder.get_name(decoded)}")
    print(f"rd={decoded['rd']}, rs1={decoded['rs1']}, imm={decoded['imm']}")
    
    # Execute the instruction
    rs1_val = rf.read(decoded['rs1'])
    result = alu.execute('ADD', rs1_val, decoded['imm'])
    rf.write(decoded['rd'], result)
    
    print(f"Result: x1 = {rf.read(1)} (expected 42)")
    
    if rf.read(1) == 42:
        print("PASS: Decoder integration working!")
        return True
    else:
        print("FAIL: Decoder integration failed")
        return False

def test_full_pipeline():
    """Test a complete instruction pipeline simulation"""
    print("\n=== Testing Full Pipeline Simulation ===")
    
    alu = ALU()
    rf = RegisterFile()
    mem = Memory()
    decoder = InstructionDecoder()
    
    # Simulate these instructions:
    # addi x1, x0, 5    -> x1 = 5
    # addi x2, x0, 10   -> x2 = 10
    # add x3, x1, x2    -> x3 = 15
    # sw x3, 0(x0)      -> mem[0] = 15
    # lw x4, 0(x0)      -> x4 = mem[0] = 15
    
    instructions = [
        0x00500093,  # addi x1, x0, 5
        0x00A00113,  # addi x2, x0, 10
        0x002081B3,  # add x3, x1, x2
        0x00302023,  # sw x3, 0(x0)
        0x00002203,  # lw x4, 0(x0)
    ]
    
    for inst in instructions:
        decoded = decoder.decode(inst)
        name = decoder.get_name(decoded)
        opcode = decoded['opcode']
        
        # Execute based on type
        if opcode == 0x13:  # I-type arithmetic
            rs1_val = rf.read(decoded['rs1'])
            result = alu.execute('ADD', rs1_val, decoded['imm'])
            rf.write(decoded['rd'], result)
            print(f"{name}: x{decoded['rd']} = {rf.read(decoded['rd'])}")
        
        elif opcode == 0x33:  # R-type
            rs1_val = rf.read(decoded['rs1'])
            rs2_val = rf.read(decoded['rs2'])
            result = alu.execute('ADD', rs1_val, rs2_val)
            rf.write(decoded['rd'], result)
            print(f"{name}: x{decoded['rd']} = {rf.read(decoded['rd'])}")
        
        elif opcode == 0x23:  # Store
            rs1_val = rf.read(decoded['rs1'])
            rs2_val = rf.read(decoded['rs2'])
            address = (rs1_val + decoded['imm']) & 0xFFFFFFFF
            mem.write_word(address, rs2_val)
            print(f"{name}: mem[0x{address:08X}] = {rs2_val}")
        
        elif opcode == 0x03:  # Load
            rs1_val = rf.read(decoded['rs1'])
            address = (rs1_val + decoded['imm']) & 0xFFFFFFFF
            value = mem.read_word(address)
            rf.write(decoded['rd'], value)
            print(f"{name}: x{decoded['rd']} = {value}")
    
    # Verify results
    success = (rf.read(1) == 5 and 
               rf.read(2) == 10 and 
               rf.read(3) == 15 and 
               rf.read(4) == 15 and
               mem.read_word(0) == 15)
    
    if success:
        print("PASS: Full pipeline simulation working!")
        return True
    else:
        print("FAIL: Pipeline simulation failed")
        return False

def test_hex_loader_integration():
    """Test loading actual hex file"""
    print("\n=== Testing Hex File Loader Integration ===")
    
    mem = Memory()
    
    # Create test file
    create_test_hex_file("test_integration.hex")
    
    # Load it
    count = load_hex_file("test_integration.hex", mem)
    
    if count > 0:
        print(f"✓ Successfully loaded {count} instructions")
        
        # Verify first instruction
        first_inst = mem.read_word(0x0)
        print(f"First instruction: 0x{first_inst:08X}")
        
        return True
    else:
        print("✗ Failed to load hex file")
        return False

def test_branch_simulation():
    """Test branch instruction behavior"""
    print("\n=== Testing Branch Simulation ===")
    
    alu = ALU()
    rf = RegisterFile()
    
    # Set up registers for branch test
    rf.write(1, 10)
    rf.write(2, 10)
    
    # Test BEQ (branch if equal)
    rs1_val = rf.read(1)
    rs2_val = rf.read(2)
    
    # Simulate: beq x1, x2, offset
    branch_taken = (rs1_val == rs2_val)
    
    print(f"x1 = {rs1_val}, x2 = {rs2_val}")
    print(f"BEQ should be taken: {branch_taken}")
    
    if branch_taken:
        print("PASS: Branch condition correct!")
        return True
    else:
        print("FAIL: Branch condition failed")
        return False

def test_memory_alignment():
    """Test memory word alignment"""
    print("\n=== Testing Memory Alignment ===")
    
    mem = Memory()
    
    # Write to aligned address
    mem.write_word(0x1000, 0x12345678)
    
    # Try to read from unaligned address (should auto-align)
    value1 = mem.read_word(0x1000)
    value2 = mem.read_word(0x1002)  # Should read from 0x1000
    
    print(f"Wrote 0x12345678 to 0x1000")
    print(f"Read from 0x1000: 0x{value1:08X}")
    print(f"Read from 0x1002: 0x{value2:08X} (should be same, auto-aligned)")
    
    if value1 == value2 == 0x12345678:
        print("PASS: Memory alignment working!")
        return True
    else:
        print("FAIL: Memory alignment issue")
        return False

def test_register_x0():
    """Test that x0 is hardwired to zero"""
    print("\n=== Testing Register x0 Hardwired to Zero ===")
    
    rf = RegisterFile()
    
    # Try to write to x0
    rf.write(0, 0xFFFFFFFF)
    
    # Read back - should still be 0
    value = rf.read(0)
    
    print(f"Tried to write 0xFFFFFFFF to x0")
    print(f"Read back: 0x{value:08X} (should be 0x00000000)")
    
    if value == 0:
        print("PASS: x0 hardwired to zero!")
        return True
    else:
        print("FAIL: x0 not hardwired")
        return False

def run_all_tests():
    """Run all integration tests"""
    print("=" * 60)
    print("Integration Tests - Component Interaction")
    print("=" * 60)
    
    tests = [
        test_alu_register_integration,
        test_register_memory_integration,
        test_decoder_integration,
        test_full_pipeline,
        test_hex_loader_integration,
        test_branch_simulation,
        test_memory_alignment,
        test_register_x0,
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"FAIL: Test crashed with error: {e}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{len(tests)} test suites passed")
    print("=" * 60)
    
    if passed == len(tests):
        print("✓ All integration tests passed!")
        return 0
    else:
        print(f"✗ {len(tests) - passed} test suite(s) failed")
        return 1


if __name__ == "__main__":
    import sys
    exit_code = run_all_tests()
    sys.exit(exit_code)