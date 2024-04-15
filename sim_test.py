import re
import sys

# sys.path.append('.')
RegAddress = {
  "00000":0,   #x0   zero
  "00001":0,   #x1   Return Address
  "00010":0,   #x2   Stack Pointer
  "00011":0,   #x3   Global Pointer
  "00100":0,   #x4   Thread Pointer
  "00101":0,   #x5   Temporary/alternate link register
  "00110":0,   #x6   Temporaries
  "00111":0,   #x7   Temporaries
  "01000":0,   #x8   Saved register/frame pointer
  "01000":0,   #x8   Saved Register
  "01001":2,   #x9   Saved Register
  "01010":0,   #x10  Function arguments/ return values
  "01011":0,   #x11  Function arguments/ return values
  "01100":0,   #x12  Function arguments
  "01101":0,   #x13  Function arguments
  "01110":0,   #x14  Function arguments
  "01111":0,   #x15  Function arguments
  "10000":0,   #x16  Function arguments
  "10001":0,   #x17  Function arguments
  "10010":3,   #x18
  "10011":0,   #x19
  "10100":0,   #x20
  "10101":0,   #x21
  "10110":0,   #x22
  "10111":0,   #x23
  "11000":0,   #x24
  "11001":0,   #x25
  "11010":0,   #x26
  "11011":0,   #x28
  "11100":0,   #x29
  "11101":0,   #x30
  "11110":0,   #x31
  "11111":0    #x32
}

DataMemory = {
    "0x001 0000" : 0,
    "0x001 0001" : 0,
    "0x001 0002" : 0,
    "0x001 0003" : 0,
    "0x001 0004" : 0,
    "0x001 0005" : 0,
    "0x001 0006" : 0,
    "0x001 0007" : 0,
    "0x001 0008" : 0,
    "0x001 0009" : 0,
    "0x001 000A" : 0,
    "0x001 000B" : 0,
    "0x001 000C" : 0,
    "0x001 000D" : 0,
    "0x001 000E" : 0,
    "0x001 000F" : 0,
    "0x001 0010" : 0,
    "0x001 0011" : 0,
    "0x001 0012" : 0,
    "0x001 0013" : 0,
    "0x001 0014" : 0,
    "0x001 0015" : 0,
    "0x001 0016" : 0,
    "0x001 0017" : 0,
    "0x001 0018" : 0,
    "0x001 0019" : 0,
    "0x001 001A" : 0,
    "0x001 001B" : 0,
    "0x001 001C" : 0,
    "0x001 001D" : 0,
    "0x001 001E" : 0,
    "0x001 001F" : 0,
}

# --------------------------------------------------------------
# Some helper functions

def decimalToUBinary(num):      #takes a integer and converts it to a unsigned binary string
  binary_string = format(num, '032b')
  return binary_string

def UbinToInt(binary_string):   #takes a unsigned binary number of string ins_type and converts it into int
  return int(binary_string, 2)

def sign_extend(value, bits):
    if (value & (1 << (bits - 1))) != 0:
        value = value - (1 << bits)
    return value

#---------------------------------------------------------------
PC = 0
line = "00000000010110011000100110010011" 
opcode = line[25:]
print(opcode)
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
print(ins_type)

