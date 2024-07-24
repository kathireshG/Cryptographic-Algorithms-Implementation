import math

rotate_by = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
             5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
             4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
             6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

# A = 01 23 45 67

# B = 89 ab cd ef

# C = fe dc ba 98

# D = 76 54 32 10

# Round 1: (b AND c) OR ((NOT b) AND (d))

# Round 2: (b AND d) OR (c AND (NOT d))

# Round 3: b XOR c XOR d

# Round 4: c XOR (b OR (NOT d))

# def split_hex_into_blocks(hex_input):
#     # Convert hexadecimal to binary
#     binary_input = bin(int(hex_input, 16))[2:].zfill(len(hex_input) * 4)

#     # Split the binary input into 32-bit blocks
#     blocks = [binary_input[i:i+32] for i in range(0, len(binary_input), 32)]

#     # Convert each block back to hexadecimal
#     hex_blocks = [hex(int(block, 2))[2:].zfill(8) for block in blocks]

#     return hex_blocks

constants = [int(abs(math.sin(i+1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]

init_MDBuffer = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

def leftRotate(x, amount):
    x &= 0xFFFFFFFF
    return (x << amount | x >> (32-amount)) & 0xFFFFFFFF

def pad(msg):
    msg_len_in_bits = (8 * len(msg)) & 0xffffffffffffffff
    msg.append(0x80)

    while len(msg) % 64 != 56:
        msg.append(0)

    msg += msg_len_in_bits.to_bytes(8, byteorder='little')
    return msg

def process_message(msg):
    init_temp = init_MDBuffer[:]

    for offset in range(0, len(msg), 64):
        A, B, C, D = init_temp
        block = msg[offset: offset+64]

        for i in range(64):
            if i < 16:
                func = lambda b, c, d: (b & c) | (~b & d)
                index_func = lambda i: i
            elif 16 <= i < 32:
                func = lambda b, c, d: (d & b) | (~d & c)
                index_func = lambda i: (5*i + 1) % 16
            elif 32 <= i < 48:
                func = lambda b, c, d: b ^ c ^ d
                index_func = lambda i: (3*i + 5) % 16
            elif 48 <= i < 64:
                func = lambda b, c, d: c ^ (b | ~d)
                index_func = lambda i: (7*i) % 16

            F = func(B, C, D)
            G = index_func(i)
            # print(G)
            to_rotate = A + F + constants[i] + int.from_bytes(block[4*G: 4*G + 4], byteorder='little')
            new_B = (B + leftRotate(to_rotate, rotate_by[i])) & 0xFFFFFFFF
            A, B, C, D = D, new_B, B, C

        for i, val in enumerate([A, B, C, D]):
            init_temp[i] += val
            init_temp[i] &= 0xFFFFFFFF

    return sum(buffer_content << (32*i) for i, buffer_content in enumerate(init_temp))

def md_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

def md5(msg):
    msg = bytearray(msg, 'ascii')
    msg = pad(msg)
    processed_msg = process_message(msg)
    message_hash = md_to_hex(processed_msg)
    print("Message Hash: ", message_hash)

if __name__ == '__main__':
    message = input("Enter the message: ")
    md5(message)
