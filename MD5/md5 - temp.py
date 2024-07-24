import math

rotate_by = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
             5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
             4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
             6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

constants = [int(abs(math.sin(i+1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]


init_MDBuffer = [0x01234567, 0x89abcdef, 0x89abcdef, 0x76543210]

# A = int("01234567",16)
#     B = int("89abcdef",16)
#     C = int("89abcdef",16)
#     D = int("76543210",16)

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

    try1 = init_MDBuffer[:]

    for round_num in range(4):
        print(f"\nRound {round_num + 1} - Initial Values: {init_temp}")

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
                to_rotate = A + F + constants[i] + int.from_bytes(block[4*G: 4*G + 4], byteorder='little')
                new_B = (B + leftRotate(to_rotate, rotate_by[i])) & 0xFFFFFFFF
                A, B, C, D = D, new_B, B, C

            for i, val in enumerate([A, B, C, D]):
                init_temp[i] += val
                init_temp[i] &= 0xFFFFFFFF
                try1[i] =  md_to_hex(init_temp[i])
                try1[i] = try1[i][:8]


        print(f"Intermediate Values after Round {round_num + 1}: {init_temp}")
        print(f"Intermediate Hexa-decimal Values after Round {round_num + 1}: {try1}")

    return sum(buffer_content << (32*i) for i, buffer_content in enumerate(init_temp))

def md_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

def md5(msg):
    msg = bytearray(msg, 'ascii')
    msg = pad(msg)
    processed_msg = process_message(msg)
    message_hash = md_to_hex(processed_msg)
    print("\nFinal Hash: ", message_hash)

if __name__ == '__main__':
    message = input("Enter the message: ")
    md5(message)
