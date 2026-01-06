import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def xor_encrypt_decrypt(data: bytes, key: str) -> bytes:
    key_bytes = key.encode()
    return bytes([data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data))])

def encrypt_file(path, key):
    with open(path, "rb") as f:
        data = f.read()

    enc_path = path + ".enc"
    encrypted_data = xor_encrypt_decrypt(data, key)

    with open(enc_path, "wb") as f:
        f.write(encrypted_data)

    return enc_path

def decrypt_file(enc_path, key):
    with open(enc_path, "rb") as f:
        data = f.read()

    dec_path = enc_path.replace(".enc", ".dec")
    decrypted_data = xor_encrypt_decrypt(data, key)

    with open(dec_path, "wb") as f:
        f.write(decrypted_data)

    return dec_path


