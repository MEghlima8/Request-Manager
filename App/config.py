import os
from dotenv import load_dotenv
load_dotenv()

configs = {
    
    'HOST' : os.getenv('HOST') , 
    'PORT' : os.getenv('PORT') , 
    'DEBUG' : os.getenv('DEBUG') , 
    'SECRET_KEY' : os.getenv('SECRET_KEY') ,
    'SEND_FILE_MAX_AGE_DEFAULT' : os.getenv('SEND_FILE_MAX_AGE_DEFAULT') ,
    
    # Database 
    'DB_NAME' : os.getenv('DB_NAME') ,
    'DB_HOST' : os.getenv('DB_HOST') ,
    'DB_USER' : os.getenv('DB_USER') ,
    'DB_PASSWORD' : os.getenv('DB_PASSWORD') ,
    'DB_PORT' : os.getenv('DB_PORT') ,
    
    # JWT
    'JWT_SECRET_KEY' : os.getenv('JWT_SECRET_KEY') ,
    
    # Email
    'SMTP_SERVER' : os.getenv('SMTP_SERVER') ,
    'SMTP_PORT' : os.getenv('SMTP_PORT') ,
    'SENDER_EMAIL' : os.getenv('SENDER_EMAIL') ,
    'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD') ,
}