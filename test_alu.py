"""
Unit tests for ALU module
Tests all arithmetic, logical, and shift operations
"""

import sys
from alu import ALU

#AI Start 
class TestALU:
    def __init__(self):
        self.alu = ALU()
        self.tests_passed = 0
        self.tests_failed = 0
    
    def assert_equal(self, actual, expected, test_name):
        """Helper function to check test results"""

        if actual == expected:
            print(f"✓ {test_name}")
            self.tests_passed += 1
            return True
        else:
            print(f"✗ {test_name}")
            print(f"  Expected: 0x{expected:08X} ({expected})")
            print(f"  Got:      0x{actual:08X} ({actual})")
            self.tests_failed += 1
            return False

    def test_add(self):
        """Test ADD operation"""
        print("\n--- Testing ADD ---")
        
        # Basic addition
        result = self.alu.execute(ALU.OP_ADD, 5, 10)
        self.assert_equal(result, 15, "ADD: 5 + 10 = 15")
        
        # Addition with zero
        result = self.alu.execute(ALU.OP_ADD, 100, 0)
        self.assert_equal(result, 100, "ADD: 100 + 0 = 100")
        
        # Overflow test (wraps around)
        result = self.alu.execute(ALU.OP_ADD, 0xFFFFFFFF, 1)
        self.assert_equal(result, 0, "ADD: 0xFFFFFFFF + 1 = 0 (overflow)")
        
        # Large numbers
        result = self.alu.execute(ALU.OP_ADD, 0x7FFFFFFF, 0x7FFFFFFF)
        self.assert_equal(result, 0xFFFFFFFE, "ADD: Large number overflow")
    #AI End
    def test_sub(self):
        """Test SUB operation"""
        print("\n--- Testing SUB ---")
        
        # Basic subtraction
        result = self.alu.execute(ALU.OP_SUB, 10, 5)
        self.assert_equal(result, 5, "SUB: 10 - 5 = 5")
        
        # Subtract from zero (underflow)
        result = self.alu.execute(ALU.OP_SUB, 0, 1)
        self.assert_equal(result, 0xFFFFFFFF, "SUB: 0 - 1 = 0xFFFFFFFF (underflow)")
        
        # Equal numbers
        result = self.alu.execute(ALU.OP_SUB, 42, 42)
        self.assert_equal(result, 0, "SUB: 42 - 42 = 0")
        self.assert_equal(self.alu.is_zero(), True, "SUB: Zero flag set")
    
    def test_and(self):
        """Test AND operation"""
        print("\n--- Testing AND ---")
        
        # Basic AND
        result = self.alu.execute(ALU.OP_AND, 0xFF, 0x0F)
        self.assert_equal(result, 0x0F, "AND: 0xFF & 0x0F = 0x0F")
        
        # AND with zero
        result = self.alu.execute(ALU.OP_AND, 0xFFFFFFFF, 0)
        self.assert_equal(result, 0, "AND: anything & 0 = 0")
        
        # AND with self
        result = self.alu.execute(ALU.OP_AND, 0x12345678, 0x12345678)
        self.assert_equal(result, 0x12345678, "AND: x & x = x")
        
        # Bit masking, AI Start
        result = self.alu.execute(ALU.OP_AND, 0xAAAAAAAA, 0x55555555)
        self.assert_equal(result, 0, "AND: Alternating bits = 0")
        #AI End
    
    def test_or(self):
        """Test OR operation"""
        print("\n--- Testing OR ---")
        
        # Basic OR
        result = self.alu.execute(ALU.OP_OR, 0xF0, 0x0F)
        self.assert_equal(result, 0xFF, "OR: 0xF0 | 0x0F = 0xFF")
        
        # OR with zero
        result = self.alu.execute(ALU.OP_OR, 0x12345678, 0)
        self.assert_equal(result, 0x12345678, "OR: x | 0 = x")
        
        # OR with all ones
        result = self.alu.execute(ALU.OP_OR, 0x12345678, 0xFFFFFFFF)
        self.assert_equal(result, 0xFFFFFFFF, "OR: x | 0xFFFFFFFF = 0xFFFFFFFF")
    
    def test_xor(self):
        """Test XOR operation"""
        print("\n--- Testing XOR ---")
        
        # Basic XOR
        result = self.alu.execute(ALU.OP_XOR, 0xFF, 0x0F)
        self.assert_equal(result, 0xF0, "XOR: 0xFF ^ 0x0F = 0xF0")
        
        # XOR with self (should be zero)
        result = self.alu.execute(ALU.OP_XOR, 0x12345678, 0x12345678)
        self.assert_equal(result, 0, "XOR: x ^ x = 0")
        
        # XOR with zero
        result = self.alu.execute(ALU.OP_XOR, 0xABCDEF01, 0)
        self.assert_equal(result, 0xABCDEF01, "XOR: x ^ 0 = x")
        
        # Bit inversion
        result = self.alu.execute(ALU.OP_XOR, 0xAAAAAAAA, 0xFFFFFFFF)
        self.assert_equal(result, 0x55555555, "XOR: Bit inversion")
    
    def test_sll(self):
        """Test Shift Left Logical"""
        print("\n--- Testing SLL ---")
        
        # Basic shift
        result = self.alu.execute(ALU.OP_SLL, 1, 4)
        self.assert_equal(result, 16, "SLL: 1 << 4 = 16")
        
        # Shift by zero
        result = self.alu.execute(ALU.OP_SLL, 0x12345678, 0)
        self.assert_equal(result, 0x12345678, "SLL: x << 0 = x")
        
        # Maximum shift (31 bits)
        result = self.alu.execute(ALU.OP_SLL, 1, 31)
        self.assert_equal(result, 0x80000000, "SLL: 1 << 31 = 0x80000000")
        
        # Shift with overflow
        result = self.alu.execute(ALU.OP_SLL, 0xFFFFFFFF, 1)
        self.assert_equal(result, 0xFFFFFFFE, "SLL: Shift with overflow")
        
        # Shift amount > 31 (should only use lower 5 bits)
        result = self.alu.execute(ALU.OP_SLL, 1, 36)  # 36 & 0x1F = 4
        self.assert_equal(result, 16, "SLL: Shift amount wraps (36 -> 4)")
    
    def test_srl(self):
        """Test Shift Right Logical"""
        print("\n--- Testing SRL ---")
        
        # Basic shift
        result = self.alu.execute(ALU.OP_SRL, 16, 4)
        self.assert_equal(result, 1, "SRL: 16 >> 4 = 1")
        
        # Shift by zero
        result = self.alu.execute(ALU.OP_SRL, 0x12345678, 0)
        self.assert_equal(result, 0x12345678, "SRL: x >> 0 = x")
        
        # Shift negative number (logical, so fills with 0s)
        result = self.alu.execute(ALU.OP_SRL, 0x80000000, 1)
        self.assert_equal(result, 0x40000000, "SRL: Logical shift (no sign extension)")
        
        # Maximum shift
        result = self.alu.execute(ALU.OP_SRL, 0xFFFFFFFF, 31)
        self.assert_equal(result, 1, "SRL: 0xFFFFFFFF >> 31 = 1")
    
    def test_sra(self):
        """Test Shift Right Arithmetic"""
        print("\n--- Testing SRA ---")
        
        # Positive number (behaves like SRL)
        result = self.alu.execute(ALU.OP_SRA, 16, 4)
        self.assert_equal(result, 1, "SRA: 16 >> 4 = 1")
        
        # Negative number (sign extension)
        result = self.alu.execute(ALU.OP_SRA, 0x80000000, 1)
        self.assert_equal(result, 0xC0000000, "SRA: Sign extension for negative")
        
        # Shift -1 (all ones stays all ones)
        result = self.alu.execute(ALU.OP_SRA, 0xFFFFFFFF, 4)
        self.assert_equal(result, 0xFFFFFFFF, "SRA: -1 >> 4 = -1")
        
        # Shift by zero
        result = self.alu.execute(ALU.OP_SRA, 0x80000000, 0)
        self.assert_equal(result, 0x80000000, "SRA: x >> 0 = x")
    
    def test_slt(self):
        """Test Set Less Than (signed)"""
        print("\n--- Testing SLT ---")
        
        # Positive numbers
        result = self.alu.execute(ALU.OP_SLT, 5, 10)
        self.assert_equal(result, 1, "SLT: 5 < 10 = 1")
        
        result = self.alu.execute(ALU.OP_SLT, 10, 5)
        self.assert_equal(result, 0, "SLT: 10 < 5 = 0")
        
        # Equal numbers
        result = self.alu.execute(ALU.OP_SLT, 7, 7)
        self.assert_equal(result, 0, "SLT: 7 < 7 = 0")
        
        # Negative vs positive (signed comparison)
        result = self.alu.execute(ALU.OP_SLT, 0xFFFFFFFF, 1)  # -1 < 1
        self.assert_equal(result, 1, "SLT: -1 < 1 = 1 (signed)")
        
        # Two negative numbers
        result = self.alu.execute(ALU.OP_SLT, 0xFFFFFFFE, 0xFFFFFFFF)  # -2 < -1
        self.assert_equal(result, 1, "SLT: -2 < -1 = 1")
    
    def test_sltu(self):
        """Test Set Less Than Unsigned"""
        print("\n--- Testing SLTU ---")
        
        # Basic unsigned comparison
        result = self.alu.execute(ALU.OP_SLTU, 5, 10)
        self.assert_equal(result, 1, "SLTU: 5 < 10 = 1")
        
        # Large unsigned vs small
        result = self.alu.execute(ALU.OP_SLTU, 0xFFFFFFFF, 1)
        self.assert_equal(result, 0, "SLTU: 0xFFFFFFFF < 1 = 0 (unsigned)")
        
        # Equal numbers
        result = self.alu.execute(ALU.OP_SLTU, 100, 100)
        self.assert_equal(result, 0, "SLTU: 100 < 100 = 0")
    
    def run_all_tests(self):
        """Run all test suites"""
        print("=" * 50)
        print("RISC-V ALU Unit Tests")
        print("=" * 50)
        
        self.test_add()
        self.test_sub()
        self.test_and()
        self.test_or()
        self.test_xor()
        self.test_sll()
        self.test_srl()
        self.test_sra()
        self.test_slt()
        self.test_sltu()
        
        # Print summary
        print("\n" + "=" * 50)
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_failed}")
        print("=" * 50)
        
        if self.tests_failed == 0:
            print("✓ All tests passed!")
            return 0
        else:
            print(f"✗ {self.tests_failed} test(s) failed")
            return 1


if __name__ == "__main__":
    tester = TestALU()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)