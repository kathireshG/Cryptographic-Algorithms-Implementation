import math

constants = [int(abs(math.sin(i+1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]
m_constants = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12,
                1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12,
                0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]
m_index = 0
const_val = 0

# Round 1: (b AND c) OR ((NOT b) AND (d))

# Round 2: (b AND d) OR (c AND (NOT d))

# Round 3: b XOR c XOR d

# Round 4: c XOR (b OR (NOT d))

def round_function(B,C,D):
    if(cnt == 1):
        value = (B & C) | ((~ B) & (D))
    elif(cnt == 2):
        value = (B & D) | (C & (~ D))
    elif(cnt == 3):
        value = B ^ C ^ D
    elif(cnt == 4):
        value = C ^ (B | (~ D))
    return value & 0xFFFFFFFF 
def operation_calculation():
    global A,B,C,D, m_index, const_val
    for i in range(0,16):
        function_value = round_function(B,C,D)
        print("function_value" , function_value)
        round_value = A|function_value
        print("round_value", round_value)
        round_value = (round_value+data[m_constants[m_index]]) & 0xFFFFFFFF
        m_index+=1
        round_value = (round_value + constants[const_val])  & 0xFFFFFFFF
        const_val +=1
        round_value = (round_value << 2) + B
        A=D
        D=C
        C=B
        B=round_value

def round_calculation(A,B,C,D):
    global cnt, final
    print(f"\nRound {cnt}: ")
    operation_calculation()
    final += str(hex(A)[2::])+str(hex(B)[2::])+str(hex(C)[2::])+str(hex(D)[2::])
    print(final)
    cnt+=1

def MD5():
    global A,B,C,D, cnt, final
    final = ""
    A = int("01234567",16)
    B = int("89abcdef",16)
    C = int("fedcba98",16)
    D = int("76543210",16)
    cnt  = 1
    round_calculation(A,B,C,D)
    round_calculation(A,B,C,D)
    round_calculation(A,B,C,D)
    round_calculation(A,B,C,D)

def padding(data):
    main_data = []
    main_length = len(data)
    length = len(data)
    if(length >=448):
        block_value = data[0:448]
        length = 448-length
        if(length > 64):
            block_value += data[448:448+64]
            main_data.append(block_value)
            block_value = data[512::]
            length = len(data) - 512
            block_value += ('1' + (447-length)*"0" + bin(main_length)[2::].rjust(64,'0'))
            main_data.append(block_value)
            return main_data
        else:
            block_value += data[448:448+length]
            block_value += ('1' + (63-length)*"0")
            main_data.append(block_value)
            block_value = ((448-length)*"0" + bin(main_length)[2::].rjust(64,'0'))
            main_data.append(block_value)
            return main_data
    elif(length < 448):
        block_value = data[0:length]
        block_value += ('1' + (447-length)*"0" + bin(main_length)[2::].rjust(64,'0'))
        main_data.append(block_value)
        return main_data
    

# data= bin(int(input().encode().hex(),16))[2::]
data= bin(int("Aravindan".encode().hex(),16))[2::]
main_data = padding(data)

# MD5(main_data[0])
data = hex(int(main_data[0],2))[2::]
data = [int(data[i:i+8],16) for i in range(0,128,8)]
print("length: ",len(data))
print(data)
MD5()
print(final)
# print(bin(int(data,16)))

# print(f"{data}"+"\n\n")
# MD5()
# print(f"Hash Value: {final}")

