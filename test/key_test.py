from key import User
from key import AesEncryption
from key import AESDecryptionWrapper
import unittest


class Test_keyClass(unittest.TestCase):
    
    def test_user_basic1(self):
        user1 = User('u1','p1')
        self.assertEqual('u1', user1.username, "check name")
        self.assertNotEqual('p1', user1.key, 'check key')
        self.assertEquals(user1.key,user1.hashPasswd('p1'), 'check key')
        self.assertEquals('None', user1.phrase, 'check phrase')
        
    def test_user_basic2(self):
        user1 = User('u2','p2','user 2')
        self.assertEqual('u2', user1.username, "check name")
        self.assertNotEqual('p2', user1.key, 'check key')
        self.assertEquals(user1.key,user1.hashPasswd('p2'), 'check key')
        self.assertEquals('user 2', user1.phrase, 'check phrase')
    
    def test_enc_basic1(self):
        user1 = User('user','Password_1')
        encData = AesEncryption(user1.key,'Data1','Password1')
        self.assertEqual('Data1', encData.name, 'Check name');
        self.assertNotEquals('Password1', encData.chiperText, 'Check password')
        self.assertEquals(encData.AESEncryptionWrapper(user1.key, 'Password1'), encData.chiperText, 'Check Cipher Text')
        self.assertEquals('Password1', AESDecryptionWrapper(user1.key, encData.chiperText), 'Check Decrypted password')
        self.assertEquals('None', encData.phrase, 'check phrase')
    
    def test_enc_basic2(self):
        user1 = User('user','Password_1')
        encData = AesEncryption(user1.key,'Data2','hahah_23423_E94932_TEST_HG','SOME PHRASE')
        print user1.key
        print len(user1.key)
        self.assertEqual('Data2', encData.name, 'Check name');
        self.assertNotEquals('hahah_23423_E94932_TEST_HG', encData.chiperText, 'Check password')
        self.assertEquals(encData.AESEncryptionWrapper(user1.key, 'hahah_23423_E94932_TEST_HG'), encData.chiperText, 'Check Cipher Text')
        self.assertEquals('hahah_23423_E94932_TEST_HG', AESDecryptionWrapper(user1.key, encData.chiperText), 'Check Decrypted password')
        self.assertEquals('SOME PHRASE', encData.phrase, 'check phrase')

    
    

if __name__ == "__main__":
    unittest.main()