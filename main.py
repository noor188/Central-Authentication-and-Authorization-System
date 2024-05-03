import hashlib

# methods
def _encryptPw(username, password):
        '''Encrypt the password with the username and return the sha digest.'''
        hashString = (username + password)
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

class InvalidUsername(AuthException):
    '''Raise an exception if username does not exist in the users dict.'''
    pass

class InvalidPassword(AuthException):
    '''Raise an exception if the password does not match.'''
    pass

class PermissionError(Exception):
    '''Raise an exception if permisiion either does not exist or
    already exist'''
    pass

class NotLoggedInError(AuthException):
    '''Raise an excpetion if the username is not logged in'''
    pass

class NotPermittedError(AuthException):
    '''Raise an exception if the username is not grated the permission'''
    pass

# end exceptions 
class User:
    '''Store the username and an encrypted password. Will allow a user to 
    login by checking whether an entered password is valid.'''

    def __init__(self, username, password):
        '''Create a new user object. The password will be encrypted before storing.'''
        self.username   = username
        self.password   = _encryptPw(username, password)
        self.isLoggedIn = False
           
    def checkPassword(self, password):
        '''Return True if the password is valid for this user, False otherwise.'''
        encrypted = _encryptPw(self.username, password)
        return encrypted == self.password
    

class Authenticator:
    '''Handles user managment and logging in/out'''

    def __init__(self):
        '''Construct an authentucator, simply a mapping of usrnames
        to user objects.'''
        self.users = {}
    
    def add_user(self, username, password):
        '''Creats a user object and add it to the user dictinary.
        It checks two conditions, username already exist and too short password'''
        if username in self.users:
            raise UsernameAlreadyExists(username)
        if len(password)< 6:
            raise PasswordTooShort(username)
        self.users[username] = User(username, password)
    
    def login(self, username, password):
        '''Logs in a user. It handles two conditions, username does not exist and
        pasword does not match.'''
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(username)

        if not user.checkPassword(password):
            raise InvalidPassword(username, user)

        user.isLoggedIn = True
        return True
    
    def is_logged_in(self, username):
        '''Checks if a particular user is logged in'''
        if username in self.users:
            return self.users[username].isLoggedIn
        return False


class Authorizer:
        ('''Deals woth permission and checs wherther a user can perform an activity'''
        def __init__(self, authenticator):
            self.authenticator = authenticator
            self.permissions = {}
        
        def add_permission(self, perm_name):
            '''Create a new permission that users can be added to'''
            try:
                perm_set = self.permissions[perm_name]
            except KeyError:
                self.permissions[perm_name] = set()                                
            else:
                raise PermissionError('Permission already exist')            

        def permit_user(self, username, perm_name):
            '''Grant the given permission to the user'''
            try:
                perm_set = self.permissions[perm_name]
            except KeyError:
                raise PermissionError('Permission does not exist')
            else:
                if username not in self.authenticator.users:
                    raise InvalidUsername(username)
                perm_set.add(username)

        def check_permission(self, username, perm_name):
            '''Checks whether the username is granted the given permission'''

            if not self.authenticator.is_logged_in(username):
                raise NotLoggedInError(username)

            try:
                perm_set = self.permissions[perm_name]
            except KeyError:
                raise PermissionError('Permission does not exist')
            else:
                if username in perm_set:
                    return True
                raise NotPermittedError(username))
    
#instance
authenticator =Authenticator()
authorizer = Authorizer(authenticator)
    
    
    

    
    


