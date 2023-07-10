import re 
import Levenshtein

class Valid:
    
    def __init__(self, username=None, email=None, password=None):
        self.username = username        
        self.email = email
        self.password = password
        
        
    # Check email is valid or not
    def is_valid_email(self):
        if not self.email :
            return 'empty_email' # Email is empty
        
        if len(self.email) > 100:
            return 'email_length' # Email length must be less than 100 chars
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, self.email):
            return True
        else:
            return 'char_email' # Email chars is not valid


    # Check username is valid or not
    def is_valid_username(self):
        if not self.username :
            return 'empty_username' # username is empty
        
        if len(self.username) > 30:
            return 'username_length'  # username length is must be less than 30 letters
        
        username_allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._')
        if not set(self.username).issubset(username_allowed_chars):
            return 'char_username' # username chars is not valid
    
    
    # Check password is valid or not
    def is_valid_password(self):
        if not self.password :
            return 'empty_password'
        
        pass_pattern1 = re.compile(r'.{8,30}') # The password must be between 8 and 30 characters long
        pass_pattern2 = re.compile(r'[A-Za-z]+') # The password must have english letter(s)
        pass_pattern3 = re.compile(r'\d+') # The password must have number(s)
        pass_pattern4 = re.compile(r'[!@#$%^&*()<>?/\|}{~:]') # The password must have special character(s)
        
        sim = self.calculate_similarity(self.username , self.password)
        if sim >= 75 :
            return 'used_info_in_password'
            
        if pass_pattern1.fullmatch(self.password) is None:
            return 'password_length'
        elif pass_pattern2.search(self.password) is None or pass_pattern3.search(self.password) is None or pass_pattern4.search(self.password) is None:
            return 'char_password'


    # check whether the username and password are valid
    def signin(self):
        check_valid_username = self.is_valid_username()
        if check_valid_username == 'username_length' or check_valid_username == 'char_username' or check_valid_username == 'empty_username':
            return check_valid_username
        
        check_valid_password = self.is_valid_password()
        if check_valid_password == 'password_length' or check_valid_password == 'char_password' or check_valid_password == 'empty_password' or check_valid_password == 'used_info_in_password' :
            return check_valid_password
        return True


    # It checks whether the signup info are valid
    def signup(self):    
        
        check_valid_username = self.is_valid_username()
        if check_valid_username == 'username_length' or check_valid_username == 'char_username' or check_valid_username == 'empty_username':
            return check_valid_username
        
        check_valid_email = self.is_valid_email()
        if check_valid_email == 'email_length' or check_valid_email == 'char_email' or check_valid_email == 'empty_email':
            return check_valid_email
        
        check_valid_password = self.is_valid_password()
        if check_valid_password == 'password_length' or check_valid_password == 'char_password' or check_valid_password == 'empty_password' or check_valid_password == 'used_info_in_password':
            return check_valid_password
        
        return True
    
    
    # Used Levenshtein distance to calculate similarity between two strings
    def calculate_similarity(self,string1, string2):
        distance = Levenshtein.distance(string1, string2)
        max_length = max(len(string1), len(string2))
        
        similarity = 1 - (distance / max_length)
        return similarity * 100
