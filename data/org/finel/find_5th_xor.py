from itertools import product

# Dictionary containing the original characters and their possible aliases
alias_mapping = {
    'i': ['1'],
    't': ['7'],
    'e': ['3'],
    'a': ['@', '4'],
    'o': ['0'],
}

# Function to convert string to bit integer
def string_to_bit_int(s):
    binary_string = ''.join(format(ord(c), '08b') for c in s)
    bit_int = int(binary_string, 2)
    return bit_int

# Function to generate all variations of a string based on the alias mapping
def generate_variations(s, index=0):
    if index >= len(s):
        return [s]
    
    char = s[index]
    variations = [char]
    
    if char in alias_mapping:
        variations += alias_mapping[char]
    
    rest_variations = generate_variations(s, index + 1)
    
    result = []
    for v in variations:
        for rest in rest_variations:
            result.append(v + rest)
    
    return result

# Function to concatenate two coordinates as a 64-bit integer
def coord_to_bin_concat(x, y):
    xint = int(x * 1000000)
    yint = int(y * 1000000)
    yint = yint << 32
    R = yint | xint
    return R

# Function to split the concatenated 64-bit integer and check the values
def split_test(R_check):
    yck = R_check >> 32
    xck = R_check & ((1 << 32) - 1)  # Use 32-bit mask for x
    print(f'yck: {yck}, xck: {xck}')
    yhex = hex(yck)[2:]
    xhex = hex(xck)[2:]
    print(f'yhex: {yhex}, xhex: {xhex}')

# Main code
x = 90.387826
y = 23.726312
R = coord_to_bin_concat(x, y)

n = 5
P = [0] * n
P[0] = "itihashe"
P[1] = "rsherara"
P[2] = "gbatchoh"
P[3] = "ornish:)"

# Generate all variations for P[0] to P[3]
variations_P0 = generate_variations(P[0])
variations_P1 = generate_variations(P[1])
variations_P2 = generate_variations(P[2])
variations_P3 = generate_variations(P[3])

# Create all combinations of variations from P[0] to P[3]
all_combinations = list(product(variations_P0, variations_P1, variations_P2, variations_P3))

# Iterate over each combination and execute the XOR logic
for combination in all_combinations:
    # Assign the current combination to P[0] to P[3]
    P[0], P[1], P[2], P[3] = combination

    # Print the current combination
    print(f'Combination: {P[0][:8]}, {P[1][:8]}, {P[2][:8]}, {P[3][:8]}')

    # Perform the XOR operations as per your logic
    for i in range(n-1):
        P[i] = string_to_bit_int(P[i][:8])  # Convert the string to bit integer
        P[n-1] = P[n-1] ^ P[i]  # XOR the values
        print(f'P_{i} = {bin(P[i])[2:].zfill(64)}')

    print(f'\nP_{n-1} = {bin(P[n-1])}')
    split_test(P[n-1])
    print()

    R_check = 0
    for i in range(n):
        R_check = R_check ^ P[i]  # XOR all the P values
    check = bin(R_check)[2:].zfill(64)
    print(f'R_check = {check}')
    split_test(R_check)
    print('-------------------\n')
