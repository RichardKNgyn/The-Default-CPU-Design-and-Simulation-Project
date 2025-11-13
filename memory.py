"""
Memory module for RISC-V CPU
Handles both instruction and data memory
"""

class Memory:
    """
    Simple memory system using dictionary for sparse storage
    Byte-addressable but we'll primarily use word access
    """
    
    def __init__(self, size=0x100000):  # 1MB default
        """
        Initialize memory
        Args:
            size: Memory size in bytes (not actually used with dict, just for reference)
        """
        self.data = {}  # Dictionary for sparse storage
        self.size = size
    
    def read_word(self, address):
        """
        Read a 32-bit word from memory
        
        Args:
            address: Byte address (should be word-aligned)
        Returns:
            32-bit value
        """
        # Word-align the address
        address = address & 0xFFFFFFFC
        
        # Return value or 0 if not initialized
        return self.data.get(address, 0)
    
    def write_word(self, address, value):
        """
        Write a 32-bit word to memory
        
        Args:
            address: Byte address (should be word-aligned)
            value: 32-bit value to write
        """
        # Word-align the address
        address = address & 0xFFFFFFFC
        
        # Store as 32-bit value
        self.data[address] = value & 0xFFFFFFFF
    
    def read_byte(self, address):
        """
        Read a single byte from memory
        
        Args:
            address: Byte address
        Returns:
            8-bit value
        """
        # Find which word this byte is in
        word_addr = address & 0xFFFFFFFC
        byte_offset = address & 0x3
        
        word = self.data.get(word_addr, 0)
        
        # Extract the correct byte (little-endian)
        byte_value = (word >> (byte_offset * 8)) & 0xFF
        return byte_value
    
    def write_byte(self, address, value):
        """
        Write a single byte to memory
        
        Args:
            address: Byte address
            value: 8-bit value to write
        """
        # Find which word this byte is in
        word_addr = address & 0xFFFFFFFC
        byte_offset = address & 0x3
        
        # Read current word value
        word = self.data.get(word_addr, 0)
        
        # Clear the target byte and insert new value
        mask = 0xFF << (byte_offset * 8)
        word = (word & ~mask) | ((value & 0xFF) << (byte_offset * 8))
        
        self.data[word_addr] = word
    
    def clear(self):
        """Clear all memory"""
        self.data = {}
    
    def dump(self, start_addr, num_words):
        """
        Dump memory contents
        
        Args:
            start_addr: Starting address
            num_words: Number of words to display
        """
        print(f"\n=== Memory Dump (0x{start_addr:08X}) ===")
        for i in range(num_words):
            addr = start_addr + (i * 4)
            value = self.read_word(addr)
            if value != 0:  # Only show non-zero values
                print(f"[0x{addr:08X}] = 0x{value:08X}")


# Test
if __name__ == "__main__":
    print("Testing Memory module...")
    
    mem = Memory()
    
    # Test word access
    mem.write_word(0x1000, 0x12345678)
    value = mem.read_word(0x1000)
    print(f"Word at 0x1000 = 0x{value:08X} (expected 0x12345678)")
    
    # Test unaligned access (should align automatically)
    mem.write_word(0x1002, 0xABCDEF00)  # Will write to 0x1000
    value = mem.read_word(0x1000)
    print(f"Word at 0x1000 = 0x{value:08X} (should be 0xABCDEF00 - overwritten)")
    
    # Test byte access
    mem.write_byte(0x2000, 0xAB)
    mem.write_byte(0x2001, 0xCD)
    mem.write_byte(0x2002, 0xEF)
    mem.write_byte(0x2003, 0x12)
    value = mem.read_word(0x2000)
    print(f"Word at 0x2000 = 0x{value:08X} (expected 0x12EFCDAB - little endian)")
    
    print("\nMemory test complete!")