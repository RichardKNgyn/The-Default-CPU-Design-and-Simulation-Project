"""
Instruction Decoder for RISC-V CPU
Decodes 32-bit instructions into their component fields
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
        # Extract basic fields that are common across formats
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
        
        return decoded
    
    def get_instruction_type(self, opcode):
        """
        Determine instruction type from opcode
        
        Returns: 'R', 'I', 'S', 'B', 'U', 'J', or 'UNKNOWN'
        """
        # R-type: register-register operations
        if opcode == 0x33:  # ADD, SUB, AND, OR, XOR, SLL, SRL, SRA
            return 'R'
        
        # I-type: immediate operations
        elif opcode in [0x13, 0x03, 0x67]:  # ADDI, LW, JALR, etc.
            return 'I'
        
        # S-type: store operations
        elif opcode == 0x23:  # SW, SH, SB
            return 'S'
        
        # B-type: branch operations
        elif opcode == 0x63:  # BEQ, BNE, BLT, BGE
            return 'B'
        
        # U-type: upper immediate
        elif opcode in [0x37, 0x17]:  # LUI, AUIPC
            return 'U'
        
        # J-type: jump
        elif opcode == 0x6F:  # JAL
            return 'J'
        
        else:
            return 'UNKNOWN'


# Test
if __name__ == "__main__":
    print("Testing Instruction Decoder...")
    
    decoder = InstructionDecoder()
    
    # Test with ADD instruction: add x3, x1, x2
    # Should be: opcode=0x33, rd=3, rs1=1, rs2=2, funct3=0, funct7=0
    instruction = 0x002081B3
    decoded = decoder.decode(instruction)
    
    print(f"\nInstruction: 0x{instruction:08X}")
    print(f"Opcode: 0x{decoded['opcode']:02X}")
    print(f"rd: x{decoded['rd']}")
    print(f"rs1: x{decoded['rs1']}")
    print(f"rs2: x{decoded['rs2']}")
    print(f"funct3: 0x{decoded['funct3']:X}")
    print(f"funct7: 0x{decoded['funct7']:02X}")
    print(f"Type: {decoder.get_instruction_type(decoded['opcode'])}")
    
    print("\nBasic decoder test complete!")