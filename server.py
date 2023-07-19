from App import config
from flask import Flask, request, render_template, session, make_response, abort
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
import uuid
import os
from pydub import AudioSegment


app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(config.configs['SEND_FILE_MAX_AGE_DEFAULT'])
app.secret_key = config.configs['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def check_token():
    # Get Token  
    access_token = request.cookies.get('access_token')    
    # Get id
    result = Token(token=access_token).handle_token()
        
    try:    
        # Check Token is valid
        user_id = int(result)      
        res = {"status":"accepted" , "result":{"user_id":user_id} , "status-code":200}
    except:
        # Token is invalid.
        res = {"status":"not accepted" , "result":result , "status-code":401}
    return res    


def check_token_and_add_req_to_db():
    # Get Token  
    access_token = request.cookies.get('access_token')    
    # Get id
    result = Token(token=access_token).handle_token()    
    try:    
        # Check Token is valid
        user_id = int(result)              
        s_req_id = add_to_db(user_id)        
        res = {"status":"accepted" , "result":{"request_id":s_req_id, "user_id":user_id} , "status-code":200}        
    except:
        # Token is invalid.
        res = {"status":"not accepted" , "result":result , "status-code":401}        
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
        session['username'] = s_username
        session['logged_in'] = True
                
        # Set cookie : access token 
        o_token = Token(username=s_username)
        s_token = o_token.encode_token()
        res = {"status":"accepted" , "result":{"token":s_token} , "status-code":200}        
        resp = make_response(res)
        resp.set_cookie('access_token', s_token,max_age= 60 * 60)            

    elif o_user == 'noactive' :
        resp = {"status":"not accepted" , "result":'your account is not active' , "status-code":403 ,}        
    else:
        resp = {"status":"not accepted" , "result":o_user , "status-code":401}
        
    return resp


def get_route_reqs_status(user_id , type):
    res_done = db.db.resDone(user_id, type)
    res_queue = db.db.resQueue(user_id, type)
    res_processing = db.db.resProcessing(user_id, type)
    res = {'queue':res_queue, 'processing': res_processing, 'done': res_done}
    return res


# Retrieve request_id , status, params , result of add calc
@app.route('/get-all-add-req', methods = ['POST'])
def get_all_add_req():
    res = check_token()
    if res['status-code'] == 200:
        route_reqs_status = get_route_reqs_status(res["result"]["user_id"], '/add')
        res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}
        return res
    elif res['result'] == 'ExpiredToken':
        
        if session['logged_in'] is not None and session['logged_in'] is True:
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
            
            route_reqs_status = get_route_reqs_status(user_id, '/add')
            res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}            
            
            resp = make_response(res)
            resp.set_cookie('access_token', s_token,max_age= 60 * 10)
            return resp
    abort (401)



# Retrieve request_id , status, params , result of stegano Image
@app.route('/get-all-img-res', methods = ['POST'])
def get_all_img_res():
    res = check_token()
    
    if res['status-code'] == 200:
        route_reqs_status = get_route_reqs_status(res["result"]["user_id"], '/hide-text')
        res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}
        return res
    
    elif res['result'] == 'ExpiredToken':
        if session['logged_in'] is True:
            
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
    
            route_reqs_status = get_route_reqs_status(user_id, '/hide-text')
            res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}
            resp = make_response(res)
            resp.set_cookie('access_token', s_token,max_age= 60 * 60)
    
            return resp
    abort (401)




# Retrieve request_id , status, params , result of steg audio
@app.route('/res-steg-audio' , methods =['POST'])
def res_steg_audio():
    res = check_token()
    if res['status-code'] == 200:
        route_reqs_status = get_route_reqs_status(res["result"]["user_id"], '/hide-in-sound')
        res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}
        return res
    
    elif res['result'] == 'ExpiredToken':
        if session['logged_in'] is True:
    
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
    
            route_reqs_status = get_route_reqs_status(user_id, '/hide-in-sound')
            res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}
            resp = make_response(res)
            resp.set_cookie('access_token', s_token,max_age= 60 * 60)
            return resp
    abort (401)


# Retrieve request_id , status, params , result of extract steg audio
@app.route('/res-extr-steg-audio' , methods =['POST'])
def res_extr_steg_audio():
    res = check_token()
    if res['status-code'] == 200:
        route_reqs_status = get_route_reqs_status(res["result"]["user_id"], '/get-from-sound')
        res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}
        return res
    
    elif res['result'] == 'ExpiredToken':
        if session['logged_in'] is True:
    
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
    
            route_reqs_status = get_route_reqs_status(user_id, '/get-from-sound')
            res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}
            resp = make_response(res)
            resp.set_cookie('access_token', s_token,max_age= 60 * 60)
            return resp
    abort (401)


