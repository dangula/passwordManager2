from key import User
from key import AesEncryption
from key import AESDecryptionWrapper
from Crypto.Hash import SHA256
import re
import shelve


ALPHA_NUM_PATTERN = '^[a-zA-Z0-9]+$'
PASSWORD_CHECK = '^[a-zA-Z0-9_@#$*]+$'
PHRASE_PATTERN = '^[a-zA-Z0-9\s]+$'


class shelveWrapper(object):
    """
    """
    def __init__(self, shelveDB):
        self.shelveDB = shelveDB

    def checkhashPasswd(self, password):
            iterations = 154769
            salt = "A1CD3r5FtG8K0980"
            key = ''
            for i in xrange(iterations):
                i
                shash = SHA256.new()
                shash.update(key + password + salt)
                key = shash.digest()
            return key

    def writeUser(self, userName, Password, Phrase):
        """
        Method to write a User Object to shelve db
        The user is shelved if there is no user with the same
        username and pass validateUser and checkPassword validation passes
        """
        s = shelve.open(self.shelveDB)
        try:
            validateUserData = validateUser(userName, Password, Phrase)
            if validateUserData == 'success':
                kList = s.keys()
                if userName in kList:
                    raise ValueExistsError
                else:
                    s[userName] = [User(userName, Password, Phrase), {}]
                    return 'User Created Successfully'
            else:
                return validateUserData
        except ValueExistsError, e:
            return "{'username': " + e.value+"}"
        finally:
            s.close()

    def retriveUser(self, userName, password):
        """
        This method retrives a shelved user from shelve db.
        Returns user object if the userName exists with the
        given password. If no user exists or username and password
        combo dont match then 'No user found' message is returned
        """
        s = shelve.open(self.shelveDB, 'r')
        try:
            #UserInfoObj = s[userName]
            data = s[userName][0]
            if isinstance(data, User):
                if data.key == self.checkhashPasswd(str(password)):
                    return data
                else:
                    raise KeyError
            else:
                raise KeyError
        except KeyError:
            return "User Data not found"
        finally:
            s.close()

    def writeEncrytptionData(self, userName, password, Name,
                             PlainText, Phrase):
        """
        Method to write a AesEncryption Object to shelve db
        The object is shelved if there is a existing user with
        the specified username and password and validatePasswordInfo passed
        """
        s = shelve.open(self.shelveDB, writeback=True)
        try:
            validatePasswordData = validatePasswordInfo(Name, PlainText,
                                                        Phrase)
            if validatePasswordData == 'success':
                user = self.retriveUser(userName, password)
                if user == 'User Data not found':
                    raise KeyError
                cur_passwds = s[userName][1]
                kList = cur_passwds.keys()
                if Name in kList:
                    raise ValueExistsError
                else:
                    data = AesEncryption(user.key, Name,
                                         PlainText, Phrase)
                    s[userName][1].update({Name: data})
                    return 'Password Info created successfully'
            else:
                return validatePasswordData
        except KeyError:
            return ("{'error' : ' No user found for username"
                    "password combination'}")
        except ValueExistsError, e:
            return "{'Name': "+e.value+"}"
        s.close()

    def retriePasswdInfo(self, UserName, Passwd, Name):
        s = shelve.open(self.shelveDB, 'r')
        try:
            data = s[UserName][0]
            if isinstance(data, User):
                if data.key == self.checkhashPasswd(str(Passwd)):
                    passInfo = s[UserName][1][Name]
                    if isinstance(passInfo, AesEncryption):
                        return passInfo
                    else:
                        raise KeyError
                else:
                    raise KeyError
            else:
                raise KeyError
        except KeyError:
            return "No data Found"
        s.close()

    def retrivePasswordInfo_NameSearch(self, UserName, Passwd,
                                       searchKey, SearchString):
        s = shelve.open(self.shelveDB, 'r')
        Result_List = []
        try:
            Userdata = s[UserName][0]
            if Userdata.key == self.checkhashPasswd(str(Passwd)):
                passInfo = s[UserName][1]
                for keys in passInfo.keys():
                    data = passInfo[keys]
                    if searchKey == 'name':
                        if SearchString in data.name:
                            Result_List.append(data)
                    if searchKey == 'phrase':
                        if SearchString in data.phrase:
                            Result_List.append(data)
                if len(Result_List) == 0:
                    return {'Result': 'No Data Found with search criteria'}
                else:
                    return_data = []
                    for data in Result_List:
                        passwd = AESDecryptionWrapper(Userdata.key,
                                                      data.chiperText)
                        resDict = {'name': data.name, 'password': passwd,
                                   'phrase': data.phrase}
                        return_data.append(resDict)
                    return return_data
            else:
                raise KeyError
        except KeyError:
            return "No data Found"


