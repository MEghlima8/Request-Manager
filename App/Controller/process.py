from App.Controller import db_postgres_controller as db
from datetime import datetime
import json


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
    
    # end time
    end_time = datetime.now()
    
    db.db.updateProcess(start_time, end_time, result, req_id)
    return 'true'


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
        res = {"status":"accepted" , "result":"not processed yet" , "request_id":s_req_id , "status-code":202}
        return res

    # There is process in process db table
    res = {"status":"done" , "result":res[0][0]["result"] , "status-code":200 , "request_id":s_req_id}
    
    return res