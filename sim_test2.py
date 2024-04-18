import re
import sys

# sys.path.append('.')
RegAddress = {
  "00000":0,   #x0   zero
  "00001":0,   #x1   ra   Return Address
  "00010":256, #x2   sp   Stack Pointer =  ( 256  )
  "00011":0,   #x3   gp   Global Pointer
  "00100":0,   #x4   tp   Thread Pointer
  "00101":0,   #x5   t0   Temporary/alternate link register
  "00110":0,   #x6   t1   Temporaries
  "00111":0,   #x7   t2   Temporaries
  "01000":0,   #x8   s0   Saved register/frame pointer
  "01001":0,   #x8   s1   Saved Register
  "01010":0,   #x9   a0   Saved Register
  "01011":0,   #x10  a1   Function arguments/ return values
  "01100":0,   #x11  a2   Function arguments/ return values
  "01101":0,   #x12  a3   Function arguments
  "01110":0,   #x13  a4   Function arguments
  "01111":0,   #x14  a5   Function arguments
  "10000":0,   #x15  a6   Function arguments
  "10001":0,   #x16  a7   Function arguments
  "10010":0,   #x18  s2   
  "10011":0,   #x19  s3
  "10100":0,   #x20  s4
  "10101":0,   #x21  s5
  "10110":0,   #x22  s6
  "10111":0,   #x23  s7
  "11000":0,   #x24  s8
  "11001":0,   #x25  s9
  "11010":0,   #x26  s10
  "11011":0,   #x28  s11
  "11100":0,   #x29  t3
  "11101":0,   #x30  t4
  "11110":0,   #x31  t5
  "11111":0    #x32  t6
}

DataMemory = {
    0x001_0000 : 0,
    0x001_0004 : 0,
    0x001_0008 : 0,
    0x001_000c : 0,
    0x001_0010 : 0,
    0x001_0014 : 0,
    0x001_0018 : 0,
    0x001_001c : 0,
    0x001_0020 : 0,
    0x001_0024 : 0,
    0x001_0028 : 0,
    0x001_002c : 0,
    0x001_0030 : 0,
    0x001_0034 : 0,
    0x001_0038 : 0,
    0x001_003c : 0,
    0x001_0040 : 0,
    0x001_0044 : 0,
    0x001_0048 : 0,
    0x001_004c : 0,
    0x001_0050 : 0,
    0x001_0054 : 0,
    0x001_0058 : 0,
    0x001_005c : 0,
    0x001_0060 : 0,
    0x001_0064 : 0,
    0x001_0068 : 0,
    0x001_006c : 0,
    0x001_0070 : 0,
    0x001_0074 : 0,
    0x001_0078 : 0,
    0x001_007c : 0,
}

# --------------------------------------------------------------
# Some helper functions

def decimalToUBinary(num):      #takes a integer and converts it to a unsigned binary string
    if(num>=0):
        binary_string = format(num, '032b')
        return binary_string
    else:
        binary_string = format(num, '032b')
        
def custom_bin_convert(num):      
    if(num>=0):
        binary_string = format(num, '032b')
    else:
        binary_string = format(2**32 + num, '032b')
    return binary_string

# ************************************************
# Function for two's compement conversion to integer
def bin_to_int(bin_str):
    if bin_str[0] == '1':
        return -1 * (int(''.join('1' if x == '0' else '0' for x in bin_str), 2) + 1)
    else:
        return int(bin_str, 2)
# *************************************************

def sign_extend(binary_str, bits):
    if len(binary_str) >= bits:
        return binary_str
    else:
        sign = binary_str[0]
        while len(binary_str) < bits:
            binary_str = sign + binary_str
        return binary_str


def UbinToInt(binary_string):   #takes a unsigned binary number of string ins_type and converts it into int
  return int(binary_string, 2)

# def bin_to_int(binary_str):
#     if binary_str[0] == "1":
#         inverted_bits = "".join("1" if bit == "0" else "0" for bit in binary_str)
#         twos_complement = int(inverted_bits, 2) + 1
#         return twos_complement*(-1)

#     else:
#         return int(binary_str, 2)

def bin_2Complement(num):
    # Convert the number to binary and keep the last 32 bits
    binary = '0b'+format(num & 0xFFFFFFFF, '032b')
    return binary

def write_binary_to_file(text, filename):
    
    with open(filename, 'a') as file:
        # Write the binary data to the file
        file.write(text)
    
    file.close