class ValueExistsError(Exception):
    """
    This class defines user defined Exception when a user name
    or password name already exists
    """
    def __init__(self):
        self.value = 'Key Already Exists'

    def __str__(self):
        return repr(self.value)


def validateUser(username, password, phrase):
    """
    This method validates user data before shelving it.
    For a user to be valid it should  pass the following validation
    1. username length must be between 4 and 50 chars
    2. username must be alpha numeric only
    3. phrase length must be between 4 and 100
    4. phrase must be alpha only(spaces allowed)
    5. password length must be between 4 and 50
    6. password must be alpha numeric , special chars
       _ ,@ , #, $ and * are allowed
    7. password must pass check password validation
    """
    if len(username) >= 4 and len(username) <= 50:
        if re.match(ALPHA_NUM_PATTERN, username):
            if len(phrase.replace(' ', '')) >= 4 and len(phrase) <= 100:
                if re.match(PHRASE_PATTERN, phrase):
                    if len(password) >= 8 and len(password) <= 50:
                        if re.match(PASSWORD_CHECK, password):
                            return CheckPassword(password)
                        else:
                            return ("{'password': ' can only contain"
                                    " alphabets,digits or special chars"
                                    " (_, @, #, $, *)'}")
                    else:
                        return "{'password': ' must be between 8 an 50 chars'}"
                else:
                    return ("{'phrase': ' can only contain alphabets and "
                            "digits(white space allowed'}")
            else:
                return ("{'phrase': ' must be between 4 and 100 "
                        "chars(excluding spaces)'}")
        else:
            return "{'username': ' can only contain alphabets and digits'}"
    else:
        return "{'username': ' must be between 4 an 50 chars'}"


def validatePasswordInfo(name, password, phrase):
    """
    This method validates password data before shelving it.
    For a user to be valid it should  pass the following validation
    1. name length must be between 4 and 50 chars
    2. name must be alpha numeric only
    3. phrase length must be between 4 and 100
    4. phrase must be alpha only(spaces allowed)
    5. password length must be at least 4 chars
    6. password with only spaces is not allowed

    """
    if len(name) >= 4 and len(name) <= 50:
        if re.match(ALPHA_NUM_PATTERN, name):
            if len(phrase.replace(' ', '')) >= 4 and len(phrase) <= 50:
                if re.match(PHRASE_PATTERN, phrase):
                    if len(password.replace(' ', '')) >= 4:
                        return 'success'
                    else:
                        return ("{'password': 'password length must be atlest"
                                " 4(not counting white spaces)'}")
                else:
                    return ("{'phrase': ' can only contain alphabets and"
                            " digits(white space allowed'}")
            else:
                return ("{'phrase': ' must be between 4 and "
                        "100 chars(exluding spaces)'}")
        else:
            return "{'name': ' can only contain alphabets and digits'}"
    else:
        return "{'name': ' must be between 4 an 50 chars'}"


def CheckPassword(password):
    """
    This method validates user password
    For user password to be valid, the password should
    contain at least 3 of the following 4
    1. a number
    2. a lower case letter
    3. a upper case letter
    4. one of the following special chars _,@,*,# and $
    """
    score = 0
    if re.search('\d+', password):
        score = score + 1
    if re.search('[a-z]', password):
        score = score + 1
    if re.search('[A-Z]', password):
        score = score+1
    if re.search('.[_,@,*,#,$]', password):
        score = score + 1
    if score >= 3:
        return 'success'
    else:
        return ("{'password ': ' must contain 3 of the following 4 - digits,"
                " lowercase, uppercase and special chars(_,@,*,#,$)}")
