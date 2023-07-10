from flask import request ,make_response
from App.Controller.email_controller import Email
from App.Controller import db_controller as db
import secrets
import json
from App.Controller.validation import Valid
# from App.logs import Log
import hashlib
import uuid


class User:
    
    def __init__(self,  username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password        
        
    # Do signup user
    def signup(self):        
        check_user_info = self.is_valid_signup()        
        
        if check_user_info is not True:
            return check_user_info
        
        # Send confirmation email
        email = Email()
        s_confirmation_link = email.send_confirmation_email(self.email, self.username)
        
        # To save password in database as hash.
        password = hashlib.md5(self.password.encode('utf-8')).hexdigest()
        
        query = 'insert into users (username,email,password,active,confirm_link) values( %s , %s , %s , false , %s)'
        db.execute(query , (self.username, self.email, password, s_confirmation_link,))
        return 'True'
    
    
    def is_valid_signup(self):
        
        # Check duplicate email
        check_exist_email = Email.is_exist_email(self.email)        
        if check_exist_email is None :
            return False
        elif check_exist_email == True :
            return 'duplicate_email'
        elif check_exist_email == 'noactive':
            return 'noactive'    
            
        # Validate signup info
        valid = Valid(username = self.username , email = self.email , password = self.password)
        valid_info = valid.signup()
        if (valid_info == 'email_length') or (valid_info == 'char_email') or (valid_info == 'empty_email'):        
            return valid_info        
        
        if (valid_info == 'password_length') or (valid_info == 'char_password') or (valid_info == 'empty_password') or (valid_info == 'used_info_in_password') :        
            return valid_info        
        
        if (valid_info == 'length_username') or (valid_info == 'char_username') or (valid_info == 'empty_username') :        
            return valid_info        
        
        if (valid_info == 'no_match_passwords'):        
            return valid_info        

        return True

    # Do signin user
    def signin(self):        
        check_user_info = self.is_valid_signin()
        
        if check_user_info == True :
            return 'True'
        
        elif check_user_info == 'noactive':               
            return 'noactive'
        
        elif (check_user_info=='email_length') or (check_user_info=='password_length') or (check_user_info=='char_email') or (check_user_info=='char_password') or (check_user_info=='empty_password') or (check_user_info=='empty_email'):                        
            return check_user_info        
        return 'username or password is invalid.'
    
    
    # True if user password is True. noactive if user did signup but did not active
    def is_valid_signin(self):        
        valid = Valid(username=self.username, password=self.password)        
        valid_info = valid.signin()        
        
        if (valid_info=='empty_username') or (valid_info=='empty_password') :
            return valid_info    
        elif (valid_info=='username_length') or (valid_info=='char_username') or (valid_info=='password_length') or (valid_info=='char_password'):
            return False
        
        # Getback users info
        hash_password = hashlib.md5(self.password.encode('utf-8')).hexdigest()
        
        s_query = 'select username,password,active from users where username=%s and password=%s'
        l_user_info = db.execute(s_query ,(self.username,hash_password,)).fetchone()

        # i[0] is username and i[1] is password and i[2] is active column
        if l_user_info is not None:
            if l_user_info[2] == True: 
                return True  
            return 'noactive'
        return False


    # Getback user_info
    @staticmethod
    def get_user_info(l_data_request):        
        user_info = request.data.decode('utf-8')
        user_info = json.loads(user_info)        
        return [user_info[req] for req in l_data_request]