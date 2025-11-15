from alu import ALU
from registers import RegisterFile
from memory import Memory
from decoder import InstructionDecoder
from loader import load_hex_file

class RISCV_CPU:
    
    def __init__(self):
        # Create all the components
        self.alu = ALU()
        self.registers = RegisterFile()
        self.memory = Memory()
        self.decoder = InstructionDecoder()
        
        self.pc = 0
        self.cycle_count = 0
        self.halted = False
    
    def load_program(self, hex_file):
        """Load program from hex file"""
        print(f"Loading: {hex_file}")
        count = load_hex_file(hex_file, self.memory, start_address=0x0)
        print(f"Loaded {count} instructions\n")
        return count
    
    def fetch(self):
        """Get instruction at current PC"""
        return self.memory.read_word(self.pc)
    
    def execute(self, instruction):
        """
        Execute one instruction
        This got pretty long but it works
        """
        # Decode it first
        decoded = self.decoder.decode(instruction)
        opcode = decoded['opcode']
        
        # R-type (register operations like add, sub, etc)
        if opcode == 0x33:
            rs1_val = self.registers.read(decoded['rs1'])
            rs2_val = self.registers.read(decoded['rs2'])
            
            funct3 = decoded['funct3']
            funct7 = decoded['funct7']
            
            # Figure out which operation
            if funct3 == 0x0:
                if funct7 == 0x00:  # ADD
                    result = self.alu.execute('ADD', rs1_val, rs2_val)
                elif funct7 == 0x20:  # SUB
                    result = self.alu.execute('SUB', rs1_val, rs2_val)
            elif funct3 == 0x7:  # AND
                result = self.alu.execute('AND', rs1_val, rs2_val)
            elif funct3 == 0x6:  # OR
                result = self.alu.execute('OR', rs1_val, rs2_val)
            elif funct3 == 0x4:  # XOR
                result = self.alu.execute('XOR', rs1_val, rs2_val)
            elif funct3 == 0x1:  # SLL
                result = self.alu.execute('SLL', rs1_val, rs2_val)
            elif funct3 == 0x5:
                if funct7 == 0x00:  # SRL
                    result = self.alu.execute('SRL', rs1_val, rs2_val)
                elif funct7 == 0x20:  # SRA
                    result = self.alu.execute('SRA', rs1_val, rs2_val)
            
            self.registers.write(decoded['rd'], result)
            self.pc += 4
        
        # I-type immediate arithmetic (like addi)
        elif opcode == 0x13:
            rs1_val = self.registers.read(decoded['rs1'])
            imm = decoded['imm']
            funct3 = decoded['funct3']
            
            if funct3 == 0x0:  # ADDI
                result = self.alu.execute('ADD', rs1_val, imm)
            elif funct3 == 0x7:  # ANDI
                result = self.alu.execute('AND', rs1_val, imm)
            elif funct3 == 0x6:  # ORI
                result = self.alu.execute('OR', rs1_val, imm)
            elif funct3 == 0x4:  # XORI
                result = self.alu.execute('XOR', rs1_val, imm)
            # AI Start - shift immediate handling
            # Asked AI how to tell SRLI from SRAI - they have same funct3
            # AI said check bit 30 which shows up as bit 10 in decoded immediate
            elif funct3 == 0x1:  # SLLI
                result = self.alu.execute('SLL', rs1_val, imm & 0x1F)
            elif funct3 == 0x5:
                # Check bit 10 to distinguish SRLI vs SRAI
                if (decoded['imm'] >> 10) == 0x00:
                    result = self.alu.execute('SRL', rs1_val, imm & 0x1F)
                else:
                    result = self.alu.execute('SRA', rs1_val, imm & 0x1F)
            # AI End
            
            self.registers.write(decoded['rd'], result)
            self.pc += 4
        
        # Load instructions
        elif opcode == 0x03:
            rs1_val = self.registers.read(decoded['rs1'])
            address = (rs1_val + decoded['imm']) & 0xFFFFFFFF
            
            if decoded['funct3'] == 0x2:  # LW
                value = self.memory.read_word(address)
                self.registers.write(decoded['rd'], value)
            
            self.pc += 4
        
        # Store instructions
        elif opcode == 0x23:
            rs1_val = self.registers.read(decoded['rs1'])
            rs2_val = self.registers.read(decoded['rs2'])
            address = (rs1_val + decoded['imm']) & 0xFFFFFFFF
            
            if decoded['funct3'] == 0x2:  # SW
                self.memory.write_word(address, rs2_val)
            
            self.pc += 4
        
        # Branch instructions
        elif opcode == 0x63:
            rs1_val = self.registers.read(decoded['rs1'])
            rs2_val = self.registers.read(decoded['rs2'])
            
            branch_taken = False
            funct3 = decoded['funct3']
            
            if funct3 == 0x0:  # BEQ
                branch_taken = (rs1_val == rs2_val)
            elif funct3 == 0x1:  # BNE
                branch_taken = (rs1_val != rs2_val)
            # AI Start - signed comparison for BLT/BGE
            # This was really tricky - branches weren't working
            # BLT was treating -1 as bigger than 5
            # Asked AI how to handle signed comparison in Python
            # AI said: if value >= 0x80000000, subtract 0x100000000 to get signed
            elif funct3 == 0x4:  # BLT - signed comparison
                # Convert to signed for comparison
                if rs1_val >= 0x80000000:
                    rs1_signed = rs1_val - 0x100000000
                else:
                    rs1_signed = rs1_val
                
                if rs2_val >= 0x80000000:
                    rs2_signed = rs2_val - 0x100000000
                else:
                    rs2_signed = rs2_val
                
                branch_taken = (rs1_signed < rs2_signed)
            elif funct3 == 0x5:  # BGE - signed comparison
                # Same conversion as BLT
                if rs1_val >= 0x80000000:
                    rs1_signed = rs1_val - 0x100000000
                else:
                    rs1_signed = rs1_val
                
                if rs2_val >= 0x80000000:
                    rs2_signed = rs2_val - 0x100000000
                else:
                    rs2_signed = rs2_val
                
                branch_taken = (rs1_signed >= rs2_signed)
            # AI End
            
            if branch_taken:
                self.pc = (self.pc + decoded['imm']) & 0xFFFFFFFF
            else:
                self.pc += 4
        
        # JAL
        elif opcode == 0x6F:
            # Save return address
            self.registers.write(decoded['rd'], self.pc + 4)
            # Jump
            self.pc = (self.pc + decoded['imm']) & 0xFFFFFFFF
        
        # JALR
        elif opcode == 0x67:
            rs1_val = self.registers.read(decoded['rs1'])
            # AI Start - JALR address alignment
            # Asked AI why JALR clears LSB - AI said instructions must be 2-byte aligned
            target = (rs1_val + decoded['imm']) & 0xFFFFFFFE  # Clear LSB
            # AI End
            self.registers.write(decoded['rd'], self.pc + 4)
            self.pc = target
        
        # LUI
        elif opcode == 0x37:
            self.registers.write(decoded['rd'], decoded['imm'])
            self.pc += 4
        
        # AUIPC
        elif opcode == 0x17:
            result = (self.pc + decoded['imm']) & 0xFFFFFFFF
            self.registers.write(decoded['rd'], result)
            self.pc += 4
        
        else:
            print(f"Unknown opcode: 0x{opcode:02X}")
            self.pc += 4
    
    def run(self, max_cycles=1000, verbose=False):
        """Run the CPU until halt or max cycles"""
        print("Starting execution...")
        print(f"PC = 0x{self.pc:08X}\n")
        
        while not self.halted and self.cycle_count < max_cycles:
            # Fetch instruction
            instruction = self.fetch()
            
            # AI Start - halt detection
            # Found that jal x0, 0 (infinite loop) is used as halt
            # This is 0x0000006F in machine code
            if instruction == 0x0000006F:
                print(f"Halt detected at cycle {self.cycle_count}")
                self.halted = True
                break
            # AI End
            
            # Check if we're in uninitialized memory
            if instruction == 0:
                print(f"Reached uninitialized memory at PC=0x{self.pc:08X}")
                self.halted = True
                break
            
            if verbose:
                decoded = self.decoder.decode(instruction)
                name = self.decoder.get_name(decoded)
                print(f"[{self.cycle_count}] PC=0x{self.pc:08X} | {instruction:08X} | {name}")
            
            # Execute it
            self.execute(instruction)
            self.cycle_count += 1
        
        print(f"\nFinished after {self.cycle_count} cycles")
        self.print_final_state()
    
    def print_final_state(self):
        """Print the final state of registers and memory"""
        print("\n" + "=" * 60)
        print("FINAL STATE")
        print("=" * 60)
        print(f"Cycles: {self.cycle_count}")
        print(f"Final PC: 0x{self.pc:08X}")
        
        # Show registers
        self.registers.dump()
        
        # Show memory if anything was written
        print("\nMemory (non-zero):")
        memory_empty = True
        for addr in sorted(self.memory.data.keys()):
            val = self.memory.data[addr]
            if val != 0:
                print(f"  [0x{addr:08X}] = 0x{val:08X} ({val})")
                memory_empty = False
        
        if memory_empty:
            print("  (nothing written)")
        
        print("=" * 60)


# Run the CPU
if __name__ == "__main__":
    import sys
    
    cpu = RISCV_CPU()
    
    # Get filename from command line
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "test_base.hex"
    
    try:
        cpu.load_program(filename)
        cpu.run(max_cycles=100, verbose=True)
    except FileNotFoundError:
        print(f"Error: Can't find file '{filename}'")
        print("Usage: python cpu.py <hex_file>")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()