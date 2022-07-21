import rsa
import os


def generate_keys():
    (pubKey, privKey) = rsa.newkeys(2048)
    with open('../keys/pubkey.pem', 'wb') as f:
        f.write(pubKey.save_pkcs1('PEM'))
    
    with open('../keys/privkey.pem', 'wb') as f:
        f.write(privKey.save_pkcs1('PEM'))

def generate_openssl_keys():
    os.system("openssl genrsa -out keys/privatekey.pem 4096")
    os.system("pyrsa-priv2pub -i keys/privatekey.pem -o keys/publickey.pem")

def generate_key_by_RSA():
    random_generator = Random.new().read

    key = RSA.generate(4096, random_generator)
    public_key = key.publickey()
    with open('../keys/pubkey.pem', 'wb') as f:
        f.write(public_key.save_pkcs1('PEM'))
    
    with open('../rsa_client/keys/privkey.pem', 'wb') as f:
        f.write(key.save_pkcs1('PEM'))

    return key, public_key

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
