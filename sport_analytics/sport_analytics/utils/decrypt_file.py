from Crypto.Cipher import AES

def decrypt_file(file_path, key_file, iv):
    with open(file_path, 'rb') as f:
        key = open(key_file, 'rb').read()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        data = cipher.decrypt(f.read())
        return data