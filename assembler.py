# uncomment these 2 lines for taking input through console
import sys                                    
code = sys.stdin.read().splitlines()

# uncomment these 2 lines if you want to read your own input file

with open('test1.txt') as f:
    code = f.read().splitlines()


# ACTUAL CODE STARTS FORM HERE  


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





registers = [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6"]
registers_flag= [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6" , "FLAGS"]
labels=["hlt"]
variables=[]
error=False

# HANDLING ALL CASES OF NORMAL INSTRUCTIONS
line_no=0                                                      
for line in code:
    line_no+=1
    if(len(line)==0):
        continue

    value = list(line.split())

    if line_no==len(code):
        handle_hlt(value)

    if(value[0]=="var"):
        continue

    if(value[0][0:-1] in labels):
        value.pop(0)

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
    
    if (operations[value[0]][1] == "A"):
        type_A(value)
            
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
    if( len(value)>1 and value[0] in labels and value[1] in operations_symbol):
        value.pop(0)

    if (value[0] in operations_symbol):

        if(value[0]=="mov" ):
            if(value[2][0]=="$"):
                value[0]="mov1"
            else:
                value[0]="mov2"

        if (operations[value[0]][1] == "B"):
            a = value[1]
            b = value[2][1:]
            b1 = bin(int(b))[2:]
            s = operations[value[0]][0] + RegAddress[a] + (8-len(b1))*"0" + b1

        elif (operations[value[0]][1] == "A"):
            a = value[1]
            b = value[2]
            c = value[3]
            s = operations[value[0]][0] + "00" + RegAddress[a] + RegAddress[b] + RegAddress[c]
    
        elif (operations[value[0]][1] == "C"):
            a = value[1]
            b = value[2]
            s = operations[value[0]][0] + "00000" + RegAddress[a] + RegAddress[b]

        elif (operations[value[0]][1] == "D"):
            a = value[1]
            b = bin(variables[value[2]])[2:]
            s = operations[value[0]][0] + RegAddress[a] + (8 - len(b)) * "0" + b

        elif (operations[value[0]][1] == "E"):
            a=value[1]
            b=bin(labels[a+":"])[2:]
            s=operations[value[0]][0] + "000" + (8 - len(b)) * "0" + b

        elif (operations[value[0]][1] == "F"):
            s = operations[value[0]][0] + "00000000000"

        print(s)


# ********************************THE END*********************************************************************