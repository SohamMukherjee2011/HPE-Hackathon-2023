# encryption and decryption file
# enrcryption and decryption done using AES encryption with fernet

from cryptography.fernet import Fernet

# encrypts password and returns encrypted password along with its key
def encrypt(message): 
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    return [key, encMessage]

# decrypts given password with provided key and returns decrypted password
def decrypt(key, message):
    fernet = Fernet(key)
    decMessage = fernet.decrypt(message)
    decMessage = str(decMessage)
    decMessage = decMessage.replace('b', '')
    decMessage = decMessage.replace("'", '')
    return str(decMessage)
