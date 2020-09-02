# IAS implementation in python


def get_modulus(x):

    if(x>0):
        return x                               # returns modulus value of the input

    else:
        return -1*x


def decode_execute():

    global IBR
    global PC
    global IR                                  # all the registers are made global so that all of them can be accessed and modified by the function
    global MAR
    global MBR
    global AC
    global Main_Memory
    global Halt
    global IBR_flag
    global Left_instruction_flag
    #print("inside decode_execute function")
    #print(IR)
    
    
    # Data Transfer Related OpCodes
    
    
    if(IR == '00100001'):   
        MBR = AC                                # store AC in MAR memory location
        Main_Memory[MAR] = MBR
    
    elif(IR == '00000001'):                     # load m(x) into AC 
        MBR = Main_Memory[MAR]
        AC = MBR
        #print(AC)
        
    elif(IR == '00000010'):
        MBR = Main_Memory[MAR]                  # load -m(x) into AC
        AC = -1*MBR
    
    elif(IR == '00000011'):                     # load Modulus of m(x) into AC
        MBR = Main_Memory[MAR]
        AC = get_modulus(MBR)
    
    elif(IR == '00000100'):                     # load negative of modulus of m(x) into AC
        MBR = Main_Memory[MAR]
        AC = -1*get_modulus(MBR)
        
    
    # Unconditional Branch Related OpCodes
    
    
    elif(IR == '00001101'):                     # take next instruction from left half of mX
        PC = MAR
        IBR = '0'*20 
        IBR_flag = 0    
        
    elif(IR == '00001110'):                     # take next instruction from right half of mx 
        PC = MAR
        IBR = Main_Memory[PC][20:40]
        IBR_flag = 1       

        
    # Conditional Branch Related OpCodes
    
    
    elif(IR == '00001111'):                     # if ac is non-negative, take instruction from left of mx
        if(AC >= 0):
            PC = MAR
            IBR = '0'*20
            IBR_flag = 0
            
    elif(IR == '00010000'):                     # if ac is non-negative, take instruction from right of mx
        if(AC >= 0):
            PC = MAR
            IBR = Main_Memory[PC][20:40]
            IBR_flag = 1        


    #Arithmetic Related OpCodes


    elif(IR == '00000101'):
        MBR = Main_Memory[MAR]
        AC += MBR                               # Used to add the memory data at MAR to AC
        #print(AC)
        
    elif(IR == '00000111'): 
        MBR = Main_Memory[MAR]                  # Used to add the modulus of memory data at MAR to AC
        AC += get_modulus(MBR)
        #print(AC)
    
    elif(IR == '00000110'):
        MBR = Main_Memory[MAR]
        AC -= MBR
        #print(AC)                               # Used to subtract the data at memory loc. MAR from AC
    
    elif(IR == '00001000'):
        MBR = Main_Memory[MAR]
        AC -= get_modulus(MBR)                  # Used to subtract the modulus of data at memory loc. MAR from AC
    
    #Halt OpCode
    
    elif(IR == '11111000'):                     # Used to stop the program
        Halt = 1
 


Main_Memory = []
#Hardcode the main memory list...
#Before 600, all are instruction strings
#After 600, all are data

for i in range(600):
    Main_Memory.append('0');   # this is done to show that type str is going to be before 600 memory location and type int after 600 till 1000 memory location
                               
for i in range(400):
    Main_Memory.append(0);


# Program 1:

# main(void){
#     int a = 6;  
#     int b = 4;
#     int c = -3;
#     int d = 2;               # this program checks the LOAD,STORE,ADD,ADD_MODULUS(Basically all the arithmetic ones)
#     var = a;
#     var = var + b;
#     var = var + mod(c);
#     d = var;
#     printf("%d",d);
# }

Main_Memory[700] = 6
Main_Memory[701] = 4
Main_Memory[702] = -3
Main_Memory[703] = 2
Main_Memory[0] = '00000001' + '001010111100' + '00000101' + '001010111101'        # LOAD data at location 700, ADD the data at 701 to it 
Main_Memory[1] = '00000111' + '001010111110' + '00100001' + '001010111111'        # ADD MOD of data present at 702, STORE the result in 703  
Main_Memory[2] = '11111000' + '000000000000' + '11111000' + '000000000000'

# Program 1 ends...



# Program 2:

# main () {
#     int a=15, b=5, c;
#     if (a >= b)
#         c = a – b;            # this program checks COND. and UNCOND. JUMPS, SUB, ADD.
#     else
#         c = a + b;
#}

#Main_Memory[700] = 15
#Main_Memory[701] = 5            # data is feeded
#Main_Memory[702] = 0

#Main_Memory[0] = '00000001' + '001010111100' + '00000110' + '001010111101' # LOAD m(700), SUB(701)
#Main_Memory[1] = '00001111' + '000000000110' + '00001101' + '000000001000' # JUMP + m(6), Jump m(8) 
#Main_Memory[2] = '00000000' + '000000000000' + '00000000' + '000000000000' # null
#Main_Memory[3] = '00000000' + '000000000000' + '00000000' + '000000000000' # null
#Main_Memory[4] = '00000000' + '000000000000' + '00000000' + '000000000000' # null
#Main_Memory[5] = '00000000' + '000000000000' + '00000000' + '000000000000' # null
#Main_Memory[6] = '00000001' + '001010111100' + '00000110' + '001010111101' # LOAD m(700), SUB m(701)
#Main_Memory[7] = '00100001' + '001010111110' + '00001110' + '000000001010' # STOR m(702), JUMP m(10)
#Main_Memory[8] = '00000001' + '001010111100' + '00000101' + '001010111101' # LOAD m(700), ADD m(701)
#Main_Memory[9] = '00100001' + '001010111110' + '11111000' + '000000000000' # STOR m(702), program halts here
#Main_Memory[10] = '11111000' + '000000000000' + '00000000' + '000000000000'

# Program 2 ends....




# whichever program you want to test, you can uncomment the #'s related to that prog's memory block, and comment the other program's memory

PC = 0    
IBR_flag = 0
Left_instruction_flag = 1

IBR = Main_Memory[0][20:40]
MBR = '0'*40
Halt = 0

while(True):
    
    if(Halt == 1):                              # when halt is reached and is set by the decode_execute function as 1, the loop breaks...
        break    
        
    if(Main_Memory[PC]=='0'*40):
        PC+=1
        continue
        
    if(IBR_flag == 0):                          # If the next instruction not in IBR
        #fetch begin
        #print("first if")
        MAR = PC                                # PC is the memory address pointer, it's 16 bits
        MBR = Main_Memory[MAR]  
                                           
        if(len(MBR) == 40):                     # is it the time for executing left instruction
            
            IBR = MBR[20:40]
            IBR_flag = 1
            IR = MBR[0:8]
            MAR = int(MBR[9:20],2)
            #print(MAR)
            decode_execute()
            
        else:
            if(len(MBR[29:40]) == 0):
                Halt = 1
                break
            IR = MBR[21:28]
            MAR = int(MBR[29:40],2)
            #print(MBR)
            IBR_flag = 0
            PC += 1
    
    
    else:                                       # If the next instruction in IBR and needs execution
        #print("else")
        #print(IBR)
        IR = IBR[0:8]
        MAR = int(IBR[9:20],2)
        #print(MAR)
        decode_execute()
        IBR_flag = 0
        PC += 1
    
    

print(Main_Memory[703])              # for first program output  --> should be 13

#print(Main_Memory[702])               # for second program output --> should be 10

