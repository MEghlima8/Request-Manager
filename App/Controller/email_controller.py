from flask import request
from App.Controller import db_postgres_controller as db
import smtplib
import ssl
import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
from App import config


class Email:
    
    def  __init__(self):
        self.s_smtp_server = config.configs['smtp_server']
        self.i_port = int(config.configs['smtp_port'])
        self.s_sender_email = config.configs['sender_email']
        self.s_password = config.configs['smtp_password']

    def send_confirmation_email(self, email, username):

        # Verify link key
        s_link_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
        
        t = threading.Thread(None, self.send_confirmation_link_multiThread, None, (email, username, s_link_key))
        t.start()
        
        return s_link_key
        
        
    def send_confirmation_link_multiThread(self, email, username, s_link_key ):
                
        # The link to which the confirmation request will be emailed
        s_link = 'http://localhost:5000/confirm?link=%s' % s_link_key
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Confirmation Link"
        msg['From'] = self.s_sender_email
        msg['To'] = email
        
        s_text = '''Hello {username} , Click on the below link to confirm your email ,otherwise ignore this message.
        {link}
        '''.format(username=username, link=s_link)
        
        s_text_mime = MIMEText(s_text, 'plain','utf-8')
        
        msg.attach(s_text_mime)
        

        # reference : https://www.mongard.ir/one_part/170/sending-email-python/
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.s_smtp_server, self.i_port, context=context) as server:
            server.login(self.s_sender_email, self.s_password) 
            server.sendmail(self.s_sender_email, email, msg.as_string())
            server.quit()
            
            return s_link_key

        
    

    @staticmethod
    def check_confirm_email():
        s_link = request.get_json()['confirm_link']
        
        query = 'select confirm_link from users where confirm_link=%s'
        is_exist = db.execute(query,(s_link,)).fetchone()
        
        if is_exist is not None :
            query = 'UPDATE users SET active=%s  where confirm_link=%s'
            db.execute(query, ('true',s_link,))
            return 'True'
        
        # Confirm link in wrong
        return 'False'
    

    @staticmethod
    def is_exist_email(email):        
        # Getback users info
        query = 'select active from users where email=%s'
        l_users_info = db.execute(query ,(email,)).fetchone()        
        if l_users_info is None :    
            return False
        elif l_users_info[0] == True:            
            return True
        return 'noactive'
        
        