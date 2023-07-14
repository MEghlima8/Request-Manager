from App import config
import psycopg2

database = config.configs['DB_NAME']
host = config.configs['DB_HOST']
user = config.configs['DB_USER']
port = config.configs['DB_PORT']
password = config.configs['DB_PASSWORD']

class PostgreSQL:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, database, user, password, port):
        if not hasattr(self, 'connection'):
            self.host = host
            self.database = database
            self.user = user
            self.password = password
            self.port = port
            self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
    def execute_query(self, query, args=()):        
        cur = self.connection.cursor()
        cur.execute(query,args)
        self.connection.commit()  
        return cur
    
    # Add request to database
    def addReqToDb(self , user_id, type, j_params, time, agent, method, ip):
        query = "INSERT INTO request (user_id,type,params,time,agent,method,ip) VALUES (%s , %s , %s , %s , %s , %s , %s) RETURNING id"
        args =(user_id, type, j_params, time, agent, method, ip)
        req_id = self.execute_query(query, args).fetchall()[0][0]
        return req_id
        
    # Retrieve user id
    def getUserId(self, username):
        query = "select id from users where username=%s"
        args =(username,)
        get_id = self.execute_query(query,args).fetchone()         
        return get_id

    # Add token to database
    def addTokenToDb(self, s_token,username):
        query = 'UPDATE users SET token=%s where username=%s'
        args =(s_token, username,)
        self.execute_query(query,args)
        return 'True'
    
    # After Successful sign up Add user info to database
    def signupUser(self , username, email, password, s_confirmation_link):
        query = 'insert into users (username,email,password,active,confirm_link) values( %s , %s , %s , false , %s)'
        args =(username, email, password, s_confirmation_link,)
        self.execute_query(query,args)
        return 'True'

    # Retrieve sign in info
    def checkSigninInfo(self, username, hash_password):
        query = 'select username,password,active from users where username=%s and password=%s'
        args =(username, hash_password,)
        res = self.execute_query(query,args).fetchone()
        return res
    
    # Insert request to Process table
    def insertToProcess(self, req_id):
        query = 'INSERT INTO process (req_id, status) VALUES(%s , %s)'
        args = (req_id, 'processing',)
        res = self.execute_query(query,args)
        return res
    
    # Retrieve request info
    def getReqInfo(self, req_id):
        query = "SELECT * FROM request WHERE id=%s"
        args = (req_id,)
        res = self.execute_query(query,args).fetchall()
        return res
    
    # Update Process table when process is done
    def updateProcess(self, start_time, end_time, result, req_id):
        query = "UPDATE process set start_time=%s, end_time=%s, result=%s, status='done' WHERE req_id=%s"
        args = (start_time, end_time, result, req_id,)
        res = self.execute_query(query,args)        
        return res
    
    # Retrieve process result
    def getReqProcessRes(self, user_id, s_req_id):
        query = "SELECT result,status FROM request INNER JOIN process ON request.id=process.req_id WHERE request.user_id=%s AND process.req_id=%s"
        args = (user_id, s_req_id,)
        res = self.execute_query(query,args).fetchall()
        return res

    # Check the request is in request table or not
    def checkIsInReqTB(self, user_id, s_req_id):
        query = "SELECT * FROM request WHERE user_id=%s AND id=%s"
        args = (user_id, s_req_id,)
        res = self.execute_query(query,args).fetchall()
        return res
    
    def getUserConfirmLink(self, s_link):
        query = 'select confirm_link from users where confirm_link=%s'
        args = (s_link,)
        res = self.execute_query(query,args).fetchone()
        return res
    
    def activeUser(self, s_link):
        query = 'UPDATE users SET active=%s  where confirm_link=%s'
        args = ('true', s_link,)
        cur = self.execute_query(query,args)
        return cur
        
    # Retrieve active column from users table
    def getActiveFromUsers(self, email):
        query = 'select active from users where email=%s'
        args = (email,)
        res = self.execute_query(query,args).fetchone()
        return res
    
    def checkDuplicateUsername(self, username):
        query = 'select username from users where username=%s'
        args = (username,)
        res = self.execute_query(query,args).fetchone()
        if res != None:
            return 'True'
        return None
    
    def getImagesName(self, s_req_id):
        query = "SELECT user_id FROM request WHERE id=%s"
        args = (int(s_req_id),)
        user_id = self.execute_query(query,args).fetchall()[0][0]

        query = "SELECT result FROM request INNER JOIN process ON request.id=process.req_id WHERE request.user_id=%s AND request.type=%s"
        args = (user_id,'/hide-text')
        res = self.execute_query(query,args).fetchall()

        return res

        

db = PostgreSQL(host=host, database=database, user=user, password=password, port=port)
db.connect()