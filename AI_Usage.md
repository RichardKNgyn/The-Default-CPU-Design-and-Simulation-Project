# AI Usage Documentation

## Overview
This document details all AI assistance used in this RISC-V CPU project. AI was primarily used to understand RISC-V specification details and debug specific issues, not to generate entire code files.

**AI Tools Used:** Gemini and Claude for technical questions and debugging

**Percentage of AI-assisted code:** Approximately 15-20% of implementation (marked with `# AI Start/End` comments)

---

## File-by-File AI Assistance

### alu.py

#### Arithmetic Right Shift (SRA) - Lines 42-54
**Location:** Marked with `# AI Start/End`

**Problem:** Implementing SRA with sign extension was confusing. Regular right shift (>>) doesn't preserve the sign bit in Python.

**Initial attempt:** Used regular `>>` shift - worked for positive numbers but not negative.

**Prompt to AI:** "How do I implement arithmetic right shift in Python that preserves the sign bit for 32-bit values?"

**AI Response:**
- Check if MSB (bit 31) is set using `value & 0x80000000`
- If set (negative), need to fill left side with 1s
- Create mask: `0xFFFFFFFF << (32 - shift_amount)`
- OR the result with the mask

**What I implemented:**
```python
if a & 0x80000000:
    result = a >> shift
    sign_bits = 0xFFFFFFFF << (32 - shift)
    self.result = (result | sign_bits) & 0xFFFFFFFF
else:
    self.result = (a >> shift) & 0xFFFFFFFF
```

**Testing:** Created test cases with 0x80000000 >> 1, verified it returns 0xC0000000 (sign extended)


---

### decoder.py

#### B-type and J-type Immediate Decoding - Lines 88-131
**Location:** Marked with `# AI Start/End`

**Problem:** B-type and J-type immediates have scrambled bit positions. Reading the RISC-V spec diagrams was confusing.

**Challenge:** 
- B-type: imm[12|10:5|4:1|11] comes from inst[31|30:25|11:8|7]
- J-type: imm[20|10:1|11|19:12] comes from inst[31|30:21|20|19:12]

**Prompt to AI:** "Why are the bits reordered in RISC-V B-type and J-type immediates? Can you explain the bit positions?"

**AI Response:**
- Bit scrambling is for hardware efficiency
- Keeps immediate bits in consistent instruction positions across formats
- Minimizes multiplexing in hardware decoders
- Provided breakdown of which instruction bits map to which immediate bits

**What I did:**
1. Drew out the bit mappings from RISC-V spec
2. Used AI explanation to understand the pattern
3. Implemented extraction for each bit group
4. Tested with known branch/jump instructions

**Example for B-type:**
```python
bit_12 = (instruction >> 31) & 0x1
bit_11 = (instruction >> 7) & 0x1
bits_10_5 = (instruction >> 25) & 0x3F
bits_4_1 = (instruction >> 8) & 0xF
imm = (bit_12 << 12) | (bit_11 << 11) | (bits_10_5 << 5) | (bits_4_1 << 1)
```

**Resources used:**
- RISC-V Specification Volume 1, Chapter 2
- RISC-V Green Card
- AI clarification on bit positions


---

### cpu.py

#### 1. Shift Immediate Instructions - Lines 88-97
**Location:** Marked with `# AI Start/End`

**Problem:** SRLI and SRAI both have funct3 = 0x5, couldn't tell them apart.

**Prompt to AI:** "How do I distinguish between SRLI and SRAI instructions in RISC-V? They have the same funct3 value."

**AI Response:**
- Check bit 30 of the instruction
- In the I-type immediate encoding, bit 30 appears as bit 10 of the decoded immediate
- SRLI: bit 30 = 0
- SRAI: bit 30 = 1

**Implementation:**
```python
if (decoded['imm'] >> 10) == 0x00:
    result = self.alu.execute('SRL', rs1_val, imm & 0x1F)
else:
    result = self.alu.execute('SRA', rs1_val, imm & 0x1F)
```

**Also learned:** Shift amount is only lower 5 bits (& 0x1F) per RISC-V spec

---

#### 2. Signed Comparison for Branches - Lines 131-159 ⭐ MOST IMPORTANT
**Location:** Marked with `# AI Start/End`

**Problem:** BLT and BGE branch instructions weren't working. Branch was comparing 0xFFFFFFFF > 5, but -1 should be less than 5.

**Initial attempts:**
- Tried regular Python comparison - wrong for negative numbers
- Tried casting to int - Python ints are unbounded, doesn't work
- Spent about 2 hours debugging before asking for help

**Prompt to AI:** "How do I compare 32-bit unsigned integers as signed integers in Python for RISC-V BLT instruction? Python doesn't have fixed-width signed types."

**AI Response:**
- Python integers are unbounded and always unsigned conceptually
- To treat as signed: if value >= 0x80000000 (MSB set), subtract 0x100000000
- This converts to Python's negative integer representation
- Then comparison works correctly

**Implementation:**
```python
if rs1_val >= 0x80000000:
    rs1_signed = rs1_val - 0x100000000
else:
    rs1_signed = rs1_val

if rs2_val >= 0x80000000:
    rs2_signed = rs2_val - 0x100000000
else:
    rs2_signed = rs2_val

branch_taken = (rs1_signed < rs2_signed)
```

