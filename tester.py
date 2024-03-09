import re
RegAddress = {
  "zero":"00000", #x0
  "ra":"00001",   #x1
  "sp":"00010",   #x2
  "gp":"00011",   #x3
  "tp":"00100",   #x4
  "t0":"00101",   #x5
  "t1":"00110",   #x6
  "t2":"00111",   #x7
  "fp":"01000",   #x8
  "s0":"01000",   #x8
  "s1":"01001",   #x9
  "a0":"01010",   #x10
  "a1":"01011",   #x11
  "a2":"01100",   #x12
  "a3":"01101",   #x13
  "a4":"01110",   #x14
  "a5":"01111",   #x15
  "a6":"10000",   #x16
  "a7":"10001",   #x17
  "s2":"10010",   #x18
  "s3":"10011",   #x19
  "s4":"10100",   #x20
  "s5":"10101",   #x21
  "s6":"10110",   #x22
  "s7":"10111",   #x23
  "s8":"11000",   #x24
  "s9":"11001",   #x25
  "s10":"11010",  #x26
  "s11":"11011",  #x28
  "t3":"11100",   #x29
  "t4":"11101",   #x30
  "t5":"11110",   #x31
  "t6":"11111"    #x32
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
   "jal":["0010111","J"],

   # Bonus type I instruction
   "halt":["0000000","H"],
   # Bonus type II instruction
   "rst":["0000001","RS"],
   # Bonus Type III instruction
   "mul":["0000010","M"],
   # Bonus type IV instruction
   "rvrs":["0000011","RV"]
   
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
                    "and","addi","lw","sltiu","jalr","beq","bne","bge",
                    "bgeu","blt","bltu","auipc","lui","jal","mul","rst",
                    "halt","rvrs"]





registers = []

for i in range(32):
    registers.append("x"+str(i))
    
error=False
line_number=0


def decimal_to_binary(decimal_num, size):
    # Convert decimal to binary using the built-in bin() function
    if(int(decimal_num) >= 0):
        binary_str = bin(int(decimal_num))[2:]
        padded_binary_str = binary_str.zfill(size)

    else:
        binary_str = bin(int(decimal_num))[3:]
        padded_binary_str = "1" + binary_str.zfill(size-1)

    return padded_binary_str

#************************************************************************
def write_binary_to_file(text, filename):

    #open file in binary write mode
    with open(filename, 'a') as file:
        # Write the binary data in the 
        file.write(text)
    
    file.close

code=["auipe 00000 -20",
      "sub t1,s0,a0",
      "sll a1,t2,t3",
      "slt s1,a2,s2",
      "sltu s3,a3,s4",
      "xor s5,a4,s6",
      "srl s7,a5,s8",
      "or s9,a6,s10",
      "and s11,a7,s0",
      "beq zero,zero,0"]


for line in code:

    line_number+=1
    value = []
    split_list = re.split(r"\s+|,", line)
    for word in split_list:
        if(word!=""):
            value.append(word)

    #ERROR HANDLING FOR UNSUPPORTED INSTRUCTIONS
    if (value[0] not in operations_symbol):
      print(f"Syntax Error at line {line_number}: Unsupported instruction '{value[0]}'")
      error=True
      break
    #ERROR HANDLING FOR TYPOS IN INSTRUCTION OR REGISTER NAME
    elif len(value)>1 and value[1] not in registers:
      print(f"Syntax Error at line {line_number}: Invalid register name '{value[1]}'")
      error=True
      break

    #ERROR HANDLING FOR INVALID DEFINITION OF LABELS
    elif len(value)==0:
        print(f"Syntax Error at line {line_number}: Invalid definition of labels")
        error=True
        break

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
            s = decimal_to_binary(imm,12) + RegAddress[rs1] + funct3[value[0]][0] + RegAddress[rd] + operations[value[0]][0]

        elif (operations[value[0]][1] == "S"):
            rs1 = value[1]
            imm = value[2]
            rs2 = value[3]
            imm1 = decimal_to_binary(imm,12)[:7]
            imm2 = decimal_to_binary(imm,12)[7:]
            s = imm1 + RegAddress[rs2] + RegAddress[rs1] + "010" + imm2 + "0100011"

        elif (operations[value[0]][1] == "B"):
            rs1 = value[1]
            rs2 = value[2]
            imm = value[3]
            imm1 = decimal_to_binary(imm,13)[0] + decimal_to_binary(imm,13)[2:8]
            imm2 = decimal_to_binary(imm,13)[8:12] + decimal_to_binary(imm,13)[1]
            s = imm1 + RegAddress[rs2] + RegAddress[rs1] + funct3[value[0]][0] + imm2 + "1100011"

        elif(operations[value[0]][1] == "U"):
            rd = value[1]
            imm = value[2]
            s = decimal_to_binary(imm,32) + RegAddress[rd] + operations[value[0]][0]
        
        elif(operations[value[0]][1] == "J"):
            rd = value[1]
            imm = value[2]
            s = decimal_to_binary(imm,21) + RegAddress[rd] + "1101111"

        elif(operations[value[0]][1] == "H"):
            s = "0000000000000000000000000" + operations[value[0]][0]

        elif(operations[value[0]][1] == "RS"):
            s = "0000000000000000000000000" + operations[value[0]][0]
        
        elif(operations[value[0]][1] == "M"):
            rd = value[1]
            rs1 = value[2]
            rs2 = value[3]
            s = "0000000" + RegAddress[rs2] + RegAddress[rs1] + "000" + RegAddress[rd] + operations[value[0]][0]
        
        elif(operations[value[0]][1] == "RV"):
            rd = value[1]
            rs = value[2]
            s = "0000000" + "00000" + RegAddress[rs] + "000" + RegAddress[rd] + operations[value[0]][0]
    
        

        print(s)
        # Open a file in binary write mode
        # write_binary_to_file(s,"stdout.txt")        