# Retrieve request_id , status, params , result of extract image
@app.route('/res-extr-steg-img' , methods =['POST'])
def res_steg_image():
    res = check_token()
    if res['status-code'] == 200:
        route_reqs_status = get_route_reqs_status(res["result"]["user_id"], '/get-text')
        res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}
        return res
    
    elif res['result'] == 'ExpiredToken':
        if session['logged_in'] is True:
            
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
    
            route_reqs_status = get_route_reqs_status(user_id, '/get-text')
            res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}
            resp = make_response(res)
            resp.set_cookie('access_token', s_token,max_age= 60 * 60)
    
            return resp
    abort (401)



# Just retrieve count and status
@app.route('/res-add-calc' , methods=["POST"])
def res_add_calc():
    res = check_token()
    if res['status-code'] == 200:
        user_reqs_status = db.db.getAllReq(res["result"]["user_id"], '/add', None)
        try: 
            dict_result = {"count" : user_reqs_status[0][1]}
        except: dict_result = {"count" : 0}
        j_result = json.dumps(dict_result)
        return j_result
    elif res['result'] == 'ExpiredToken':
        if session['logged_in'] is True:
            
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
    
            user_reqs_status = db.db.getAllReq(user_id, '/add', None)
            resp = make_response(user_reqs_status)
            resp.set_cookie('access_token', s_token,max_age = 60 * 60)
    
            return resp
    abort (401)


# Just retrieve count and status
@app.route('/get-all-img-steg-req' , methods=['POST'])
def get_all_img_steg_req():
    res = check_token()    
    if res['status-code'] == 200:
        user_reqs_status = db.db.getAllReq(res["result"]["user_id"], '/hide-text', '/get-text')
        try: 
            dict_result = {"count" : user_reqs_status[0][1]}
        except: dict_result = {"count" : 0}
        j_result = json.dumps(dict_result)
        return j_result
        
    elif res['result'] == 'ExpiredToken':
        if session['logged_in'] is True:
            
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
    
            user_reqs_status = db.db.getAllReq(user_id, '/hide-text', '/get-text')
            resp = make_response(user_reqs_status)
            resp.set_cookie('access_token', s_token,max_age= 60 * 60)
    
            return resp
    abort (401)


# Just retrieve count and status
@app.route('/get-all-audio-steg-req', methods = ['POST'])
def get_all_audio_steg_req():
    res = check_token()    
    if res['status-code'] == 200:
        user_reqs_status = db.db.getAllReq(res["result"]["user_id"], '/hide-in-sound', '/get-from-sound')
        try: 
            dict_result = {"count" : user_reqs_status[0][1]}
        except: dict_result = {"count" : 0}
        j_result = json.dumps(dict_result)
        return j_result
    
    elif res['result'] == 'ExpiredToken':
        if session['logged_in'] is True:
            
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
    
            user_reqs_status = db.db.getAllReq(user_id, '/hide-in-sound', '/get-from-sound')
            resp = make_response(user_reqs_status)
            resp.set_cookie('access_token', s_token,max_age= 60 * 60)
    
            return resp
    abort (401)



@app.route('/get-user-requests-status', methods=['POST'])
def get_user_requests_status():
    res = check_token()    
    if res['status-code'] == 200:
        user_reqs_status = db.db.getUserRequestsStatus(res["result"]["user_id"])
        dict_result = {"done":0 , "in queue":0 , "processing":0}
        for i in user_reqs_status:
            dict_result[i[0]] = i[1]
        j_result = json.dumps(dict_result)
        return j_result
    elif res['result'] == 'ExpiredToken':
        if session['logged_in'] is True:
            
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
    
            user_reqs_status = db.db.getUserRequestsStatus(user_id)
            dict_result = {"done":0 , "in queue":0 , "processing":0}
            for i in user_reqs_status:
                dict_result[i[0]] = i[1]
            j_result = json.dumps(dict_result)
            
            resp = make_response(j_result)
            resp.set_cookie('access_token', s_token,max_age= 60 * 60)
    
            return resp
    abort (401)
    

