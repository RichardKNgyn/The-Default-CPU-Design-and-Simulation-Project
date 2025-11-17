# RISC-V CPU Simulator

**Author:** Richard Nguyen
**Course:** Computer Architecture  
**Project:** 32-bit RISC-V Single-Cycle CPU Implementation

## Overview

This project implements a single-cycle 32-bit RISC-V CPU simulator that supports a subset of the RV32I instruction set architecture. The CPU is implemented in Python to focus on understanding processor architecture concepts.


### Arithmetic Operations
- `ADD`, `SUB` - Register-register arithmetic
- `ADDI` - Add immediate

### Logical Operations
- `AND`, `OR`, `XOR` - Register-register logical
- `ANDI`, `ORI`, `XORI` - Logical with immediate

### Shift Operations
- `SLL`, `SRL`, `SRA` - Register-register shifts
- `SLLI`, `SRLI`, `SRAI` - Immediate shifts

### Memory Operations
- `LW` - Load word from memory
- `SW` - Store word to memory

### Control Flow
- `BEQ`, `BNE` - Branch on equal/not equal
- `BLT`, `BGE` - Branch on less than / greater or equal (signed)
- `JAL` - Jump and link
- `JALR` - Jump and link register

### Upper Immediate
- `LUI` - Load upper immediate
- `AUIPC` - Add upper immediate to PC

## Project Structure

```
riscv-cpu/
├── README.md              # This file
├── AI_USAGE.md            # Detailed AI assistance documentation
│
├── alu.py                 # Arithmetic Logic Unit
├── registers.py           # 32-register file
├── memory.py              # Memory system (instruction + data)
├── decoder.py             # Instruction decoder
├── loader.py              # Hex file loader
├── cpu.py                 # Main CPU implementation
│
├── test_alu.py            # ALU unit tests
├── test_decoder.py        # Decoder unit tests
├── test_integration.py    # Component integration tests
├── test_cpu.py            # Full CPU tests
│
├── test_base.hex          # Provided test program
└── test_*.hex             # Generated test programs
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/riscv-cpu.git
cd riscv-cpu

# Verify Python version
python --version
```

## Usage

### Running the CPU

```bash
# Run with the provided test program
python cpu.py test_base.hex

# Run with verbose output (shows each instruction)
python cpu.py test_base.hex

# Run with a custom program
python cpu.py your_program.hex
```

### Running Tests

```bash
# Test individual components
python test_alu.py           # Test ALU operations
python test_decoder.py       # Test instruction decoder
python test_integration.py   # Test component integration

# Test complete CPU
python test_cpu.py           # Run full CPU test suite
```

## Example Output

```
Loading: test_base.hex
Loaded 11 instructions

Starting execution...
PC = 0x00000000

[0] PC=0x00000000 | 00500093 | ADDI
[1] PC=0x00000004 | 00A00113 | ADDI
[2] PC=0x00000008 | 002081B3 | ADD
[3] PC=0x0000000C | 40110233 | SUB
[4] PC=0x00000010 | 000102B7 | LUI
[5] PC=0x00000014 | 0032A023 | SW
[6] PC=0x00000018 | 0002A203 | LW
[7] PC=0x0000001C | 00418463 | BEQ
[8] PC=0x00000024 | 00200313 | ADDI
[9] PC=0x00000028 | 0000006F | JAL
Halt detected at cycle 10

Finished after 10 cycles

============================================================
FINAL STATE
============================================================
Cycles: 10
Final PC: 0x00000028

=== Register File ===
x 0-x 3: 0x00000000 0x00000005 0x0000000A 0x0000000F 
x 4-x 7: 0x0000000F 0x00010000 0x00000002 0x00000000 
...

Memory (non-zero):
  [0x00010000] = 0x0000000F (15)
============================================================
```

## Creating Your Own Programs

### Using RARS Assembler

1. Write RISC-V assembly code:
```assembly
.text
.globl _start
_start:
    addi x1, x0, 10
    addi x2, x0, 20
    add x3, x1, x2
    jal x0, 0
```

