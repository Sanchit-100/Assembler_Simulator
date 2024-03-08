# Dictionaries and stuff
# -----------------------------------------------------------

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
                    "and","addi","lw","sltiu","jalr","beq","bne","bge",
                    "bgeu","blt","bltu","auipc","lui","jal","mul","rst",
                    "halt","rvrs"]



# creating the dictionary for ABI names
# Here key is the ABI and corresponding value
# is the register name like x_

ABI_names={
    "zero":"x0",
    "ra" : "x1",
    "sp":"x2",
    "gp" : "x3",
    "tp":"x4",
    "t0" : "x5",
    "t1":"x6",
    "t2" : "x7",
    "s0":"x8",
    "fp" : "x8",
    "s1":"x9",
    "a0" : "x10",
    "a1":"x11",
    "a2" : "x12",
    "a3":"x13",
    "a4" : "x14",
    "a5":"x15",
    "a6" : "x16",
    "a7":"x17",
    "s2" : "x18",
    "s3":"x19",
    "s4" : "x20",
    "s5":"x21",
    "s6" : "x22",
    "s7":"x23",
    "s8" : "x24",
    "s9":"x25",
    "s10" : "x26",
    "s11":"x27",
    "t3" : "x28",
    "t4":"x29",
    "t5" : "30",
    "t6":"x31"

}
registers = []

for i in range(32):
    registers.append("x"+str(i))
    
# --------------------------------------------------------------
# Some helper functions

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

# ------------------------------------------------------------------

with open('sample_test.txt', 'r') as file:
    # Write the binary data to the file
    code = file.read().splitlines()


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
            s = funct7[value[0]][0] + RegAddress[ABI_names[rs2]] + RegAddress[ABI_names[rs1]] + funct3[value[0]][0] + RegAddress[ABI_names[rd]] + operations[value[0]][0]

        elif (operations[value[0]][1] == "I"):
            rd = value[1]
            rs1 = value[2]
            imm = value[3]
            s = decimal_to_binary(imm) + RegAddress[ABI_names[rs1]] + funct3[value[0]][0] + RegAddress[ABI_names[rd]] + operations[value[0]][0]

        elif(operations[value[0]][1] == "U"):
            rd = value[1]
            imm = value[2]
            s = decimal_to_binary(imm) + RegAddress[ABI_names[rd]] + operations[value[0]][0]
        
        elif(operations[value[0]][1] == "J"):
            comma_sep=line.split(',')
            
            rd = (comma_sep[0].split())[1]
            label_name = comma_sep[1]
            label_value = label_dict[label_name]-PC
            
            temp_imm = decimal_to_binary(label_value)
            final_imm= temp_imm[20] + temp_imm[10:1] + temp_imm[11] + temp_imm[19:12]
            s = final_imm + RegAddress[ABI_names[rd]] + "0010111"
        
        elif operations[value[0]][1] == "S":
            rd = value[1]
            imm_and_rs=value[2]
            temp=imm_and_rs.split('(')
            imm=temp[0]
            rs=temp[1].rstrip(')')
            
            temp_bin=decimal_to_binary(imm)
            
            s=imm[11:5]+ RegAddress[ABI_names[rd]] + RegAddress[ABI_names[rs]] + funct3[value[0]][0] + imm[4:0] + operations[value[0]][0]
        
    
    
        print(s)
        # Open a file in binary write mode
        write_binary_to_file(s,"stdout.txt")
        PC+=4
