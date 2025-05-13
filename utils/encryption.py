from cryptography.fernet import Fernet

# Generate a new 32-byte encryption key
def generate_key():
    return Fernet.generate_key()

# Create a Fernet cipher object using the provided key
def get_cipher(key: bytes):
    return Fernet(key)

# Encrypt a plaintext string and return the ciphertext as bytes
def encrypt_field(cipher, plaintext: str) -> bytes:
    return cipher.encrypt(plaintext.encode())

# Decrypt a ciphertext (bytes or memoryview) and return the original string
def decrypt_field(cipher, ciphertext: bytes) -> bytes:
    if isinstance(ciphertext, memoryview):
        ciphertext = ciphertext.tobytes()  # Convert memoryview to bytes
    
    return cipher.decrypt(ciphertext).decode()