if(ins_type=="R"):
    func3 = line[17:20]
    func7 = line[:7]
    rs2 = line[7:12]
    rs1 = line[12:17]
    rd = line[20:25]

    print(RegAddress[rd]) #testing

    if(func3 == "000"):
        if(func7 == "0000000"):    #ADD operation
            RegAddress[rd] = RegAddress[rs1] + RegAddress[rs2]

        elif(func7 == "0100000"):  #Subtract operation
            RegAddress[rd] = RegAddress[rs1] - RegAddress[rs2]   
    
    elif(func7 == "0000000" and func3 == "001"): #sll
        RegAddress[rd] = int(RegAddress[rs1]*2**(UbinToInt(decimalToUBinary(RegAddress[rs2])[27:]))) 
        
    elif(func7 == "0000000" and func3 == "101"): #srl
        RegAddress[rd] = int(RegAddress[rs1]//2**(UbinToInt(decimalToUBinary(RegAddress[rs2])[27:]))) 

    elif(func7 == "0000000" and func3 == "010"):     #slt operation
        if(RegAddress[rs2]>RegAddress[rs1]):
            RegAddress[rd] = 1

    elif(func7 == "0000000" and func3 == "011"):  #sltu operation
        if (RegAddress[rs2]<RegAddress[rs1]):
            RegAddress[rd]=1
        else:
            RegAddress[rd]=0

    elif(func3 == "100"):   #XOR
        RegAddress[rd] = (RegAddress[rs1]^RegAddress[rs2])

    elif(func3 == "110"):   #OR
        RegAddress[rd] = RegAddress[rs1] | RegAddress[rs2]
    
    elif(func3 == "111"):   #AND
        RegAddress[rd] = RegAddress[rs1] & RegAddress[rs2]

    print(RegAddress[rd]) #testing

if(ins_type == "I"):
    rd = line[20:25]
    func3 = line[17:20]
    rs1 = line[12:17]
    imm1 = line[0:12]
    
    if opcode == "0000011" and func3 == "010": #lw
        address = RegAddress[rs1] + UbinToInt(imm1)
        RegAddress[rd] = DataMemory.get(hex(address),0) #loading from memory

    elif opcode == "0010011" and func3 == "000": #adii
        RegAddress[rd] = RegAddress[rs1] + UbinToInt(imm1)
    
    elif opcode == "0010011" and func3 == "011": #sltiu
        if(RegAddress[rs1] < UbinToInt(imm1)):
            RegAddress[rd] = 1
    
    elif(opcode == "1100111"): # This is jalr (´。＿。｀)
        new_pc = (RegAddress[rs1]+UbinToInt(imm1)) & -2   #to set LSB to 0
        RegAddress[rd]=RegAddress["00001"]+4

if(ins_type == "S"):
    imm_s1 = line[20:25]
    func3 = line[17:20]
    rs1 = line[12:17]
    rs2 = line[7:12]
    imm_s2 = line[:7]
    if opcode == "0100011" and func3 == "010":  #sw
        imm = sign_extend((imm_s1+imm_s2),12)
        address = RegAddress[rs1] + imm
        RegAddress[rd] = DataMemory.get(hex(address),0)

if(ins_type == "B"):
    imm_s1 = line[20:25]  #to be fixed
    rs2 = line[15:20]     
    rs1 = line[7:12]      
    func3 = line[12:15]   
    imm_s2 = line[8:12]   
    opcode = line[0:7] 
    if opcode == "1100011":
        if func3 == "000": #beq
            if sign_extend(RegAddress[rs1]) == sign_extend(RegAddress[rs2]):
                PC = PC + sign_extend(imm[12:1]+ "0",13)
        
        if func3 == "001": #bne
            if sign_extend(RegAddress[rs1]) != sign_extend(RegAddress[rs2]):
                PC = PC + sign_extend(imm[12:1]+ "0",13)
        
        if func3 == "101": #bge
            if sign_extend(RegAddress[rs1]) >= sign_extend(RegAddress[rs2]):
                PC = PC + sign_extend(imm[12:1]+ "0",13)
        
        if func3 == "100": #blt
            if sign_extend(RegAddress[rs1]) < sign_extend(RegAddress[rs2]):
                PC = PC + sign_extend(imm[12:1]+ "10",13)

        if func3 == "110": #bltu
            if RegAddress[rs1] < RegAddress[rs2]:
                PC = PC + sign_extend(imm[12:1]+ "0",13)

        if func3 == "111": #bgeu
            if RegAddress[rs1] >= RegAddress[rs2]:
                PC = PC + sign_extend(imm[12:1]+ "0",13)

if(ins_type == "U"):
    rd = line[20:25]
    imm_u = line[:20]

if(ins_type == "J"):
    print("Need to figure out pc stuff and will add tomorrow")


