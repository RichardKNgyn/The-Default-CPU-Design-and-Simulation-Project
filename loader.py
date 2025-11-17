def load_hex_file(filename, memory, start_address=0x0):
    """
    Load a .hex file into memory
    
    Format: One 32-bit instruction per line, 8 hex digits
    Example:
        00500093
        00A00113
        002081B3
    
    Args:
        filename: Path to .hex file
        memory: Memory object to load into
        start_address: Starting address for program (default 0x0)
    
    Returns:
        Number of instructions loaded
    """
    instruction_count = 0
    current_address = start_address
    
    try:
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                # Remove whitespace
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse hex value
                try:
                    # Should be exactly 8 hex digits
                    instruction = int(line, 16)
                    
                    # Verify it's a 32-bit value
                    if instruction > 0xFFFFFFFF:
                        print(f"Warning: Line {line_num} has value > 32 bits, truncating")
                        instruction = instruction & 0xFFFFFFFF
                    
                    # Store in memory
                    memory.write_word(current_address, instruction)
                    
                    instruction_count += 1
                    current_address += 4  # Move to next word
                    
                except ValueError:
                    print(f"Error: Line {line_num} contains invalid hex: '{line}'")
                    continue
        
        print(f"Loaded {instruction_count} instructions from {filename}")
        return instruction_count
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return 0
    except Exception as e:
        print(f"Error loading file: {e}")
        return 0


def create_test_hex_file(filename="test_simple.hex"):
    """
    Create a simple test hex file for testing the loader
    """
    test_program = [
        "00500093",  # addi x1, x0, 5
        "00A00113",  # addi x2, x0, 10
        "002081B3",  # add x3, x1, x2
    ]
    
    with open(filename, 'w') as f:
        for instruction in test_program:
            f.write(instruction + '\n')
    
    print(f"Created test file: {filename}")


# Test
if __name__ == "__main__":
    from memory import Memory
    
    print("Testing hex loader...")
    
    # Create a test file
    create_test_hex_file()
    
    # Load it into memory
    mem = Memory()
    count = load_hex_file("test_simple.hex", mem, start_address=0x0)
    
    print(f"\nLoaded {count} instructions")
    
    # Verify the load
    print("\nVerifying loaded instructions:")
    print(f"0x00000000: 0x{mem.read_word(0x0):08X} (expected 0x00500093)")
    print(f"0x00000004: 0x{mem.read_word(0x4):08X} (expected 0x00A00113)")
    print(f"0x00000008: 0x{mem.read_word(0x8):08X} (expected 0x002081B3)")
    
    print("\nLoader test complete!")