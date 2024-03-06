RegAddress = {
  "x0":"00000",
  "x1":"00100",
  "x2":"01000"
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

operations_symbol = ["add","sub","xor","slt","sltu","sll","srl","or",
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

code=["add x0, x1, x2","sub x0, x1, x2","addi x0, x1, 12"]
for line in code:

    if(len(line)==0):
        continue

    result = line.split()
    value=[word.rstrip(',') for word in result]

    if (value[0] in operations_symbol):

        if (operations[value[0]][1] == "R"):
            r1 = value[1]
            r2 = value[2]
            r3 = value[3]
            s = funct7[value[0]][0] + RegAddress[r3] + RegAddress[r2] + funct3[value[0]][0] + RegAddress[r1] + operations[value[0]][0]

        elif (operations[value[0]][1] == "I"):
            r1 = value[1]
            r2 = value[2]
            imm = value[3]
            s = decimal_to_binary(imm) + RegAddress[r2] + funct3[value[0]][0] + RegAddress[r1] + operations[value[0]][0]
    
        

        print(s)
        # Open a file in binary write mode
        write_binary_to_file(s,"stdout.txt")
