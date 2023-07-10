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
    
    'SESSION_TYPE' : os.getenv('SESSION_TYPE') ,
    # Redis
    'REDIS_HOST' : os.getenv('REDIS_HOST') ,
    'REDIS_PORT' : os.getenv('REDIS_PORT') ,
    'REDIS_PASSWORD' : os.getenv('REDIS_PASSWORD') ,
    'REDIS_DB_NUMBER' : os.getenv('REDIS_DB_NUMBER')
}