def print_data_memory(data_memory):

    for address, value in data_memory.items():
        s=f"{address:#010x}:{bin_2Complement(value)}"
        # print(s)
        write_binary_to_file(s,"output.txt")
        write_binary_to_file('\n',"output.txt")

with open("sample.txt", 'r') as file:
    # Write the binary data to the file
    list1 = file.read().splitlines()
    file.close()

#---------------------------------------------------------------
# list1 = ["00000000000000000000010010110011",
# "00000000000000000000100100110011",
# "00000000000100000000010010010011",
# "00000001000000000000100100010011",
# "00000001001001001001010010110011",
# "00000000101100000000101010010011",
# "00000001010101001010000000100011",
# "00000000000001001010100100000011",
# "00000000010001001000010010010011",
# "00000000000100000000100110010011",
# "00000001001110010111100100110011",
# "00000001001000000000100001100011",
# "00000000001100000000101000010011",
# "00000001010001001010000000100011",
# "00000000000000000000000001100011",
# "00000000001000000000101000010011",
# "00000001010001001010000000100011",
# "00000000000000000000000001100011"]

# list1 = ["00000000100101000010000000100011","00000000000000000000000001100011"]

# f=open("input.txt","r")
# list1=f.readlines()
# f.close()
# g=open("output.txt","w")

pc = 0
temp1 = len(list1)-1


