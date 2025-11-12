"""
ALU (Arithmetic Logic Unit) for RISC-V CPU
Refactored to use private methods for better organization
"""

class ALU:
    """
    32-bit ALU for RISC-V processor
    Supports arithmetic, logical, shift, and comparison operations
    """
    
    def __init__(self):
        self.result = 0
        self.zero_flag = False
    
    def execute(self, operation, a, b):
        """Execute an ALU operation and return result"""
        # Ensure 32-bit values
        a = a & 0xFFFFFFFF
        b = b & 0xFFFFFFFF
        
        # Dispatch to appropriate operation
        if operation == 'ADD':
            self.result = self._add(a, b)
        elif operation == 'SUB':
            self.result = self._sub(a, b)
        elif operation == 'AND':
            self.result = self._and(a, b)
        elif operation == 'OR':
            self.result = self._or(a, b)
        elif operation == 'XOR':
            self.result = self._xor(a, b)
        elif operation == 'SLL':
            self.result = self._sll(a, b)
        elif operation == 'SRL':
            self.result = self._srl(a, b)
        elif operation == 'SRA':
            self.result = self._sra(a, b)
        elif operation == 'SLT':
            self.result = self._slt(a, b)
        elif operation == 'SLTU':
            self.result = self._sltu(a, b)
        else:
            print(f"Error: Unknown operation {operation}")
            self.result = 0
        
        # Update zero flag
        self.zero_flag = (self.result == 0)
        
        return self.result
    
    def _add(self, a, b):
        """32-bit addition"""
        return (a + b) & 0xFFFFFFFF
    
    def _sub(self, a, b):
        """32-bit subtraction"""
        return (a - b) & 0xFFFFFFFF
    
    def _and(self, a, b):
        """Bitwise AND"""
        return a & b
    
    def _or(self, a, b):
        """Bitwise OR"""
        return a | b
    
    def _xor(self, a, b):
        """Bitwise XOR"""
        return a ^ b
    
    def _sll(self, a, b):
        """Shift left logical"""
        shift = b & 0x1F
        return (a << shift) & 0xFFFFFFFF
    
    def _srl(self, a, b):
        """Shift right logical"""
        shift = b & 0x1F
        return (a >> shift) & 0xFFFFFFFF
    
    def _sra(self, a, b):
        """Shift right arithmetic - preserves sign bit"""
        shift = b & 0x1F
        
        # Check if MSB is set (negative number)
        if a & 0x80000000:
            # Fill with 1s from the left
            result = a >> shift
            sign_bits = 0xFFFFFFFF << (32 - shift)
            return (result | sign_bits) & 0xFFFFFFFF
        else:
            # Positive numbers just shift normally
            return (a >> shift) & 0xFFFFFFFF
    
    def _slt(self, a, b):
        """Set less than (signed comparison)"""
        # Convert to signed integers
        if a & 0x80000000:
            a_signed = a - 0x100000000
        else:
            a_signed = a
        
        if b & 0x80000000:
            b_signed = b - 0x100000000
        else:
            b_signed = b
        
        return 1 if a_signed < b_signed else 0
    
    def _sltu(self, a, b):
        """Set less than unsigned"""
        return 1 if a < b else 0
    
    def get_result(self):
        """Get the last result"""
        return self.result
    
    def is_zero(self):
        """Check if result is zero"""
        return self.zero_flag


# Test module
if __name__ == "__main__":
    print("ALU Module Test")
    print("=" * 40)
    
    alu = ALU()
    
    # Test a few operations, AI Start
    tests = [
        ('ADD', 5, 10, 15),
        ('SUB', 10, 5, 5),
        ('AND', 0xFF, 0x0F, 0x0F),
        ('SLL', 1, 4, 16),
        ('SRA', 0x80000000, 1, 0xC0000000),
        ('SLT', 0xFFFFFFFF, 1, 1),  # -1 < 1
    # AI End
    ]
    
    passed = 0
    for op, a, b, expected in tests:
        result = alu.execute(op, a, b)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status}: {op} -> 0x{result:08X} (expected 0x{expected:08X})")
        if result == expected:
            passed += 1
    
    print(f"\n{passed}/{len(tests)} tests passed")