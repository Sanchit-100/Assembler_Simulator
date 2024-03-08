import re
RegAddress = {
  "x0":"00000",
  "x1":"00001",
  "x2":"00010",
  "x3":"00011",
  "x4":"00100",
  "x5":"00101",
  "x6":"00110",
  "x7":"00111",
  "x8":"01000",
  "x9":"01001",
  "x10":"01010",
  "x11":"01011",
  "x12":"01100",
  "x13":"01101",
  "x14":"01110",
  "x15":"01111",
  "x16":"10000",
  "x17":"10001",
  "x18":"10010",
  "x19":"10011",
  "x20":"10100",
  "x21":"10101",
  "x22":"10110",
  "x23":"10111",
  "x24":"11000",
  "x25":"11001",
  "x26":"11010",
  "x27":"11011",
  "x28":"11100",
  "x29":"11101",
  "x30":"11110",
  "x31":"11111"
}


operations = {
    # R type instructions
   "add":["0110011","R"],
   "sub":["0110011","R"],
   "sll":["0110011","R"],
   "slt":["0110011","R"],
   "sltu":["0110011","R"],
   "xor":["0110011","R"],
   "srl":["0110011","R"],
   "or":["0110011","R"],
   "and":["0110011","R"],
   
   # I type instructions
   "lw":["0000011","I"],
   "addi":["0010011","I"],
   "sltiu":["0010011","I"],
   "jalr":["1100111","I"],
   
   # S type instructions
   "sw":["0100011","S"],
   
   # B type instructions
   "beq":["1100011","B"],
   "bne":["1100011","B"],
   "blt":["1100011","B"],
   "bge":["1100011","B"],
   "bltu":["1100011","B"],
   "bgeu":["1100011","B"],
   
   # U type instructions
   "lui":["0110111","U"],
   "auipc":["0010111","U"],
   
   # J type instructions
   "jal":["0010111","J"]
   
}

funct7={
    # R type instructions
   "add":["0000000","R"],
   "sub":["0100000","R"],
   "sll":["0000000","R"],
   "slt":["0000000","R"],
   "sltu":["0000000","R"],
   "xor":["0000000","R"],
   "srl":["0000000","R"],
   "or":["0000000","R"],
   "and":["0000000","R"],
}

funct3={
    # R type instructions
   "add":["000","R"],
   "sub":["000","R"],
   "sll":["001","R"],
   "slt":["010","R"],
   "sltu":["011","R"],
   "xor":["100","R"],
   "srl":["101","R"],
   "or":["110","R"],
   "and":["111","R"],
   
   # I type instructions
   "lw":["010","I"],
   "addi":["000","I"],
   "sltiu":["011","I"],
   "jalr":["000","I"],
   
   #S type instructions
   "sw":["010","S"],
   
   # B type instructions
   "beq":["000","B"],
   "bne":["001","B"],
   "blt":["100","B"],
   "bge":["101","B"],
   "bltu":["110","B"],
   "bgeu":["111","B"],
}

operations_symbol = ["add","sub","xor","slt","sltu","sll","srl","or","sw",
                    "and","addi","sltiu","jalr","beq","bne","bge",
                    "bgeu","blt","bltu","auipc","lui","jal","mul","rst",
                    "halt","rvrs"]





registers = []

for i in range(32):
    registers.append("x"+str(i))
    
error=False


def decimal_to_binary(decimal_num):
    # Convert decimal to binary using the built-in bin() function
    binary_str = bin(int(decimal_num))[2:]  # Remove the '0b' prefix

    # Pad with leading zeros to ensure a 12-bit representation
    padded_binary_str = binary_str.zfill(12)

    return padded_binary_str

#************************************************************************
def write_binary_to_file(text, filename):
    
    with open(filename, 'a') as file:
        # Write the binary data to the file
        file.write(text)
    
    file.close

code=["add x0,x1,x2","sub x0,x1,x2","addi x0,x1,12"]
for line in code:

    value = []
    split_list = re.split(r"\s+|,", line)
    for word in split_list:
        if(word!=""):
            value.append(word)

    if (value[0] in operations_symbol):

        if (operations[value[0]][1] == "R"):
            rd = value[1]
            rs1 = value[2]
            rs2 = value[3]
            s = funct7[value[0]][0] + RegAddress[rs2] + RegAddress[rs1] + funct3[value[0]][0] + RegAddress[rd] + operations[value[0]][0]

        elif (operations[value[0]][1] == "I"):
            rd = value[1]
            rs1 = value[2]
            imm = value[3]
            s = decimal_to_binary(imm) + RegAddress[rs1] + funct3[value[0]][0] + RegAddress[rd] + operations[value[0]][0]
            
        elif (operations[value[0]][1] == "S"):
            r1 = value[1]
            r2 = value[2]
            imm = value[3]
            imm_b = str(decimal_to_binary(imm))
            s = imm_b[:7] + RegAddress[r1] + RegAddress[r2] + funct3[value[0]][0] + imm_b[7:] + operations[value[0]][0]
    
        elif (operations[value[0]][1] == "B"):
            rs1 = value[1]
            rs2 = value[2]
            label = value[3]
            label_b = str(decimal_to_binary(label))
            s = label_b[:7] + RegAddress[rs2] + RegAddress[rs1] + funct3[value[0]][0] + label_b[7:] + operations[value[0]][0]

        elif(operations[value[0]][1] == "U"):
            rd = value[1]
            imm = value[2]
            s = decimal_to_binary(imm) + RegAddress[rd] + operations[value[0]][0]
        
        elif(operations[value[0]][1] == "J"):
            rd = value[1]
            imm = value[2]
            s = decimal_to_binary(imm) + RegAddress[rd] + "0010111"
    
        

        print(s)
        # Open a file in binary write mode
        write_binary_to_file(s,"stdout.txt")
