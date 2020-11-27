from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
import getpass
import base64

masterpass = getpass.getpass(
    prompt='Enter new master password: ')

password = masterpass.encode()
salt = b'salt_'
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))

f = Fernet(key)

codec = 'codec'.encode()

print('\ncopy and paste in authenticate.py to update password >>> ')
print(f.encrypt(codec))

