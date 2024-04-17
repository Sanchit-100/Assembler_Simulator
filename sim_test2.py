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
    0x001_0001 : 0,
    0x001_0002 : 0,
    0x001_0003 : 0,
    0x001_0004 : 0,
    0x001_0005 : 0,
    0x001_0006 : 0,
    0x001_0007 : 0,
    0x001_0008 : 0,
    0x001_0009 : 0,
    0x001_000A : 0,
    0x001_000B : 0,
    0x001_000C : 0,
    0x001_000D : 0,
    0x001_000E : 0,
    0x001_000F : 0,
    0x001_0010 : 0,
    0x001_0011 : 0,
    0x001_0012 : 0,
    0x001_0013 : 0,
    0x001_0014 : 0,
    0x001_0015 : 0,
    0x001_0016 : 0,
    0x001_0017 : 0,
    0x001_0018 : 0,
    0x001_0019 : 0,
    0x001_001A : 0,
    0x001_001B : 0,
    0x001_001C : 0,
    0x001_001D : 0,
    0x001_001E : 0,
    0x001_001F : 0,
}

# --------------------------------------------------------------
# Some helper functions

def decimalToUBinary(num):      #takes a integer and converts it to a unsigned binary string
    if(num>=0):
        binary_string = format(num, '032b')
        return binary_string
    else:
        binary_string = format(num, '032b')



def UbinToInt(binary_string):   #takes a unsigned binary number of string ins_type and converts it into int
  return int(binary_string, 2)

def binary_2complement(binary_str):
    if binary_str[0] == "1":
        inverted_bits = "".join("1" if bit == "0" else "0" for bit in binary_str)
        twos_complement = int(inverted_bits, 2) + 1
        return -twos_complement

    else:
        return int(binary_str, 2)

def bin_2Complement(num):
    # Convert the number to binary and keep the last 32 bits
    binary = '0b'+format(num & 0xFFFFFFFF, '032b')
    return binary
#---------------------------------------------------------------
list1 = ["00000000000000000000010010110011",
"00000000000000000000100100110011",
"00000000000100000000010010010011",
"00000001000000000000100100010011",
"00000001001001001001010010110011",
"00000000101100000000101010010011",
"00000001010101001010000000100011",
"00000000000001001010100100000011",
"00000000010001001000010010010011",
"00000000000100000000100110010011",
"00000001001110010111100100110011",
"00000001001000000000100001100011",
"00000000001100000000101000010011",
"00000001010001001010000000100011",
"00000000000000000000000001100011",
"00000000001000000000101000010011",
"00000001010001001010000000100011",
"00000000000000000000000001100011"]

# list1 = ["00000000100101000010000000100011","00000000000000000000000001100011"]

# f=open("input.txt","r")
# list1=f.readlines()
# f.close()
# g=open("output.txt","w")

pc = 0
temp1 = len(list1)-1


while(pc<temp1*4):
    line = list1[int(pc/4)]  # accessing the line


# line = "00000000010110011000100110010011"
    

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
                RegAddress[rd] = 1
                pc = pc + 4

        elif(func3 == "011"):  #sltu operation  
            if(UbinToInt(decimalToUBinary(RegAddress[rs2])) > UbinToInt(decimalToUBinary(RegAddress[rs1]))):
                RegAddress[rd] = 1
                pc = pc + 4
                           

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
            RegAddress[rd] = DataMemory[RegAddress[rs1] + binary_2complement(imm1)]
            pc = pc + 4

        elif(func3 == "000"): #adii
            RegAddress[rd] = RegAddress[rs1] + UbinToInt(imm1)
            pc = pc + 4
    
        elif(func3 == ""): #sltiu
            if(RegAddress[rs1] < UbinToInt(imm1)):
                RegAddress[rd] = 1
                pc = pc + 4
    
        elif(opcode == "1100111"): #jalr 
            RegAddress[rd] = pc + 4
            pc = RegAddress[rs1] + bin_2Complement(imm1)

    if(ins_type == "S"):
        imm_s1 = line[20:25]
        func3 = line[17:20]
        rs1 = line[12:17]
        rs2 = line[7:12]
        imm_s2 = line[:7]
        imm_s = imm_s2 + imm_s1
        DataMemory[RegAddress[rs1] + binary_2complement(imm_s)] = RegAddress[rs2]
        pc = pc + 4

    if(ins_type == "B"):
        imm_b = line[0] + line[24] + line[1:7] + line[20:24]+'0'
        func3 = line[17:20]
        rs1 = line[12:17]
        rs2 = line[7:12]

        if(func3 == "000"): #Beq
            if(RegAddress[rs1] == RegAddress[rs2]):    
                pc = pc + binary_2complement(imm_b)
            else:
                pc = pc + 4
        
        if(func3 == "001"):  #Bne
            if(RegAddress[rs1] != RegAddressp[rs2]):
                pc = pc + binary_2complement(imm_b)
            else:
                pc = pc + 4

        if(func3 == "100"):  #Blt
            if(RegAddress[rs1] < RegAddressp[rs2]):
                pc = pc + binary_2complement(imm_b)
            else:
                pc = pc + 4

        if(func3 == "101"):  #Bge
            if(RegAddress[rs1] >= RegAddressp[rs2]):
                pc = pc + binary_2complement(imm_b)
            else:
                pc = pc + 4 

        if(func3 == "110"):  #Bltu
            if(decimalToUBinary(UbinToInt(RegAddress[rs1])) < decimalToUBinary(UbinToInt(RegAddressp[rs2]))):
                pc = pc + binary_2complement(imm_b)
            else:
                pc = pc + 4

        if(func3 == "111"):  #Bgeu
            if(decimalToUBinary(UbinToInt(RegAddress[rs1])) >= decimalToUBinary(UbinToInt(RegAddressp[rs2]))):
                pc = pc + binary_2complement(imm_b)  
            else:
                pc = pc + 4

    
    if(ins_type == "U"):
        rd = line[20:25]
        imm_u = line[:20]

        if(opcode == "0110111"):  #lui
            RegAddress[rd] = binary_2complement(imm_u + "000000000000")
            pc = pc + 4

        if(opcode == "0010111"):  #auipc
            RegAddress[rd] = pc + binary_2complement(imm_u + "000000000000")
            pc = pc + 4

    if(ins_type == "J"):
        rd = line[20:25]
        imm_j = line[0] + line[12:20] + line[11]+ line[1:11]+ "0"
        RegAddress[rd] = pc + 4
        temporary = pc + binary_2complement(imm_j)
        if(temporary%2==0):
            pc = temporary
        else:
            pc = temporary-1
    

    print(bin_2Complement(pc), end = " ")
    for i in range(32):
        print(bin_2Complement(RegAddress[decimalToUBinary(i)[27:]]), end = " ")
    print("\n")

    if line=="00000000000000000000000001100011":  #Virtual Halt
        break
    
    # for i in range(32):
    #     g.write(bin(RegAddress[decimalToUBinary(i)[27:]]))  
    #     g.write("\n")   

    # g.close()
