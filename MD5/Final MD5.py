import math

constants = [int(abs(math.sin(i + 1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]

m_constants = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12,
                1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12,
                0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]

shift_values = [
    [7, 12, 17, 22] * 4,
    [5, 9, 14, 20] * 4,
    [4, 11, 16, 23] * 4,
    [6, 10, 15, 21] * 4,
]
#
rotate_by_ = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
             5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
             4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
             6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

rotate_by_index = 0
m_index = 0
const_val = 0

def round_function(B, C, D, cnt):
    if cnt == 1:
        value = (B & C) | ((~B) & (D))
    elif cnt == 2:
        value = (B & D) | (C & (~D))
    elif cnt == 3:
        value = B ^ C ^ D
    elif cnt == 4:
        value = C ^ (B | (~D))
    return value & 0xFFFFFFFF

def rotate_by(value,rotate):
    return int((value[rotate::]+value[0:rotate]),2)
def operation_calculation(cnt):
    global A, B, C, D, m_index, const_val, rotate_by_index
    for i in range(0, 16):
        function_value = round_function(B, C, D, cnt)
        round_value = (A + function_value) & 0xFFFFFFFF
        round_value = (round_value + (data[m_constants[m_index]])) & 0xFFFFFFFF
        round_value = (round_value + constants[const_val % 64]) & 0xFFFFFFFF
        round_value = rotate_by(bin(round_value)[2::],shift_values[cnt-1][i])
        round_value = (round_value + B) & 0xFFFFFFFF
        const_val += 1
        m_index += 1
        rotate_by_index +=1
        A, B, C, D = D, round_value, B, C
        print(f"A: {hex(A)}, B: {hex(B)}, C: {hex(C)}, D: {hex(D)}")
    print(f"Round {cnt}: A: {hex(A)}, B: {hex(B)}, C: {hex(C)}, D: {hex(D)}")

def round_calculation(A, B, C, D, cnt):
    print(f"\nRound {cnt}: ")
    operation_calculation(cnt)

def MD5():
    global A, B, C, D, cnt
    A = int("67452301", 16)
    B = int("efcdab89", 16)
    C = int("98badcfe", 16)
    D = int("10325476", 16)
    # A = int("01234567",16)
    # B = int("89abcdef",16)
    # C = int("fedcba98",16)
    # D = int("76543210",16)
    cnt = 1
    round_calculation(A, B, C, D, cnt)
    cnt += 1
    round_calculation(A, B, C, D, cnt)
    cnt += 1
    round_calculation(A, B, C, D, cnt)
    cnt += 1
    round_calculation(A, B, C, D, cnt)

def padding(data):
    main_data = []
    main_length = len(data)
    if main_length >=960:
        block_value = data[0:512]
        main_data.append(block_value)
        block_value = data[512:960]

        length = abs(960 - main_length)
        if length > 64:
            block_value += data[960:960 + 64]
            main_data.append(block_value)
            block_value = data[1024:]
            length = abs(main_length - 1024)
            block_value += ('1' + (447 - length) * "0" + bin(main_length)[2:].rjust(64, '0'))
            main_data.append(block_value)
            return main_data       
        else:
            block_value += data[960:960 + length]
            block_value += ('1' + (63 - length) * "0")
            main_data.append(block_value)
            block_value = ((448 - length) * "0" + bin(main_length)[2:].rjust(64, '0'))
            main_data.append(block_value)
            return main_data
    elif main_length >= 448:
        block_value = data[0:448]
        length = abs(448 - main_length)
        if length > 64:
            block_value += data[448:448 + 64]
            main_data.append(block_value)
            block_value = data[512:]
            length = main_length - 512
            block_value += ('1' + (447 - length) * "0" + bin(main_length)[2:].rjust(64, '0'))
            main_data.append(block_value)
            return main_data
        else:
            block_value += data[448:448 + length]
            block_value += ('1' + (63 - length) * "0")
            main_data.append(block_value)
            block_value = ((448 - length) * "0" + bin(main_length)[2:].rjust(64, '0'))
            main_data.append(block_value)
            return main_data
    elif main_length < 448:
        block_value = data[0:main_length]
        block_value += ('1' + (447 - main_length) * "0" + bin(main_length)[2:].rjust(64, '0'))
        main_data.append(block_value)
        return main_data

# data = bin(int("Kathiresh".encode().hex(), 16))[2:]
data = bin(int(input('Enter the Message: ').encode().hex(), 16))[2:]
# print("Using 448 Bit Message")
# main_448 = "0101001101101000101010010100010101010001010100101010011011010001010100101000101010100010101001010100110110100010101001010001010101000101010010101001101101000101010010100010101010001010100101010011011010001010100101000101010100010101001010100110110100010101001010001010101000101010010101001101101000101010010100010101010001010100101010011011010001010100101000101010100010101001010100110110100010101001010001010101000101010010101001101101000101000000"
main_448 = "1000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010100000101000001010000010"
# print(f"Message: {main_448}")
# print("Using 960 Bit Message")
# main_960="010100110110100010101001010001010101000101010010101001101101000101010010100010101010001010100101010011011010001010100101000101010100010101001010100110110100010101001010001010101000101010010101001101101000101010010100010101010001010100101010011011010001010100101000101010100010101001010100110110100010101001010001010101000101010010101001101101000101010010100010101010001010100101010011011010001010100101000101010100010101001010100110110100010100000001010011011010001010100101000101010100010101001010100110110100010101001010001010101000101010010101001101101000101010010100010101010001010100101010011011010001010100101000101010100010101001010100110110100010101001010001010101000101010010101001101101000101010010100010101010001010100101010011011010001010100101000101010100010101001010100110110100010101001010001010101000101010010101001101101000101010010100010101010001010100101010011011010001010000001000000000011111111111111110000000000000000000000000000000000000"
# print(f"Message: {main_960}")

# main_data = padding(data)
main_data = padding(main_448)
# main_data = padding(main_960)
# main_data = padding(data)


print(f"\nNumber of blocks: {len(main_data)}\n\n")
print("Blocks: ",main_data,"\n\n")
for i in range(len(main_data)):
    print(f"Block {i+1}")
    data = [int(main_data[i][j:j + 32], 2) for j in range(0, 512, 32)]
    MD5()
    print("\n\n")
    m_index = 0
    const_val = 0

# A = (A + int("01234567",16)) & 0xFFFFFFFF    
# B = (B + int("89abcdef",16)) & 0xFFFFFFFF    
# C = (C + int("fedcba98",16)) & 0xFFFFFFFF    
# D = (D + int("76543210",16)) & 0xFFFFFFFF    

A = (A + int("67452301",16)) & 0xFFFFFFFF    
B = (B + int("efcdab89",16)) & 0xFFFFFFFF    
C = (C + int("98badcfe",16)) & 0xFFFFFFFF    
D = (D + int("10325476",16)) & 0xFFFFFFFF    

# A = int("674523025476", 


print(f"\nFinal Hash Value: {hex(A)}{hex(B)}{hex(C)}{hex(D)}")
