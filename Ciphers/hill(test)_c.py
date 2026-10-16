import socket
import numpy as np

def process_key(key_str):
    key_str = "".join([c.upper() for c in key_str if c.isalpha()])
    if len(key_str) >= 9:
        key_str = key_str[:9]
        n = 3
    elif len(key_str) == 4:
        n = 2
    elif len(key_str) < 4:
        while len(key_str) < 4:
            key_str += 'X'
        n = 2
    else:  # Between 5 and 8 characters
        while len(key_str) < 9:
            key_str += 'X'
        n = 3
    return key_str, n

def hill_encrypt(text, key_str):
    key_processed, n = process_key(key_str)
    key_matrix = np.array([ord(c) - ord('A') for c in key_processed]).reshape(n, n)
    
    nums = [ord(c) - ord('A') for c in text.upper() if c.isalpha()]
    while len(nums) % n != 0:
        nums.append(23) # Padding 'X'
        
    cipher_nums = []
    for i in range(0, len(nums), n):
        vector = np.array([[nums[i+j]] for j in range(n)])
        result = np.dot(key_matrix, vector) % 26
        cipher_nums.extend(result.flatten())
    return "".join([chr(num + ord('A')) for num in cipher_nums])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5001))

text = input("Enter plaintext: ")
key_str = input("Enter secret key: ").strip()

ciphertext = hill_encrypt(text, key_str)
print("Encrypted:", ciphertext)

client.send(ciphertext.encode())
client.close()

# Output:
# Enter plaintext: caesar
# Enter secret key: govindh 
# Encrypted: SCCXNX
