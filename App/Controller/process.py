from App.Controller import db_postgres_controller as db
from datetime import datetime
import json


def process(req_id):
    
    query = "INSERT INTO process (req_id, status) VALUES(%s , %s)"
    req_info = db.db.execute(query, (req_id, 'processing'))
    
    # start time
    start_time = datetime.now()
    
    # Get route and params
    query = "SELECT * FROM request WHERE id=%s"
    req_info = db.db.execute( query , (req_id,)).fetchall()
    
    route = req_info[0][2]
    if route == '/add':
        result = add(req_info[0])
    
    # end time
    end_time = datetime.now()
    
    # add request to process database
    query = "UPDATE process set start_time=%s, end_time=%s, result=%s, status='done' WHERE req_id=%s"
    req_info = db.db.execute(query, (start_time, end_time, result, req_id))
    
    return 'true'


def add(info):
    param1 = info[3]["num1"]
    param2 = info[3]["num2"]
    
    res = {"result": param1 + param2}
    res = json.dumps(res)
    return res


def result(s_req_id,user_id):
    
    # Get request process result if there is in process table
    query = "SELECT result,status FROM request INNER JOIN process ON request.id=process.req_id WHERE request.user_id=%s AND process.req_id=%s"
    res = db.db.execute(query, (user_id, s_req_id)).fetchall()
    
    if res == []:
        # There is no the processed request in process table
        
        # Now , check is there in request table or not
        query = "SELECT * FROM request WHERE user_id=%s AND id=%s"
        res = db.db.execute(query, (user_id, s_req_id)).fetchall()
        if res == []:
            # There is no the request in request table
            res = {"status":"not accepted" , "result":"request id is wrong"}
        else:
            res = {"status":"accepted" , "result":"request is in queue" , "request_id":res[0][0]}
        return res
    
    elif res[0][0] is None or res[0][1] != 'done' :
        return 'None'

    # There is process in process db table
    res = res[0][0]
    return res