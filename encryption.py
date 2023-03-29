from cryptography.fernet import Fernet
 
def encrypt(message): 
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    return [key, encMessage]

def decrypt(key, message):
    fernet = Fernet(key)
    decMessage = fernet.decrypt(message)
    decMessage = str(decMessage)
    decMessage = decMessage.replace('b', '')
    decMessage = decMessage.replace("'", '')
    return str(decMessage)
