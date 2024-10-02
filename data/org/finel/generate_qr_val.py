import random


k = 16  # Precision: 10 binary digits after decimal point
def float_to_binary(x, k):
    # Handle negative numbers
    if x < 0:
        return '-' + float_to_binary(-x, k)

    # Separate the number into integer and fractional parts
    integer_part = int(x)
    fractional_part = x - integer_part

    # Convert integer part to binary
    binary_integer = bin(integer_part)[2:].zfill(8)

    # Convert fractional part to binary with k precision digits
    binary_fractional = []
    while fractional_part > 0 and len(binary_fractional) < k:
        fractional_part *= 2
        bit = int(fractional_part)
        binary_fractional.append(str(bit))
        fractional_part -= bit

    # Combine both parts
    binary_result = binary_integer + ''.join(binary_fractional)

    return binary_result


def string_to_bit_int(s):
    # Convert each character to its ASCII value and then to an 8-bit binary string
    binary_string = ''.join(format(ord(c), '08b') for c in s)
    
    # Convert the resulting binary string to an integer
    bit_int = int(binary_string, 2)
    
    return bit_int

# Example usage
y = 23.726312
x = 90.387826

biny = bin(int(y*1000000))[2:].zfill(32)
binx = bin(int(x*1000000))[2:].zfill(32)
print (biny, binx)

def coord_to_bin_concat (x, y):
    xint = int(x * 1000000)
    yint = int(y * 1000000)
    yint = yint << 32
    R = yint | xint
    return R


def split_test (R_check):
    yck = R_check >> 32
    xck = R_check & ((1<<32)-1)
    print(yck, xck) 
    yhex = hex(yck)[2:]
    xhex = hex(xck)[2:]
    # print (int(bin(R_check), 2))
    print(yhex, xhex) 

# R = int (binary_representation, 2)
R = coord_to_bin_concat (x, y)
n = 5
P = [0] * n
P[n-1] = R

for i in range(n-1):
    P[i] = string_to_bit_int(input())
    P[n-1] = P[n-1] ^ P[i]
    print (f'P_{i} = {bin(P[i])[2:].zfill(64)}')

print()
print (f'P_{n-1} = {bin(P[n-i])}')
split_test(P[n-i])
print()

R_check = 0
for i in range(n):
    R_check = R_check ^ P[i]
check = bin(R_check)[2:].zfill(64)
print (f'R_check = {check}')
split_test (R_check)




