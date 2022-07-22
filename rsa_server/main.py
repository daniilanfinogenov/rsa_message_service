import rsa
import os


def generate_openssl_keys(length=4096):
    if os.path.exists("keys/"): pass
    else: os.system("mkdir keys")
    os.system(f"openssl genrsa -out keys/privatekey.pem {length}")
    os.system("pyrsa-priv2pub -i keys/privatekey.pem -o keys/publickey.pem")

def load_keys():
    with open('keys/publickey.pem', 'rb') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read())

    with open('keys/privatekey.pem', 'rb') as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read())

    return pubkey, privkey

def encrypt(msg, key):
    return rsa.encrypt(msg.encode('utf-8'), key)

def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('utf-8')
    except:
        return False

def sign_sha1(msg, key):
    return rsa.sign(msg.encode("utf-8"), key, 'SHA-1')

def verify_sha1(msg, signature, key):
    try:
        return rsa.verify(msg.encode('utf-8'), signature, key) == 'SHA-1'
    except:
        return False
