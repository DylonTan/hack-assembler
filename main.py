import sys

# C-Instruction 

compute_instructions = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",

    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

destinations = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jumps = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

symbol_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10, 
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15 
}

variable_pointer = 16
root_file = sys.argv[1]

def filter_instruction(instruction):
    if len(instruction) < 1:
        return ''
    current = instruction[0]
    if current == '\n' or current == '/':
        return ''
    elif current == ' ':
        return filter_instruction(instruction[1:])
    else:
        return current + filter_instruction(instruction[1:])

def auto_complete_instruction(instruction):
    # instruction = instruction[:-1]
    if not '=' in instruction:
        instruction = "null=" + instruction
    if not ";" in instruction:
        instruction = instruction + ";null"
    return instruction

def map_variable_to_table(variable):
    global variable_pointer
    symbol_table[variable] = variable_pointer
    variable_pointer += 1
    return symbol_table[variable]

def parse_a_instruction(instruction):
    if instruction[1].isalpha():
        label = instruction[1:]
        a_value = symbol_table.get(label, -1)
        if a_value == -1:
            a_value = map_variable_to_table(label)
    else:
        a_value = int(instruction[1:])
    b_value = bin(a_value)[2:].zfill(16)
    return b_value

def parse_c_instruction(instruction):
    instruction = auto_complete_instruction(instruction)
    print(instruction)
    temp = instruction.split('=')
    destination = destinations.get(temp[0], "UNDEFINED")
    temp = temp[1].split(';')
    compute_instruction = compute_instructions.get(temp[0], "UNDEFINED")
    jump = jumps.get(temp[1], "UNDEFINED")
    return compute_instruction, destination, jump

def filter_label(instruction, current_line):
    if instruction != '':
        if instruction[0] == '(':
            label = instruction[1:-1]
            map_label_to_table(label, current_line)
            return ''
        else:
            return instruction

def map_label_to_table(label, current_line):
    symbol_table[label] = current_line
    return symbol_table[label]

def parse(instruction):
    if instruction[0] == '@':
        return parse_a_instruction(instruction)
    else:
        temp = parse_c_instruction(instruction)
        return "111" + temp[0] + temp[1] + temp[2]

def assemble():
    input_file = open(root_file + '.asm')
    output_file = open(root_file + '.hack', 'w')

    current_line = 0
    for instruction in input_file:
        filtered_instruction = filter_instruction(instruction)
        filtered_instruction_and_label = filter_label(filtered_instruction, current_line)
        if filtered_instruction_and_label != '':
            current_line += 1
            parsed_line = parse(filtered_instruction_and_label)
            output_file.write(parsed_line + '\n')

    input_file.close()
    output_file.close()

assemble()
# print(filter_instruction('@2'))