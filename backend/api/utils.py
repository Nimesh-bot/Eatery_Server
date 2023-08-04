from cryptography.fernet import Fernet

def encrypt_message(message, key):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message

def write_to_encrypted_file(file_path, content, key):
    encrypted_content = encrypt_message(content, key)
    try:
        with open(file_path, 'a') as file:
            file.write(str(encrypted_content) + '\n')
        print("Successfully wrote encrypted data to the file:", file_path)
    except IOError as e:
        print("An error occurred while writing to the file:", str(e))

def read_from_encrypted_file(file_path, key):
    try:
        with open(file_path, 'rb') as file:
            encrypted_content = file.read()
            decrypted_content = decrypt_message(encrypted_content, key)
            return decrypted_content
    except IOError as e:
        print("An error occurred while reading from the file:", str(e))
        return None
