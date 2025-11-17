class ALU:
    """
    32-bit ALU for RISC-V processor
    """
    
    def __init__(self):
        self.result = 0
        self.zero_flag = False
    
    def execute(self, operation, a, b):
        """Execute an ALU operation and return result"""
        # Ensure 32-bit values
        a = a & 0xFFFFFFFF
        b = b & 0xFFFFFFFF
        
        if operation == 'ADD':
            self.result = (a + b) & 0xFFFFFFFF
        elif operation == 'SUB':
            self.result = (a - b) & 0xFFFFFFFF
        elif operation == 'AND':
            self.result = a & b
        elif operation == 'OR':
            self.result = a | b
        elif operation == 'XOR':
            self.result = a ^ b
        elif operation == 'SLL':
            shift = b & 0x1F
            self.result = (a << shift) & 0xFFFFFFFF
        elif operation == 'SRL':
            shift = b & 0x1F
            self.result = (a >> shift) & 0xFFFFFFFF
        elif operation == 'SRA':
            # Shift right arithmetic - preserve sign bit
            shift = b & 0x1F
            
            # AI Start - arithmetic right shift with sign extension
            # Had trouble with this - needed to preserve sign bit for negative numbers
            # Asked AI how to handle sign extension in Python
            # AI explained: check MSB, if set then fill with 1s from left
            if a & 0x80000000:
                # Fill with 1s from the left
                result = a >> shift
                sign_bits = 0xFFFFFFFF << (32 - shift)
                self.result = (result | sign_bits) & 0xFFFFFFFF
            else:
                # Positive numbers just shift normally
                self.result = (a >> shift) & 0xFFFFFFFF
            # AI End
        elif operation == 'SLT':
            # Set less than (signed)
            # Convert to signed integers
            if a & 0x80000000:
                a_signed = a - 0x100000000
            else:
                a_signed = a
            
            if b & 0x80000000:
                b_signed = b - 0x100000000
            else:
                b_signed = b
            
            self.result = 1 if a_signed < b_signed else 0
        elif operation == 'SLTU':
            # Set less than unsigned - just compare directly
            self.result = 1 if a < b else 0
        else:
            print(f"Error: Unknown operation {operation}")
            self.result = 0
        
        # Update zero flag for branch operations
        self.zero_flag = (self.result == 0)
        
        return self.result
    
    def get_result(self):
        """Get the last result"""
        return self.result
    
    def is_zero(self):
        """Check if result is zero"""
        return self.zero_flag


# Test
if __name__ == "__main__":
    print("Testing ALU operations...")
    
    alu = ALU()
    
    # Test a few operations
    tests = [
        ('ADD', 5, 10, 15),
        ('SUB', 10, 5, 5),
        ('AND', 0xFF, 0x0F, 0x0F),
        ('SLL', 1, 4, 16),
        ('SRA', 0x80000000, 1, 0xC0000000),
        ('SLT', 0xFFFFFFFF, 1, 1),  # -1 < 1
    ]
    
    passed = 0
    for op, a, b, expected in tests:
        result = alu.execute(op, a, b)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status}: {op} -> 0x{result:08X} (expected 0x{expected:08X})")
        if result == expected:
            passed += 1
    
    print(f"\n{passed}/{len(tests)} tests passed")