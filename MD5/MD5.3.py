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

def operation_calculation(A, B, C, D, data, cnt, m_index, const_val):
    for i in range(0, 16):
        function_value = round_function(B, C, D, cnt)
        round_value = (A + function_value) & 0xFFFFFFFF
        round_value = (round_value + data[m_constants[m_index]]) & 0xFFFFFFFF
        round_value = (round_value + constants[const_val % 64]) & 0xFFFFFFFF
        round_value = (round_value << shift_values[cnt-1][i]) | (round_value >> (32 - shift_values[cnt-1][i])) & 0xFFFFFFFF
        round_value = (round_value + B) & 0xFFFFFFFF
        const_val += 1
        m_index += 1
        A, B, C, D = D, round_value, B, C
    return A, B, C, D, const_val, m_index

def round_calculation(A, B, C, D, cnt, data, const_val, m_index):
    print(f"\nRound {cnt}: ")
    A, B, C, D, const_val, m_index = operation_calculation(A, B, C, D, data, cnt, m_index, const_val)
    print(f"A: {hex(A)}, B: {hex(B)}, C: {hex(C)}, D: {hex(D)}")
    return A, B, C, D, const_val, m_index

def MD5(data):
    A = int("01234567", 16)
    B = int("89abcdef", 16)
    C = int("fedcba98", 16)
    D = int("76543210", 16)
    cnt = 1
    const_val = 0
    m_index = 0

    A, B, C, D, const_val, m_index = round_calculation(A, B, C, D, cnt, data, const_val, m_index)
    cnt += 1
    A, B, C, D, const_val, m_index = round_calculation(A, B, C, D, cnt, data, const_val, m_index)
    cnt += 1
    A, B, C, D, const_val, m_index = round_calculation(A, B, C, D, cnt, data, const_val, m_index)
    cnt += 1
    A, B, C, D, const_val, m_index = round_calculation(A, B, C, D, cnt, data, const_val, m_index)
    
    # Combine A, B, C, D to get the final result
    final_result = hex(A)[2:] + hex(B)[2:] + hex(C)[2:] + hex(D)[2:]
    return final_result

def padding(data):
    main_data = []
    main_length = len(data)
    
    if main_length >= 448:
        block_value = data[0:448]
        length = 448 - main_length
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

# Example usage:
data = bin(int("Aravindan".encode().hex(), 16))[2:]
main_data = padding(data)

# MD5(main_data[0])
data_hex = hex(int(main_data[0], 2))[2:]
data = [int(data_hex[i:i + 8], 16) for i in range(0, 128, 8)]
result = MD5(data)
print("\nFinal MD5 Result:", result)