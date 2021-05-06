# -------------------------------
# ENCRYPTION/DECRYPTION FUNCTIONS
# -------------------------------
from cryptography.fernet import Fernet

def write_key():
    # WARNING:
    # ONLY USE IF YOU KNOW WHAT YOU ARE DOING
    # Losing the key will result in being unable to decrypt the data
    key = Fernet.generate_key()
    with open("data/keys/key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("data/keys/key.key", "rb").read()


def encrypt_pass(password):
    key = load_key()
    encoded = password.encode()
    f = Fernet(key)
    encrypted = f.encrypt(encoded)
    return encrypted

def decrypt_pass(encrypted):
    key = load_key()
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    decrypted = decrypted.decode()
    return decrypted
