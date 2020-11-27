from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
import getpass
import base64


def authenticate():
    masterpass = getpass.getpass(
        prompt='[PasswordManager] Enter the master password: ')

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
    try:
        codec = b'gAAAAABfwYnXxLDLOCqLgHeKm8g2BDayAMvvXejUdQ7bx2rg76v_nFq2Xrx6oqtSbkMEp9H_wQfY7GYzXy9TGoWAzknawUe6zQ=='
        decrypted = f.decrypt(codec)
    except InvalidToken as e:
        print('[PasswordManager] Invalid Key')
        return None
    return key