while(pc<=temp1*4):
    line = list1[int(pc/4)]  # accessing the line
    
    opcode = line[25:]
    ins_type = ""
    if(opcode=="0110011"):
        ins_type = "R"
    elif(opcode == "0000011" or opcode == "0010011" or opcode == "1100111"):
        ins_type = "I"
    elif(opcode == "0100011"):
        ins_type = "S"
    elif(opcode == "1100011"):
        ins_type = "B"
    elif(opcode == "0110111" or opcode == "0010111"):
        ins_type = "U"
    elif(opcode == "1101111"):
        ins_type = "J"

    if(ins_type=="R"):
        func3 = line[17:20]
        func7 = line[:7]
        rs2 = line[7:12]
        rs1 = line[12:17]
        rd = line[20:25]

    # print(RegAddress[rd]) #testing

        if(func3 == "000"):
            if(func7 == "0000000"):    #ADD operation
                RegAddress[rd] = (RegAddress[rs1] + RegAddress[rs2])
                pc = pc + 4

            elif(func7 == "0100000"):  #Subtract operation
                RegAddress[rd] = RegAddress[rs1] - RegAddress[rs2]
                pc = pc + 4   
    
        elif(func3 == "001"): #error
            # RegAddress[rd] = int((RegAddress[rs1])*2**(UbinToInt(decimalToUBinary(RegAddress[rs2])[27:])))  #sll operation clearing required
            RegAddress[rd] = RegAddress[rs1]<<(RegAddress[rs2] & 0b11111)
            pc = pc + 4
        
        elif(func3 == "010"):     #slt operation
            if(RegAddress[rs2]>RegAddress[rs1]):
                # print(RegAddress[rs2])
                # print(RegAddress[rs1])
                RegAddress[rd] = 1
            
            pc = pc + 4
            pc=pc & ~1 
                

        elif(func3 == "011"):  #sltu operation  
            if(UbinToInt(decimalToUBinary(RegAddress[rs2])) > UbinToInt(decimalToUBinary(RegAddress[rs1]))):
                RegAddress[rd] = 1
                
            pc = pc + 4
            pc=pc & ~1
                           

        elif(func3 == "100"):   #XOR
            RegAddress[rd] = (RegAddress[rs1]^RegAddress[rs2])
            pc = pc + 4

        elif(func3 == "101"):   #SRL  error
            # RegAddress[rd] = int(RegAddress[rs1]/2**(UbinToInt(decimalToUBinary(RegAddress[rs2])[27:])))
            RegAddress[rd] = RegAddress[rs1]>>(RegAddress[rs2] & 0b11111)
            pc = pc + 4

        elif(func3 == "110"):   #OR
            RegAddress[rd] = RegAddress[rs1] | RegAddress[rs2]
            pc = pc + 4
    
        elif(func3 == "111"):   #AND
            RegAddress[rd] = RegAddress[rs1] & RegAddress[rs2]
            pc = pc + 4

        # print(RegAddress[rd]) #testing

    if(ins_type == "I"):
        rd = line[20:25]
        func3 = line[17:20]
        rs1 = line[12:17]
        imm1 = line[0:12]
    
        if(func3 == "010"): #lw
            RegAddress[rd] = DataMemory[RegAddress[rs1] + bin_to_int(imm1)]
            pc = pc + 4

        elif(func3 == "000"): #adii
            RegAddress[rd] = RegAddress[rs1] + bin_to_int(imm1)
            pc = pc + 4
            pc = pc & ~1
            # print(RegAddress[rd])
            
    
        elif(func3 == "011"): #sltiu
            if(RegAddress[rs1] < UbinToInt(imm1)):
                RegAddress[rd] = 1
            
            pc = pc + 4
    
        if(opcode == "1100111"): #jalr 
            RegAddress[rd] = pc + 4
            pc = RegAddress[rs1] + UbinToInt(imm1)
            # print("hello")
            pc = pc & ~1
            # print(pc)

    if(ins_type == "S"):
        imm_s1 = line[20:25]
        func3 = line[17:20]
        rs1 = line[12:17]
        rs2 = line[7:12]
        imm_s2 = line[:7]
        imm_s = imm_s2 + imm_s1
        DataMemory[RegAddress[rs1] + bin_to_int(imm_s)] = RegAddress[rs2]
        pc = pc + 4

    if(ins_type == "B"):
        imm_b = line[0] + line[24] + line[1:7] + line[20:24]+'0'
        func3 = line[17:20]
        rs1 = line[12:17]
        rs2 = line[7:12]

        if(func3 == "000"): #Beq
            if(RegAddress[rs1] == RegAddress[rs2]):    
                pc = pc + bin_to_int(imm_b)
            else:
                pc = pc + 4
        
        if(func3 == "001"):  #Bne
            if(RegAddress[rs1] != RegAddress[rs2]):
                pc = pc + bin_to_int(imm_b)
            else:
                pc = pc + 4

        if(func3 == "100"):  #Blt
            if(RegAddress[rs1] < RegAddress[rs2]):
                pc = pc + bin_to_int(imm_b)
            else:
                pc = pc + 4

        if(func3 == "101"):  #Bge
            if(RegAddress[rs1] >= RegAddress[rs2]):
                pc = pc + bin_to_int(imm_b)
            else:
                pc = pc + 4 

        if(func3 == "110"):  #Bltu
            if(decimalToUBinary(UbinToInt(RegAddress[rs1])) < decimalToUBinary(UbinToInt(RegAddress[rs2]))):
                pc = pc + bin_to_int(imm_b)
            else:
                pc = pc + 4

        if(func3 == "111"):  #Bgeu
            if(decimalToUBinary(UbinToInt(RegAddress[rs1])) >= decimalToUBinary(UbinToInt(RegAddress[rs2]))):
                pc = pc + bin_to_int(imm_b)  
            else:
                pc = pc + 4

    
    if(ins_type == "U"):
        rd = line[20:25]
        imm_u = line[:20]

        if(opcode == "0110111"):  #lui
            RegAddress[rd] = bin_to_int(imm_u + "000000000000")
            pc = pc + 4

        if(opcode == "0010111"):  #auipc
            RegAddress[rd] = pc + bin_to_int(imm_u + "000000000000")
            pc = pc + 4

    if(ins_type == "J"):
        rd = line[20:25]
        imm_j = line[0] + line[12:20] + line[11]+ line[1:11]+ "0"
        RegAddress[rd] = pc + 4
        pc = pc + UbinToInt(imm_j)
        pc = pc & ~1
    
    # 00000001100000000000000011101111

    # print(bin_2Complement(pc), end = " ")
    RegAddress["00000"]=0
    RegAddress["00011"]=0
    RegAddress["00100"]=0
    
    write_binary_to_file(bin_2Complement(pc),"output.txt")
    write_binary_to_file(" ","output.txt")
    
    for i in range(32):
        text=bin_2Complement(RegAddress[decimalToUBinary(i)[27:]])
        write_binary_to_file(text,"output.txt")
        write_binary_to_file(" ","output.txt")
        # print(text, end = " ")
        
    # print("\n")
    write_binary_to_file('\n',"output.txt")

    RegAddress["00000"]=0
    if line=="00000000000000000000000001100011":  #Virtual Halt
        break

print_data_memory(DataMemory)
    # for i in range(32):
    #     g.write(bin(RegAddress[decimalToUBinary(i)[27:]]))  
    #     g.write("\n")   

    # g.close()