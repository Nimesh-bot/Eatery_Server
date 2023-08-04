from cryptography.fernet import Fernet

FERNET_KEY = b'q-jEpb08S-XdYKk-v49iFwKn0lOXFIUe4ID4qyv4fek='

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    encrypted_message = encrypted_message[2:-2]
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message

def read_from_encrypted_file(file_path, key):
    try:
        with open(file_path, 'r') as file:
            for encrypted_line in file:
                # encrypted_line_str = encrypted_line.
                decrypted_line = decrypt_message(encrypted_line, key)
                print(decrypted_line)
    except IOError as e:
        print("An error occurred while reading from the file:", str(e))
        return None


read_from_encrypted_file('log/AnonymousUser.log', FERNET_KEY)
