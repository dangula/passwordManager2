from Crypto.Hash import SHA256
from Crypto.Cipher import AES


class User(object):
    """
    Class User
    This Class represents a user object
    """
    def hashPasswd(self, passwd):
        iterations = 154769
        salt = "A1CD3r5FtG8K0980"
        key = ''
        for i in xrange(iterations):
            i
            shash = SHA256.new()
            shash.update(key + passwd + salt)
            key = shash.digest()
        return key

    def __init__(self, uname, passwd, phrase='None'):
        self.username = uname
        self.key = self.hashPasswd(passwd)
        self.phrase = phrase


class AesEncryption(User):
    """
    Class AesEncryption
    This class represents Encryted object
    """
    def AESEncryptionWrapper(self, key, PlainText):
        iv = 'RP3CqI4GELO489WV'
        aesEncryptObj = AES.new(key, AES.MODE_CTR, counter=lambda: iv)
        return aesEncryptObj.encrypt(PlainText)

    def __init__(self, Key, Name, Text, phrase='None'):
        self.name = Name
        self.phrase = phrase
        self.chiperText = self.AESEncryptionWrapper(Key, Text)


def AESDecryptionWrapper(key, CipherText):
    """
    Helper method to decrypt a encryted string
    """
    iv = 'RP3CqI4GELO489WV'
    aesDecryptObj = AES.new(key, AES.MODE_CTR, counter=lambda: iv)
    return aesDecryptObj.decrypt(CipherText)
