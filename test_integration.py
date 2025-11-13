from alu import ALU
from registers import RegisterFile
from memory import Memory
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
        print("✓ ALU + Register integration working!")
        return True
    else:
        print("✗ Integration test failed")
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
        print("✓ Register + Memory integration working!")
        return True
    else:
        print("✗ Integration test failed")
        return False
#AI Start
def test_full_pipeline():
    """Test a complete instruction pipeline simulation"""
    print("\n=== Testing Full Pipeline Simulation ===")
    
    alu = ALU()
    rf = RegisterFile()
    mem = Memory()
    
    # Simulate these instructions:
    # addi x1, x0, 5    -> x1 = 5
    # addi x2, x0, 10   -> x2 = 10
    # add x3, x1, x2    -> x3 = 15
    # sw x3, 0(x0)      -> mem[0] = 15
    # lw x4, 0(x0)      -> x4 = mem[0] = 15
    
    # Instruction 1: addi x1, x0, 5
    rs1_val = rf.read(0)  # x0
    imm = 5
    result = alu.execute('ADD', rs1_val, imm)
    rf.write(1, result)
    print(f"addi x1, x0, 5  -> x1 = {rf.read(1)}")
    
    # Instruction 2: addi x2, x0, 10
    rs1_val = rf.read(0)
    imm = 10
    result = alu.execute('ADD', rs1_val, imm)
    rf.write(2, result)
    print(f"addi x2, x0, 10 -> x2 = {rf.read(2)}")
    
    # Instruction 3: add x3, x1, x2
    rs1_val = rf.read(1)
    rs2_val = rf.read(2)
    result = alu.execute('ADD', rs1_val, rs2_val)
    rf.write(3, result)
    print(f"add x3, x1, x2  -> x3 = {rf.read(3)}")
    
    # Instruction 4: sw x3, 0(x0)
    address = rf.read(0) + 0  # x0 + offset
    mem.write_word(address, rf.read(3))
    print(f"sw x3, 0(x0)    -> mem[0x{address:08X}] = {mem.read_word(address)}")
    
    # Instruction 5: lw x4, 0(x0)
    address = rf.read(0) + 0
    rf.write(4, mem.read_word(address))
    print(f"lw x4, 0(x0)    -> x4 = {rf.read(4)}")
    
    # Verify results, AI End
    success = (rf.read(1) == 5 and 
               rf.read(2) == 10 and 
               rf.read(3) == 15 and 
               rf.read(4) == 15 and
               mem.read_word(0) == 15)
    
    if success:
        print("✓ Full pipeline simulation working!")
        return True
    else:
        print("✗ Pipeline simulation failed")
        return False

def test_hex_loader():
    """Test loading actual hex file"""
    print("\n=== Testing Hex File Loader ===")
    
    mem = Memory()
    
    # Create test file
    create_test_hex_file("test_day2.hex")
    
    # Load it
    count = load_hex_file("test_day2.hex", mem)
    
    if count > 0:
        print(f"✓ Successfully loaded {count} instructions")
        mem.dump(0x0, 4)
        return True
    else:
        print("✗ Failed to load hex file")
        return False

# Run all tests
if __name__ == "__main__":
    print("=" * 50)
    print("Day 2 Integration Tests")
    print("=" * 50)
    
    tests = [
        test_alu_register_integration,
        test_register_memory_integration,
        test_full_pipeline,
        test_hex_loader
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{len(tests)} test suites passed")
    print("=" * 50)