# Signup user
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('/pages/sign-up.html')
    
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
@app.route('/confirm', methods=['GET'])
def _check_confirm():
    res = Email.check_confirm_email()
    if res == 'True':
        res = 'حساب کاربری شما با موفقیت تایید شد. اکنون میتوانید وارد حساب خود شوید.'
    else :
        res = 'لینک تایید معتبر نمی باشد.'
    return res




@app.route('/add', methods=['POST'])
def add():    
    res = check_token_and_add_req_to_db()
    if res["status"] == "accepted":
        send_request.send(res["result"]["request_id"])        # Send request to queue
        res = process.result(res["result"]["request_id"] , res["result"]["user_id"])
    return res


@app.route('/get-size', methods=['POST'])
def get_size():    
    res = check_token_and_add_req_to_db()
    if res["status"] == "accepted":
        send_request.send(res["result"]["request_id"])        # Send request to queue
        res = process.result(res["result"]["request_id"] , res["result"]["user_id"])
    return res    


@app.route('/hide-text', methods=['POST'])
def hide_text():
    res = check_token_and_add_req_to_db()
    if res["status"] == "accepted":
        send_request.send(res["result"]["request_id"])        # Send request to queue
        res = process.result(res["result"]["request_id"] , res["result"]["user_id"])    
    return res


@app.route('/get-text', methods=['POST'])
def get_text():    
    res = check_token_and_add_req_to_db()
    if res["status"] == "accepted":
        send_request.send(res["result"]["request_id"])        # Send request to queue
        res = process.result(res["result"]["request_id"] , res["result"]["user_id"])
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


@app.route('/hide-in-sound' , methods=['POST'])
def hide_in_sound():
    res = check_token_and_add_req_to_db()
    if res["status"] == "accepted":
        send_request.send(res["result"]["request_id"])        # Send request to queue
        res = process.result(res["result"]["request_id"] , res["result"]["user_id"])
    return res


@app.route('/get-from-sound' , methods=['POST'])
def get_from_sound():
    res = check_token_and_add_req_to_db()
    if res["status"] == "accepted":
        send_request.send(res["result"]["request_id"])        # Send request to queue
        res = process.result(res["result"]["request_id"] , res["result"]["user_id"])
    return res


def add_to_db(user_id):    
    type = request.path # ex: /add
    if type == '/hide-text':   
        # Save image        
        img_steg_new_req_img = request.files['img_steg_new_req_img']         
        name_uuid = uuid.uuid4().hex
        img_src = name_uuid + '.png'
        img_steg_new_req_img.save(os.path.join(config.configs["UPLOAD_IMAGE_BEFORE_HIDE"], img_src))        
        msg_steg_newreq_img = request.form['msg_steg_newreq_img']        
        params = {"url" : config.configs["UPLOAD_IMAGE_BEFORE_HIDE"] + img_src , 
                  "text" : msg_steg_newreq_img}
        
    elif type == '/get-text':
        extr_steg_img = request.files['extr_steg_img']
        name_uuid = uuid.uuid4().hex
        img_src = name_uuid + '.png'        
        extr_steg_img.save(os.path.join(config.configs["UPLOAD_IMAGE_BEFORE_HIDE"], img_src))        
        params = {"url" : config.configs["UPLOAD_IMAGE_BEFORE_HIDE"] + img_src }
        
    elif type == '/hide-in-sound':
        msg_newreq_audio = request.form['msg_newreq_audio']        
        # Save Audio        
        audio_newreq_audio = request.files['audio_newreq_audio'] 
        
        wav_output_path = config.configs["UPLOAD_SOUND_BEFORE_HIDE"] + uuid.uuid4().hex + '.wav'
        audio = AudioSegment.from_file(audio_newreq_audio)
        audio.export(wav_output_path , format='wav')
        
        params = {"url" : wav_output_path , 
                  "text" : msg_newreq_audio}
    
    elif type == '/get-from-sound':
        extr_steg_audio = request.files['extr_steg_audio'] 
        
        wav_output_path = config.configs["UPLOAD_SOUND_BEFORE_HIDE"] + uuid.uuid4().hex + '.wav'
        audio = AudioSegment.from_file(extr_steg_audio)
        audio.export(wav_output_path , format='wav')

        params = {"url" : wav_output_path}
        
    else:  
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
    t = threading.Thread(None, get_request.get_requests_from_queue, None, ())
    t.start()
    app.run(host=config.configs['HOST'], port=config.configs['PORT'] , debug=config.configs['DEBUG'])