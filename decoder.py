"""
Instruction Decoder for RISC-V CPU
Added R-type and I-type immediate decoding
"""

class InstructionDecoder:
    """
    Decodes RISC-V RV32I instructions
    """
    
    def __init__(self):
        pass
    
    def decode(self, instruction):
        """
        Decode a 32-bit instruction
        
        Args:
            instruction: 32-bit instruction word
            
        Returns:
            Dictionary with decoded fields
        """
        # Extract basic fields
        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x7
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F
        
        decoded = {
            'instruction': instruction,
            'opcode': opcode,
            'rd': rd,
            'funct3': funct3,
            'rs1': rs1,
            'rs2': rs2,
            'funct7': funct7,
        }
        
        # Determine instruction type and decode immediates
        inst_type = self.get_instruction_type(opcode)
        decoded['type'] = inst_type
        
        # Decode immediates based on type
        if inst_type == 'I':
            decoded['imm'] = self._decode_i_immediate(instruction)
        
        return decoded
    
    def _decode_i_immediate(self, instruction):
        """
        Decode I-type immediate (bits 31:20)
        12-bit immediate, sign-extended
        """
        imm = (instruction >> 20) & 0xFFF
        
        # Sign extend from 12 bits to 32 bits
        if imm & 0x800:  # If bit 11 is set (negative)
            imm = imm | 0xFFFFF000  # Fill upper bits with 1s
        
        return imm
    
    def get_instruction_type(self, opcode):
        """
        Determine instruction type from opcode
        
        Returns: 'R', 'I', 'S', 'B', 'U', 'J', or 'UNKNOWN'
        """
        # R-type: register-register operations
        if opcode == 0x33:
            return 'R'
        
        # I-type: immediate operations
        elif opcode in [0x13, 0x03, 0x67]:
            return 'I'
        
        # S-type: store operations
        elif opcode == 0x23:
            return 'S'
        
        # B-type: branch operations
        elif opcode == 0x63:
            return 'B'
        
        # U-type: upper immediate
        elif opcode in [0x37, 0x17]:
            return 'U'
        
        # J-type: jump
        elif opcode == 0x6F:
            return 'J'
        
        else:
            return 'UNKNOWN'


# Test
if __name__ == "__main__":
    print("Testing Instruction Decoder with R-type and I-type...")
    
    decoder = InstructionDecoder()
    
    # Test R-type: add x3, x1, x2 (0x002081B3)
    print("\n=== R-type Test ===")
    instruction = 0x002081B3
    decoded = decoder.decode(instruction)
    print(f"Instruction: 0x{instruction:08X}")
    print(f"Type: {decoded['type']}")
    print(f"Operation: ADD x{decoded['rd']}, x{decoded['rs1']}, x{decoded['rs2']}")
    
    # Test I-type: addi x1, x0, 5 (0x00500093)
    print("\n=== I-type Test ===")
    instruction = 0x00500093
    decoded = decoder.decode(instruction)
    print(f"Instruction: 0x{instruction:08X}")
    print(f"Type: {decoded['type']}")
    print(f"Operation: ADDI x{decoded['rd']}, x{decoded['rs1']}, {decoded['imm']}")
    
    # Test I-type with negative immediate: addi x2, x0, -1 (0xFFF00113)
    print("\n=== I-type Negative Immediate Test ===")
    instruction = 0xFFF00113
    decoded = decoder.decode(instruction)
    print(f"Instruction: 0x{instruction:08X}")
    print(f"Immediate: {decoded['imm']} (should be -1)")
    
    print("\nDecoder test complete!")