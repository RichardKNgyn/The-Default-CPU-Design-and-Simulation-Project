class RegisterFile:
    """
    RISC-V register file with 32 registers
    """
    
    def __init__(self):
        # 32 registers, all initialized to 0
        self.registers = [0] * 32
    
    def read(self, reg_num):
        """
        Read value from a register
        
        Args:
            reg_num: Register number (0-31)
        Returns:
            32-bit value from register
        """
        if 0 <= reg_num < 32:
            return self.registers[reg_num]
        else:
            print(f"Error: Invalid register number {reg_num}")
            return 0
    
    def write(self, reg_num, value):
        """
        Write value to a register
        x0 always remains 0
        
        Args:
            reg_num: Register number (0-31)
            value: 32-bit value to write
        """
        if reg_num == 0:
            # x0 is hardwired to zero, ignore writes
            return
        
        if 0 <= reg_num < 32:
            # Ensure 32-bit value
            self.registers[reg_num] = value & 0xFFFFFFFF
        else:
            print(f"Error: Invalid register number {reg_num}")
    
    def reset(self):
        """Reset all registers to 0"""
        self.registers = [0] * 32
    
    def dump(self):
        """Print all register values"""
        print("\n=== Register File ===")
        for i in range(0, 32, 4):
            print(f"x{i:2d}-x{i+3:2d}: ", end="")
            for j in range(4):
                if i + j < 32:
                    print(f"0x{self.registers[i+j]:08X} ", end="")
            print()


# Test
if __name__ == "__main__":
    print("Testing Register File...")
    
    rf = RegisterFile()
    
    # Test write and read
    rf.write(1, 0x12345678)
    rf.write(2, 0xABCDEF00)
    
    print(f"x1 = 0x{rf.read(1):08X} (expected 0x12345678)")
    print(f"x2 = 0x{rf.read(2):08X} (expected 0xABCDEF00)")
    
    # Test x0 is always 0
    rf.write(0, 0xFFFFFFFF)
    print(f"x0 = 0x{rf.read(0):08X} (expected 0x00000000)")
    
    # Test overflow handling
    rf.write(5, 0x1FFFFFFFF)  # More than 32 bits
    print(f"x5 = 0x{rf.read(5):08X} (should be masked to 32 bits)")
    
    print("\nRegister file test complete!")