**Testing:**
- Created test: 5 < 10 (both positive) ✓
- Created test: -1 < 5 (negative vs positive) ✓
- Created test: -5 < -1 (both negative) ✓
- All work correctly now

**Note:** I repeated this code for both BLT (funct3=0x4) and BGE (funct3=0x5). Could refactor into a helper function but kept it simple.

---

#### 3. JALR Address Alignment - Lines 180-182
**Location:** Marked with `# AI Start/End`

**Problem:** Implementing JALR, wasn't sure about the `& 0xFFFFFFFE` in target calculation.

**Prompt to AI:** "Why does RISC-V JALR instruction clear the least significant bit of the target address?"

**AI Response:**
- RISC-V requires instructions to be aligned on 2-byte boundaries (halfword aligned)
- LSB must always be 0
- JALR explicitly clears bit 0 to ensure alignment
- This is in RISC-V spec Section 2.5

**Implementation:**
```python
target = (rs1_val + decoded['imm']) & 0xFFFFFFFE
```

**Verification:** Checked RISC-V spec, confirmed this is required

---

#### 4. Halt Detection - Lines 206-212
**Location:** Marked with `# AI Start/End`

**Problem:** How to know when the program is done? RISC-V doesn't have a "halt" instruction.

**Research process:**
1. Looked at test_base.hex - ends with `jal x0, 0`
2. Realized this is infinite loop to self
3. Confirmed with AI this is the standard convention

**Prompt to AI:** "Is `jal x0, 0` the standard way to halt a RISC-V program in simulators?"

**AI Response:**
- Yes, common convention for bare-metal programs
- Creates infinite loop at current PC
- Simulators detect this pattern as halt
- Machine code is 0x0000006F

**Implementation:**
```python
if instruction == 0x0000006F:
    print(f"Halt detected at cycle {self.cycle_count}")
    self.halted = True
    break
```

---

### test_cpu.py

#### 1. Test Program Encoding - Lines 12-20, 42-50, 70-78
**Location:** Multiple test functions, marked with `# AI Start/End`

**Challenge:** Creating test programs in machine code format.

**Tool Used:** RARS RISC-V Assembler (https://github.com/TheThirdOne/rars)

**Process:**
1. Wrote simple RISC-V assembly for each test
2. Assembled using RARS
3. Copied hex machine code output
4. Added to Python test file

**Example workflow:**
```assembly
# I wrote this in RARS:
addi x1, x0, 5
addi x2, x0, 10
add x3, x1, x2

# RARS assembled to:
00500093
00A00113
002081B3
```

**AI Help:** Asked ChatGPT for clarification on RISC-V assembly syntax when unsure.

**Prompt example:** "What's the correct RISC-V assembly syntax for a branch with offset? Is it `beq x1, x2, 8` or `beq x1, x2, label`?"

**Response:** Both work - numeric is offset in bytes, label is symbolic. For machine code generation, numeric is simpler.

---

#### 2. Memory Address Convention - Lines 59-62
**Location:** `test_memory_ops()`, marked with `# AI Start/End`

**Question:** What address should I use for testing memory operations?

**Research:**
- Noticed test_base.hex uses 0x10000
- Don't want to conflict with instructions at 0x0

**Prompt to AI:** "What's a standard address to use for data memory in RISC-V simulators? I have instructions at 0x0."

**AI Response:**
- Common convention: instructions at 0x0, data at 0x10000 (65536)
- Keeps them well separated
- Easy to identify in hex dumps
- Many RISC-V educational materials use this

**Decision:** Used 0x10000 for consistency with test_base.hex

---

#### 3. Expected Values Verification - Lines 96-112
**Location:** `test_full_program()`, marked with `# AI Start/End`

**Challenge:** Need to verify test_base.hex produces correct output.

**Process:**
1. Manually traced through test_base.hex instructions on paper
2. Ran test_base.hex in RARS simulator
3. Compared my CPU output with RARS output
4. Documented expected values

**RARS Verification:**
- Loaded test_base.hex into RARS
- Stepped through instruction-by-instruction
- Recorded final register and memory values
- Used these as expected values in test

**Expected state after execution:**
```
x1 = 5        (from: addi x1, x0, 5)
x2 = 10       (from: addi x2, x0, 10)
x3 = 15       (from: add x3, x1, x2)
x4 = 15       (from: lw x4, 0(x5))
x5 = 0x10000  (from: lui x5, 0x00010)
x6 = 2        (from: addi x6, x0, 2 after branch)
mem[0x10000] = 15 (from: sw x3, 0(x5))
```

**Why x6 = 2 not 1:** The BEQ branches forward, skipping `addi x6, x0, 1`



## References

### Primary Sources
- RISC-V Instruction Set Manual, Volume I (v20191213)
- RISC-V Green Card (Reference Card)
- RARS RISC-V Assembler documentation

### AI Tools
- ChatGPT (GPT-4) for technical questions
- Claude for explaining complex concepts

### Other Resources
- Computer Organization and Design RISC-V Edition (Patterson & Hennessy)
- GitHub RISC-V examples and test cases
- Stack Overflow for Python-specific questions



