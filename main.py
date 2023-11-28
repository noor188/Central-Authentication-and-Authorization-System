import hashlib

def _encryptPw(self, password):
        '''Encrypt the password with the username and return the sha digest.'''
        hashString = (self.username + password)
        hashString = hashString.encode('UTF-8')
        return hashlib.sha256(hashString).hexdigest()

class User:
    def __init__(self, username, password):
        '''Create a new user object. The password will be encrypted before storing.'''
        self.username = username
        self.password = self._encryptPw(password)
        self.isLoggedIn = False
           
    def checkPassword(self, password):
        '''Return True if the password is valid for this user, False otherwise.'''
        encrypted = self._encryptPw(password)
        return encrypted == self.password

