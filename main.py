from App import config
from flask import Flask, request
from App.Controller.email_controller import Email
from App.Controller.user_controller import User
from App.Controller import get_request
from App.Controller import send_request
from App.Controller import process
from App.jwt import Token
from App.Controller import db_controller as db
from datetime import datetime
import sys
import json
import threading
import os


app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(config.configs['SEND_FILE_MAX_AGE_DEFAULT'])
app.secret_key = config.configs['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


# Signup user
@app.route('/signup', methods=['GET' , 'POST'])
def signup():
    
    # Retrieve data from the body and header
    body_data = request.get_json()
    # header_data = request.headers
    
    o_user = User(body_data['username'] , body_data['email'] , body_data['password'])
    s_user = o_user.signup()
    
    if s_user == 'True':
        res = {"status":"accepted" , "result":"done"}
    else:
        res = {"status":"not accepted" , "result":s_user}
    return res


# To accept the link confirmation request
@app.route('/confirm', methods=['GET' , 'POST'])
def _check_confirm():
    res = Email.check_confirm_email()
    if res == 'True':
        res = {"status":"accepted" , "result":"email is verified"}
    else :
        res = {"status":"not accepted" , "result":"link is not valid"}
    return res


# Signin user
@app.route('/signin' ,methods=['POST'])
def signin():
        
    j_body_data = request.get_json()
    s_username = j_body_data['username']
    s_password = j_body_data['password']
    
    o_user = User(username = s_username , password = s_password)
    o_user = o_user.signin()
    
    if o_user == 'True':
        o_token = Token(username=s_username)
        s_token = o_token.encode_token()
        res = {"status":"accepted" , "result":{"token":s_token}}
    else:
        res = {"status":"not accepted" , "result":o_user}
    return res


@app.route('/add', methods=['POST'])
def add():    
    # Get Token
    s_token = request.headers.get('Authorization')
        
    # Get id
    result = Token(token=s_token).handle_token()        
    try:        
        # Token is valid
        user_id = int(result)
        s_req_id = add_to_db(user_id) 
                       
        # Send request to queue
        send_request.send(s_req_id)        
        res = process.result(s_req_id,user_id)
        print('s_req_id,user_id: ',s_req_id,user_id)
        try:            
            if res == 'None' :                
                # add request accepted but not processed yet 
                res = {"status":"accepted" , "result":"not processed yet" , "request_id":s_req_id}
        finally:            
            return res
    except:        
        # Token is invalid.
        res = {"status":"not accepted" , "result":result}        
        return res


@app.route('/get-result' , methods=['POST'])
def get_result():
    # Get request id
    s_req_id = request.get_json()["request_id"]    
    
    # Get Token
    s_token = request.headers.get('Authorization')
    
    # Get id
    result = Token(token=s_token).handle_token()        
    try:        
        # Token is valid
        user_id = int(result)                
        res = process.result(s_req_id,user_id)        
        return res
    except:
        # Token is invalid.        
        res = {"status":"not accepted" , "result":result}   
        return res   


def add_to_db(user_id): 
    type = request.path # ex: /add
    params = request.get_json()["params"]
    j_params = json.dumps(params)    
    agent = request.headers['User-Agent']
    method = request.method
    ip =  request.remote_addr
    time = str(datetime.now())
    
    query = "INSERT INTO request (user_id,type,params,time,agent,method,ip) VALUES (%s , %s , %s , %s , %s , %s , %s)"
    db.db.execute( query , (user_id, type, j_params, time, agent, method, ip))
    
    query = "SELECT id FROM request ORDER BY id DESC LIMIT 1"
    req_id = db.db.execute(query , ()).fetchall()[0][0]
    return str(req_id)


# receive request from queue 
def get_requests_from_queue():
    try:
        get_request.main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    

if __name__ == '__main__':

    t = threading.Thread(None, get_requests_from_queue, None, ())
    t.start()
    app.run(host=config.configs['HOST'], port=config.configs['PORT'] , debug=config.configs['DEBUG'])
    