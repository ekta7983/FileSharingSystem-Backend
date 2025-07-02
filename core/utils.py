from cryptography.fernet import Fernet
from django.conf import settings

# Generate this once and use in .env
FERNET_KEY = settings.FERNET_KEY
fernet = Fernet(FERNET_KEY.encode())

def encrypt_id(user_id):
    return fernet.encrypt(str(user_id).encode()).decode()

def decrypt_id(token):
    return int(fernet.decrypt(token.encode()).decode())
