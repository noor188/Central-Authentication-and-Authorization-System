import hashlib

# methods
def _encryptPw(self, password):
        '''Encrypt the password with the username and return the sha digest.'''
        hashString = (self.username + password)
        hashString = hashString.encode('UTF-8')
        return hashlib.sha256(hashString).hexdigest()

# start exceptions
class AuthException(Exception):
    def __init__(self, username, user=None):
        super().__init__(username, user)
        self.username = username
        self.user     = user

class UsernameAlreadyExists(AuthException):
    '''Exception to stop adding a user if that username already
    exists in the dictionary. To prevent overwriting an existing user's data
    and the new user might have access to that user's privileges.'''
    pass

class PasswordTooShort(AuthException):
    '''Raise an exception if the password is too short.'''
    pass

# end exceptions 
class User:
    '''Store the username and an encrypted password. Will allow a user to 
    login by checking whether an entered password is valid.'''

    def __init__(self, username, password):
        '''Create a new user object. The password will be encrypted before storing.'''
        self.username   = username
        self.password   = _encryptPw(password)
        self.isLoggedIn = False
           
    def checkPassword(self, password):
        '''Return True if the password is valid for this user, False otherwise.'''
        encrypted = _encryptPw(password)
        return encrypted == self.password