2. Assemble using RARS (https://github.com/TheThirdOne/rars)
3. Export as hex file (one 32-bit word per line)
4. Run with your CPU simulator

### Manual Hex Format

Create a `.hex` file with one 32-bit instruction per line:
```
00A00093
01400113
002081B3
0000006F
```

## Architecture Details

### Single-Cycle Design

The CPU follows a classic single-cycle architecture:

1. **Fetch**: Read instruction from memory at PC
2. **Decode**: Extract opcode, registers, and immediate
3. **Execute**: Perform operation using ALU or memory
4. **Write Back**: Update register file if needed
5. **PC Update**: Increment PC or jump to target

### Components

**ALU (alu.py)**
- 32-bit arithmetic and logical operations
- Handles signed/unsigned operations
- Sign extension for arithmetic right shift

**Register File (registers.py)**
- 32 general-purpose registers (x0-x31)
- x0 hardwired to zero (reads always return 0, writes ignored)
- 32-bit values

**Memory (memory.py)**
- Dictionary-based sparse storage
- Word-aligned access (4 bytes)
- Separate address spaces for instructions and data

**Decoder (decoder.py)**
- Supports all RISC-V instruction formats (R, I, S, B, U, J)
- Extracts opcodes, registers, function codes
- Sign-extends immediate values

**CPU (cpu.py)**
- Integrates all components
- Single-cycle execution
- Halt detection (JAL x0, 0)
- Verbose output mode for debugging

## Testing

The project includes comprehensive tests at multiple levels:

### Unit Tests
- **test_alu.py**: Tests all ALU operations with edge cases
- **test_decoder.py**: Tests instruction decoding for all formats

### Integration Tests
- **test_integration.py**: Tests component interactions
- **test_cpu.py**: Tests complete programs

### Test Coverage
- ✅ All required instructions
- ✅ Arithmetic overflow/underflow
- ✅ Signed/unsigned operations
- ✅ Branch taken/not taken
- ✅ Memory load/store
- ✅ Jump operations

## Development Process

### Timeline

**Day 1-2: Foundation**
- Implemented ALU with all operations
- Created register file and memory system
- Built hex file loader

**Day 3: Decoder**
- Implemented instruction decoder
- Handled all immediate formats
- Debugged B-type and J-type bit scrambling

**Day 4-5: CPU Integration**
- Integrated all components
- Implemented instruction execution
- Debugged signed comparison for branches
- Added comprehensive testing

**Day 6: Testing & Documentation**
- Created test suite
- Verified against RARS simulator
- Wrote documentation
- Added AI usage log

### Challenges & Solutions

**Challenge 1: Arithmetic Right Shift (SRA)**
- Problem: Python's >> doesn't preserve sign bit
- Solution: Manual sign extension with bit masking
- See AI_USAGE.md for details

**Challenge 2: Signed Branch Comparisons**
- Problem: Python has unbounded integers, not fixed-width signed
- Solution: Convert to signed by subtracting 0x100000000 if MSB set
- Most time-consuming debug (3 hours)
- See AI_USAGE.md for complete explanation

**Challenge 3: B-type/J-type Immediate Encoding**
- Problem: Bit scrambling in RISC-V spec was confusing
- Solution: Carefully extracted each bit group per spec
- See AI_USAGE.md for details

## AI Usage

This project used AI assistance for specific technical challenges, primarily:
- Understanding RISC-V specification details
- Python-specific implementation questions
- Debugging complex issues

**All AI assistance is:**
- Clearly marked with `# AI Start/End` comments in code
- Fully documented in AI_USAGE.md
- Limited to ~14% of total code

**See AI_USAGE.md for complete documentation including:**
- Specific prompts and responses
- What was AI-assisted vs. what I wrote
- Time spent on each component
- Learning process and debugging stories

## Known Limitations

- Only supports word-aligned memory access (no LB, LH, SB, SH)
- No multiply/divide instructions (M extension)
- No floating-point (F/D extensions)
- No compressed instructions (C extension)
- No interrupts or exceptions
- No pipelining (single-cycle only)


## Resources

### RISC-V References
- [RISC-V ISA Specification](https://riscv.org/technical/specifications/)
- [RISC-V Green Card](https://www.cl.cam.ac.uk/teaching/1617/ECAD+Arch/files/docs/RISCVGreenCardv8-20151013.pdf)
- Computer Organization and Design: RISC-V Edition (Patterson & Hennessy)

### Tools
- [RARS Simulator](https://github.com/TheThirdOne/rars) - For assembling and testing
- Python 3.7+ - Implementation language

### Learning Resources
- RISC-V Reader (An Open Architecture Atlas)
- Berkeley CS61C Course Materials
- MIT 6.004 Course Materials

---

**Last Updated:** [11/16/25]  
**Project Status:** Complete and Functional ✅