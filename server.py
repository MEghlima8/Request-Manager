from App import config
from flask import Flask, request
from App.Controller.email_controller import Email
from App.Controller.user_controller import User
from App.Controller import get_request
from App.Controller import send_request
from App.Controller import process
from App.Controller.jwt import Token
from App.Controller import db_postgres_controller as db
from datetime import datetime
import json
import threading
import time


app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(config.configs['SEND_FILE_MAX_AGE_DEFAULT'])
app.secret_key = config.configs['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


# Signup user
@app.route('/signup', methods=['POST'])
def signup():
    
    # Retrieve data from the body and header
    body_data = request.get_json()
    # header_data = request.headers
    
    o_user = User(body_data['username'] , body_data['email'] , body_data['password'])
    j_user = o_user.signup()
    
    if j_user["status"] == "True":
        res = {"status":"success" , "result":"done" , "status-code":201 , "confirm_link":j_user["result"] }
    else:
        res = {"status":"not accepted" , "result":j_user["result"] , "status-code":400}
    return res


# To accept the link confirmation request
@app.route('/confirm', methods=['POST'])
def _check_confirm():
    res = Email.check_confirm_email()
    if res == 'True':
        res = {"status":"accepted" , "result":"email verified now" , "status-code":200}
    else :
        res = {"status":"not accepted" , "result":"link is not valid" , "status-code":400}
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
        res = {"status":"accepted" , "result":{"token":s_token} , "status-code":200}
    elif o_user == 'noactive' :
        res = {"status":"not accepted" , "result":'your account is not active' , "status-code":403}
    else:
        res = {"status":"not accepted" , "result":o_user , "status-code":401}
    return res


@app.route('/add', methods=['POST'])
def add():    
    # Get Token
    try:
        s_token = request.headers.get('Authorization').split()[1]
    except:
        s_token = request.headers.get('Authorization')
    # Get id
    result = Token(token=s_token).handle_token()
    try:                
        # Check Token is valid
        user_id = int(result)
        s_req_id = add_to_db(user_id)        
        
        # Send request to queue
        send_request.send(s_req_id)
        res = process.result(s_req_id,user_id)

        return res
    except:
        # Token is invalid.
        res = {"status":"not accepted" , "result":result , "status-code":401}        
        return res



@app.route('/get-size', methods=['POST'])
def get_size():    
    try:
        s_token = request.headers.get('Authorization').split()[1]        
    except:
        s_token = request.headers.get('Authorization')        
    # Get id
    result = Token(token=s_token).handle_token()    
    try:            
        # Check Token is valid
        user_id = int(result)        
        s_req_id = add_to_db(user_id)        
    except:        
        # Token is invalid.
        res = {"status":"not accepted" , "result":result , "status-code":401}                
        return res    
    # Send request to queue
    send_request.send(s_req_id)
    res = process.result(s_req_id,user_id)
    return res    
    
    

@app.route('/hide-text', methods=['POST'])
def hide_text():
    # Get Token
    try:
        s_token = request.headers.get('Authorization').split()[1]
    except:
        s_token = request.headers.get('Authorization')
    # Get id
    result = Token(token=s_token).handle_token()
    
    try:    
        # Check Token is valid
        user_id = int(result)
        s_req_id = add_to_db(user_id)      
    except:
        # Token is invalid.
        res = {"status":"not accepted" , "result":result , "status-code":401}        
        return res
    
    # Send request to queue
    send_request.send(s_req_id)
    res = process.result(s_req_id,user_id)
    return res


@app.route('/get-text', methods=['POST'])
def get_text():    
    # Get Token
    try:
        s_token = request.headers.get('Authorization').split()[1]
    except:
        s_token = request.headers.get('Authorization')
    # Get id
    result = Token(token=s_token).handle_token()
        
    try:    
        # Check Token is valid
        user_id = int(result)        
        s_req_id = add_to_db(user_id)
    except:
        # Token is invalid.
        res = {"status":"not accepted" , "result":result , "status-code":401}        
        return res    
    # Send request to queue
    send_request.send(s_req_id)    
    res = process.result(s_req_id,user_id)    
    return res



@app.route('/get-result' , methods=['POST'])
def get_result():
    # Get request id
    s_req_id = request.get_json()["request_id"]    
    
    # Get Token
    try:
        s_token = request.headers.get('Authorization').split()[1]
    except:
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
        res = {"status":"not accepted" , "result":result , "status-code":401}   
        return res   


def add_to_db(user_id): 
    type = request.path # ex: /add
    try:
        params = request.get_json()["params"]
    except:
        params = {"params":"None"}
    j_params = json.dumps(params)    
    agent = request.headers['User-Agent']
    method = request.method
    ip =  request.remote_addr
    time = str(datetime.now())
    
    req_id = db.db.addReqToDb(user_id, type, j_params, time, agent, method, ip)
    
    return str(req_id)


if __name__ == '__main__':
    time.sleep(10)
    t = threading.Thread(None, get_request.get_requests_from_queue, None, ())
    t.start()
    app.run(host=config.configs['HOST'], port=config.configs['PORT'] , debug=config.configs['DEBUG'])