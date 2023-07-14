from App.Controller import db_postgres_controller as db
from datetime import datetime
import json
import uuid
from stegano import lsb
import os
from App import config
import requests 
from PIL import Image
from io import BytesIO
import mimetypes


def process(req_id):
    
    # Insert to request process table
    db.db.insertToProcess(req_id)
    
    # start time
    start_time = datetime.now()
    
    # Get route and params
    req_info = db.db.getReqInfo(req_id)
    
    route = req_info[0][2]
    if route == '/add':
        result = add(req_info[0])
    elif route == '/hide-text':
        result = hide_text(req_info[0])
    elif route == '/get-text':        
        result = get_text(req_info[0])
    elif route == '/get-size':
        result = get_size(req_info[0])
    
    # end time
    end_time = datetime.now()
    
    db.db.updateProcess(start_time, end_time, result, req_id)
    return 'true'


def get_size(info):
    images_folder = config.configs["UPLOAD_IMAGE_AFTER_HIDE"]
    imgs_name = db.db.getImagesName(info[0])
    total_size = 0
    
    for file_dir in imgs_name:
        filename = file_dir[0]["result"]["url"].split('/')[-1]
        file_path = os.path.join(images_folder, filename)
        total_size += os.path.getsize(file_path)
        
    res = {"result":{"total_size":total_size}}
    
    res = json.dumps(res)
    return res


def get_text(info):
    try:
        image_url = info[3]["url"]
        # Get image from URL
        response = requests.get(image_url)
        image_content = response.content
        image = Image.open(BytesIO(image_content))    
    except:
        image_url = info[3]["path"]
        image = Image.open(image_url)
    
    try:
        text = lsb.reveal(image)
        res = {"result":{"extracted text":text}}        
    except:        
        res = {"result":"this images doesn't have any hidden text"}
    res = json.dumps(res)
    return res



def hide_text(info):
    text = info[3]["text"]
    try:
        image_url = info[3]["url"]
        # Get image from URL
        response = requests.get(image_url)
        mime_type = response.headers.get("content-type")
        image_content = response.content
        image = Image.open(BytesIO(image_content))    
    except:
        image_path = info[3]["path"]
        image = Image.open(image_path)
        mime_type, _ = mimetypes.guess_type(image_path)
    
    img_uuid = uuid.uuid4().hex
    
    # Save user image with random name generated by uuid -> ex: dafhiuqcnjnac.jpg
    img_name = img_uuid + '.' + mime_type.split('/')[1]
    image.save(os.path.join(config.configs["UPLOAD_IMAGE_BEFORE_HIDE"], img_name))
    
    # Put text in image
    secret_img = lsb.hide(image, text, auto_convert_rgb=True)
    
    # Save new image with random name generated by uuid
    secret_img.save(os.path.join(config.configs["UPLOAD_IMAGE_AFTER_HIDE"], img_name))
    
    os.remove(os.path.join(config.configs["UPLOAD_IMAGE_BEFORE_HIDE"], img_name))
    
    res = {"result":{"url":f'http://127.0.0.1:5000/static/images/afterHide/{img_name}'}}
    res = json.dumps(res)
    return res


def add(info):
    param1 = info[3]["num1"]
    param2 = info[3]["num2"]
    
    res = {"result": param1 + param2}
    res = json.dumps(res)
    return res


def result(s_req_id,user_id):
    
    # Get request process result if there is in process table
    res = db.db.getReqProcessRes(user_id, s_req_id)
    
    if res == []:
        # There is no the processed request in process table
        
        # Now , check is there in request table or not
        res = db.db.checkIsInReqTB(user_id, s_req_id)
        
        if res == []:
            # There is no the request in request table
            res = {"status":"not accepted" , "result":"request id is wrong" , "status-code":400}
        else:
            res = {"status":"accepted" , "result":"request is in queue" , "request_id":res[0][0] , "status-code":202}
        return res
    
    elif res[0][0] is None or res[0][1] != 'done' :
        # request accepted but not processed yet 
        res = {"status":"accepted" , "result":"processing" , "request_id":s_req_id , "status-code":202}
        return res

    # There is process in process db table
    res = {"status":"done" , "result":res[0][0]["result"] , "status-code":200 , "request_id":s_req_id}
    
    return res