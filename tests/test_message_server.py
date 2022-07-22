import os
import sys
sys.path.insert(1, "../rsa_server/")
import main
import unittest

class Test_Main(unittest.TestCase):

    def test_generate_openssl_pubkey(self):
        main.generate_openssl_keys()
        self.assertTrue(os.path.exists("keys/publickey.pem"))

    def test_generate_openssl_privkey(self):
        main.generate_openssl_keys()
        self.assertTrue(os.path.exists("keys/privatekey.pem"))
    
    def test_load_keys(self):
        self.assertIsNotNone(main.load_keys())

    def test_encrypt(self):
        self.addTypeEqualityFunc(bytes, main.encrypt("hello", main.load_keys()[0]))
        
    
    def test_decrypt(self):
        encmsg = main.encrypt("hello", main.load_keys()[0])
        privkey = main.load_keys()[1]
        decmsg = main.decrypt(encmsg, privkey)
        self.assertEquals("hello", decmsg)
        
class Test_Message_Server(unittest.TestCase):
    def test_something(self):
        pass


if __name__ == '__main__':
    unittest.main()