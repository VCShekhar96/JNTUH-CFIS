import socket
import numpy as np

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

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

def matrix_mod_inverse(matrix, modulus):
    n = matrix.shape[0]
    det = int(np.round(np.linalg.det(matrix))) % modulus
    det_inv = mod_inverse(det, modulus)
    if det_inv is None:
        raise ValueError("Key matrix is not invertible modulo 26!")
        
    if n == 2:
        adj = np.array([[matrix[1,1], -matrix[0,1]], [-matrix[1,0], matrix[0,0]]])
    else:
        adj = np.zeros((3, 3), dtype=int)
        for i in range(3):
            for j in range(3):
                submatrix = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                sub_det = int(np.round(np.linalg.det(submatrix)))
                cofactor = ((-1)**(i + j)) * sub_det
                adj[j, i] = cofactor % modulus
                
    return (det_inv * adj) % modulus

def hill_decrypt(ciphertext, key_str):
    key_processed, n = process_key(key_str)
    key_matrix = np.array([ord(c) - ord('A') for c in key_processed]).reshape(n, n)
    
    nums = [ord(c) - ord('A') for c in ciphertext.upper() if c.isalpha()]
    inv_matrix = matrix_mod_inverse(key_matrix, 26)
    
    plain_nums = []
    for i in range(0, len(nums), n):
        vector = np.array([[nums[i+j]] for j in range(n)])
        result = np.dot(inv_matrix, vector) % 26
        plain_nums.extend(int(np.round(n_val)) % 26 for n_val in result.flatten())
    return "".join([chr(n_val + ord('A')) for n_val in plain_nums])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5001))
server.listen(1)

print("server waiting for connection...")
client, address = server.accept()
print("client connected: ", address)

data = client.recv(1024).decode()
print("Received cipher: ", data)

key_str = input("Enter secret key: ").strip()
plaintext = hill_decrypt(data, key_str)
print("Decrypted message : ", plaintext)

client.close()
server.close()

# Output:
# server waiting for connection...
# client connected:  ('127.0.0.1', 62149)
# Received cipher:  SCCXNX
# Enter secret key: govindh
# Decrypted message :  CAESAR
