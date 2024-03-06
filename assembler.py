# uncomment these 2 lines for taking input through console
import sys                                    
code = sys.stdin.read().splitlines()

# uncomment these 2 lines if you want to read your own input file

with open('test1.txt') as f:
    code = f.read().splitlines()


# ACTUAL CODE STARTS FORM HERE  

# Store here the binary values of each register
RegAddress = {
  "R0":"000",
  "R1":"001",
  "R2":"010",
  "R3":"011",
  "R4":"100",
  "R5":"101",
  "R6":"110",
  "FLAGS":"111"
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

#**************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE R *******************************************#
def type_R(value):
    global error
    if(len(value)!=4):
        print("line no" , line_no , " wrong syntax used for", value[0],"instruction",sep=' ' )
        error=True
        return

    for i in range(1,len(value)):

        if(value[i] not in registers):
            print("line no" , line_no ,'(',value[i],')', "is invalid register name ",sep=' ')
            error=True
            
#****************************************************************************
def decimal_to_binary(decimal_num):
    # Convert decimal to binary using the built-in bin() function
    binary_str = bin(decimal_num)[2:]  # Remove the '0b' prefix

    # Pad with leading zeros to ensure a 12-bit representation
    padded_binary_str = binary_str.zfill(12)

    return padded_binary_str

#************************************************************************
def write_binary_to_file(binary_value, filename):
    # Convert the binary string to bytes
    binary_bytes = int(binary_value, 2)

    # Open the file in binary write mode
    with open(filename, 'wb') as file:
        # Write the binary data to the file
        file.write(binary_bytes)
        

#****************************************************************************

# HANDLING ALL CASES OF NORMAL INSTRUCTIONS
line_no=0                                                      
for line in code:
    line_no+=1
    if(len(line)==0):
        continue


    result = line.split()
    value=[word.rstrip(',') for word in result]
    # value contains the list for all the elements of an instruction



    if(len(value)==0):
        print("line no", line_no , "invalid defnation of labels",sep=' ')
        error=True
        continue
    
    if(value[0] not in operations_symbol):
        print("line no",line_no , '(',value[0],')'," is invalid instruction name ", sep=' ')
        error=True
        continue

    if(value[0]=="mov" and len(value)>=2):
        c = value[2][0]
        if(65<=ord(c)<=90 or 97<=ord(c)<=122):
            value[0]="mov2"
        else:
            value[0]="mov1"
    
    if (operations[value[0]][1] == "R"):
        type_R(value)
            
    elif (operations[value[0]][1] == "C"):
        type_C(value)
        
    elif (operations[value[0]][1] == "B"):
        type_B(value)

    elif (operations[value[0]][1] == "D"):
        type_D(value)
    
    elif (operations[value[0]][1] == "E"):
        type_E(value)

    elif (operations[value[0]][1] == "F"):
        type_F(value)

    else:
        print("line no",line_no,"invalid syntax",sep=' ')
        error=True



#********************************************************************************************************************************************
# THIS IS ASSEMBLER THIS WILL RUN ONLY WHEN THERE ARE NO ERRORS IN THE ASSEMBLY CODE 

labels={}
variables={}

t=1
address=-1

if(error==True):
    exit()


#*********************************THIS LOOP WILL STORE THE ADDRESS OF ALL VARIABLES IN DICTIONARY*******************
for line in code:
    if len(line)==0:
        continue
    value = list(line.split())
    
    if(value[0] in operations_symbol):
        address+=1

    if value[0]=="hlt":
        labels[value[0]+":"]=address

    if(value[0][-1]==":"):
        address+=1
        labels[value[0]]=address
        

#********************************* THIS LOOP WILL STORE THE ADDRESS OF ALL LABELS IN DICTIONARY ********************
for line in code:
    if(len(line)==0):
        continue
    value = list(line.split())
    if value[0]=="var" and len(value)==2:
        variables[value[1]]=t+address
        t+=1


#********************************* THIS IS MAIN LOOP TO COVERT ASSEMBLY INTO BINARY CODE *******************************
for line in code:

    if(len(line)==0):
        continue

    value = list(line.split())

    if (value[0] in operations_symbol):

        if (operations[value[0]][1] == "R"):
            r1 = value[1]
            r2 = value[2]
            r3 = value[3]
            s = operations[value[0]][0] + RegAddress[r1] + RegAddress[r2] + RegAddress[r3]

        elif (operations[value[0]][1] == "I"):
            r1 = value[1]
            r2 = value[2]
            imm = value[3]
            s = operations[value[0]][0] + RegAddress[r1] + RegAddress[r2] + decimal_to_binary(imm)

        print(s)
        # Open a file in binary write mode
        write_binary_to_file(s,"stdout.bin")

# The file is automatically closed after the 'with' block



# ********************************THE END*********************************************************************