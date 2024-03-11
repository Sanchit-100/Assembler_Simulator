# Dictionaries and stuff
# -----------------------------------------------------------

import re
import sys

sys.path.append('.')
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
   "jal":["1101111","J"]
   

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


registers=["zero","ra","sp","gp","tp","t0","t1","t2","s0","fp","s1","a0","a1","a2","a3","a4","a5","a6","a7","s2","s3","s4","s5","s6" ,"s7","s8","s9","s10","s11","t3","t4","t5","t6"]
    
# --------------------------------------------------------------
# Some helper functions

def decimal_to_binary(decimal_num, size):
    # Convert decimal to binary using the built-in bin() function
    if(int(decimal_num) >= 0):
        binary_str = bin(int(decimal_num))[2:]
        binary_str = binary_str.zfill(size)

    else:
        binary_str = bin(int(decimal_num))[3:]
        bin_str = binary_str.zfill(size)

        binary_str = "".join(["1" if bit == "0" else "0" for bit in bin_str])
        carry = 1
        for i in range(len(binary_str) - 1, -1, -1):
            if carry == 1:
                if binary_str[i] == "0":
                    binary_str = binary_str[:i] + "1" + binary_str[i + 1:]
                    carry = 0
                else:
                    binary_str = binary_str[:i] + "0" + binary_str[i + 1:]

    return binary_str


#************************************************************************
def check_string(s):
    if (s.startswith('-') and s[1:].isdigit()) or s.isdigit():
        return 1;  # "The string is numeric."
    else:
        return 0;    # "The string is alphabetical."
#******************************************************************
def write_binary_to_file(text, filename):
    
    with open(filename, 'a') as file:
        # Write the binary data to the file
        file.write(text)
    
    file.close

# ------------------------------------------------------------------

with open(sys.argv[1], 'r') as file:
    # Write the binary data to the file
    code = file.read().splitlines()
    file.close()


# creating dictionary for addresses of labels
# ****************************************************************
label_dict={}
line_address=0
for line in code:
    temp_list=line.split(':')
    if(len(temp_list)==2):
        label_dict[temp_list[0]]=line_address
    line_address+=4

for i in label_dict.keys():
    print(i,"-> ", label_dict[i])

# By now, we have created a dictionary of labels 
# where the key is the name of the label and
# and the corresponding is the address
# ******************************************************************

# Main code starts from below
line_number = 0
for line in code:
    line_number +=1
    temp_list=line.split(':')
    if(len(temp_list)==2):
        line=temp_list[1]
    
    value = []
    split_list = re.split(r"\s+|,", line)
    for word in split_list:
        if(word!=""):
            value.append(word)

    # Error handling for invalid labels
    if not value:
        print("Error: Invalid definition of labels at line", line_number)
        break

    # Error handling for unsupported instructions
    if value[0] not in operations_symbol:
        print("Syntax Error at line", line_number, ": Unsupported instruction '", value[0], "'", sep="")
        break

    # Error handling for invalid register names or operands
    if len(value) > 1 and value[1] not in registers:
        print("Syntax Error at line", line_number, ": Invalid register name '", value[1], "'", sep="")
        break

    elif operations[value[0]][1] == "I":
        if len(value) < 4:
            # If the instruction is missing an immediate value
            print("Error: Missing immediate value at line", line_number)
            break
        elif value[0] == "lw":
            rd = value[1]
            imm_and_rs = value[2]
            temp = imm_and_rs.split('(')
            imm = temp[0]
            rs = temp[1].rstrip(')')
            if not (-2048 <= int(imm) <= 2047):
                # If the immediate value is out of bounds
                print("Error: Immediate value out of bounds at line", line_number)
                break
            temp_bin = decimal_to_binary(imm, 12)
            s = temp_bin + RegAddress[rs] + funct3[value[0]][0] + RegAddress[rd] + operations[value[0]][0]
        else:
            rd = value[1]
            rs1 = value[2]
            imm = value[3]
            if not (-2048 <= int(imm) <= 2047):
                # If the immediate value is out of bounds, as it is 12 bit
                print("Error: Immediate value out of bounds at line", line_number)
                break
            final_imm = decimal_to_binary(imm, 12)
            s = final_imm + RegAddress[rs1] + funct3[value[0]][0] + RegAddress[rd] + operations[value[0]][0]


# Program counter        
PC=0
for line in code:

    temp_list=line.split(':')
    if(len(temp_list)==2):
        line=temp_list[1]
    
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
            if value[0]=="lw":
                rd = value[1]
                imm_and_rs=value[2]
                temp=imm_and_rs.split('(')
                imm=temp[0]
                rs=temp[1].rstrip(')')
                
                temp_bin=decimal_to_binary(imm,12)
                
                s=temp_bin + RegAddress[rs] + funct3[value[0]][0] + RegAddress[rd]+ operations[value[0]][0]
            
            else:
                
                rd = value[1]
                rs1 = value[2]
                imm = value[3]
                final_imm=decimal_to_binary(imm,12)
                s = final_imm + RegAddress[rs1] + funct3[value[0]][0] + RegAddress[rd] + operations[value[0]][0]

        elif operations[value[0]][1] == "S":
                rd = value[1]
                imm_and_rs=value[2]
                temp=imm_and_rs.split('(')
                imm=temp[0]
                rs=temp[1].rstrip(')')
                
                temp_bin=decimal_to_binary(imm,12)
                
                s=temp_bin[0:7]+ RegAddress[rd] + RegAddress[rs] + funct3[value[0]][0] + temp_bin[7:12] + operations[value[0]][0]

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
            final_imm=decimal_to_binary(imm,32)
            s = final_imm[0:20] + RegAddress[rd] + operations[value[0]][0]
                
        elif(operations[value[0]][1] == "J"):
            comma_sep=line.split(',')
            
            rd = (comma_sep[0].split())[1]
            
            # checking if directly immediate is given
            # or a label_name is given
            
            if check_string(comma_sep[1])==0:
                label_name = comma_sep[1]
                label_value = label_dict[label_name]-PC
            
            else:
                label_value=comma_sep[1]
            
            temp_imm = str(decimal_to_binary(label_value,21))
            final_imm= temp_imm[0] + temp_imm[10:20] + temp_imm[9] + temp_imm[1:9]
            s = final_imm + RegAddress[rd] + operations[value[0]][0]
    
    
        print(s)
        # Open a file in binary write mode
        write_binary_to_file(s,sys.argv[2])
        write_binary_to_file('\n',sys.argv[2])
        PC+=4
