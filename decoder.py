class InstructionDecoder:
    
    def __init__(self):
        pass
    
    def decode(self, instruction):
        """
        Decode a 32-bit instruction
        Returns a dictionary with all the fields
        """
        # Extract the basic fields using bit shifting and masks, AI Start
        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x7
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F
        
        # Store in dictionary
        result = {
            'opcode': opcode,
            'rd': rd,
            'funct3': funct3,
            'rs1': rs1,
            'rs2': rs2,
            'funct7': funct7,
        }
        
        # Figure out instruction type
        inst_type = self.get_type(opcode)
        result['type'] = inst_type
        
        # Decode the immediate value based on instruction type
        if inst_type == 'I':
            result['imm'] = self.decode_i_imm(instruction)
        elif inst_type == 'S':
            result['imm'] = self.decode_s_imm(instruction)
        elif inst_type == 'B':
            result['imm'] = self.decode_b_imm(instruction)
        elif inst_type == 'U':
            result['imm'] = self.decode_u_imm(instruction)
        elif inst_type == 'J':
            result['imm'] = self.decode_j_imm(instruction)
        
        return result
    #AI End
    def decode_i_imm(self, instruction):
        """Decode I-type immediate (bits 31:20)"""
        imm = (instruction >> 20) & 0xFFF
        
        # Sign extend from 12 bits to 32 bits
        if imm & 0x800:  # if bit 11 is set (negative number)
            imm = imm | 0xFFFFF000
        
        return imm
    
    def decode_s_imm(self, instruction):
        """Decode S-type immediate"""
        # S-type splits the immediate into two parts
        # bits 31:25 are imm[11:5]
        # bits 11:7 are imm[4:0]
        upper = (instruction >> 25) & 0x7F
        lower = (instruction >> 7) & 0x1F
        
        imm = (upper << 5) | lower
        
        # Sign extend
        if imm & 0x800:
            imm = imm | 0xFFFFF000
        
        return imm
    
    def decode_b_imm(self, instruction):
        """
        Decode B-type immediate
        This one is tricky because the bits are scrambled
        """
        # Extract each piece
        bit_12 = (instruction >> 31) & 0x1
        bit_11 = (instruction >> 7) & 0x1
        bits_10_5 = (instruction >> 25) & 0x3F
        bits_4_1 = (instruction >> 8) & 0xF
        
        # Put them back together in the right order
        # bit 0 is always 0 (2-byte aligned)
        imm = (bit_12 << 12) | (bit_11 << 11) | (bits_10_5 << 5) | (bits_4_1 << 1)
        
        # Sign extend from 13 bits
        if imm & 0x1000:
            imm = imm | 0xFFFFE000
        
        return imm
    
    def decode_u_imm(self, instruction):
        """Decode U-type immediate - just the upper 20 bits"""
        return instruction & 0xFFFFF000
    
    def decode_j_imm(self, instruction):
        """
        Decode J-type immediate
        Also scrambled like B-type
        """
        bit_20 = (instruction >> 31) & 0x1
        bits_19_12 = (instruction >> 12) & 0xFF
        bit_11 = (instruction >> 20) & 0x1
        bits_10_1 = (instruction >> 21) & 0x3FF
        
        # Reconstruct (bit 0 is always 0)
        imm = (bit_20 << 20) | (bits_19_12 << 12) | (bit_11 << 11) | (bits_10_1 << 1)
        
        # Sign extend from 21 bits
        if imm & 0x100000:
            imm = imm | 0xFFE00000
        
        return imm
    
    def get_type(self, opcode):
        """Return the instruction type based on opcode"""
        
        if opcode == 0x33:
            return 'R'
        elif opcode == 0x13 or opcode == 0x03 or opcode == 0x67:
            return 'I'
        elif opcode == 0x23:
            return 'S'
        elif opcode == 0x63:
            return 'B'
        elif opcode == 0x37 or opcode == 0x17:
            return 'U'
        elif opcode == 0x6F:
            return 'J'
        else:
            return 'UNKNOWN'
    
    def get_name(self, decoded):
        """
        Get the instruction name/mnemonic
        """
        opcode = decoded['opcode']
        funct3 = decoded['funct3']
        funct7 = decoded['funct7']
        
        # R-type instructions
        if opcode == 0x33:
            if funct3 == 0x0 and funct7 == 0x00:
                return "ADD"
            elif funct3 == 0x0 and funct7 == 0x20:
                return "SUB"
            elif funct3 == 0x7:
                return "AND"
            elif funct3 == 0x6:
                return "OR"
            elif funct3 == 0x4:
                return "XOR"
            elif funct3 == 0x1:
                return "SLL"
            elif funct3 == 0x5 and funct7 == 0x00:
                return "SRL"
            elif funct3 == 0x5 and funct7 == 0x20:
                return "SRA"
        
        # I-type arithmetic
        elif opcode == 0x13:
            if funct3 == 0x0:
                return "ADDI"
            elif funct3 == 0x7:
                return "ANDI"
            elif funct3 == 0x6:
                return "ORI"
            elif funct3 == 0x4:
                return "XORI"
        
        # Load/Store
        elif opcode == 0x03 and funct3 == 0x2:
            return "LW"
        elif opcode == 0x23 and funct3 == 0x2:
            return "SW"
        
        # Branches
        elif opcode == 0x63:
            if funct3 == 0x0:
                return "BEQ"
            elif funct3 == 0x1:
                return "BNE"
            elif funct3 == 0x4:
                return "BLT"
            elif funct3 == 0x5:
                return "BGE"
        
        # Jumps
        elif opcode == 0x6F:
            return "JAL"
        elif opcode == 0x67:
            return "JALR"
        
        # Upper immediate
        elif opcode == 0x37:
            return "LUI"
        elif opcode == 0x17:
            return "AUIPC"
        
        return "UNKNOWN"


# Test it
if __name__ == "__main__":
    decoder = InstructionDecoder()
    
    print("Testing decoder with test_base.hex instructions...")
    print()
    
    # Instructions from test_base.hex
    instructions = [
        0x00500093,  # addi x1, x0, 5
        0x00A00113,  # addi x2, x0, 10
        0x002081B3,  # add x3, x1, x2
        0x40110233,  # sub x4, x2, x1
        0x000102B7,  # lui x5, 0x00010
        0x0032A023,  # sw x3, 0(x5)
        0x0002A203,  # lw x4, 0(x5)
        0x00418463,  # beq x3, x4, 8
        0x00100313,  # addi x6, x0, 1
        0x00200313,  # addi x6, x0, 2
        0x0000006F,  # jal x0, 0
    ]
    
    for i, inst in enumerate(instructions):
        decoded = decoder.decode(inst)
        name = decoder.get_name(decoded)
        print(f"{i*4:08X}: {inst:08X}  {name}")
    
    print()
    print("Decoder test complete!")