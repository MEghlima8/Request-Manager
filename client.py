import requests
import threading
import argparse

parser = argparse.ArgumentParser()

def add_argument_parser():
    arguments = [
        ['--route', 'route -> ex: /add'],
        ['--num1', 'first number'],
        ['--num2', 'second number'],
        ['--reqid', 'your request id'],
        ['--token', 'token (JWT)'],
        ['--username', 'your username'],
        ['--password', 'your password'],
        ['--confirm_link', 'confirm link'],
        ['--email', 'your email'],
        ['--size', 'requests size'],
        ['--host', 'host'],
        ['--port', 'port'],
        ['--url', 'your image url'],
        ['--text', 'your text to hide in image '],
    ]
    
    # ex: '--text', 'your text to hide in image '
    for arg,help in arguments:
      parser.add_argument(arg, help=help)  
    return


def send_request(url, data, headers):
    response = requests.post(url, json=data, headers=headers)
    print(response.text)


def send_multiple_requests(data, size, route, host, port, headers=None):
    url = 'http://%s:%s/%s' % (host, port, route)
    # data = {"params":{"num1": 200, "num2": 3100}} 
    
    for _ in range(size):
        t = threading.Thread(target=send_request, args=(url, data, headers))
        t.start()


# add
def add_route(req_size,host,port):
    args = parser.parse_args()
    data = {"params":{"num1": int(args.num1), "num2": int(args.num2)}} 
    headers = {'Authorization': args.token}
    send_multiple_requests(data, req_size, 'add', host, port, headers)
    
        
# get result    
def get_result_route(req_size, host,port):
    args = parser.parse_args()
    data = {"request_id":args.reqid}
    headers = {'Authorization': args.token}
    send_multiple_requests(data, req_size, 'get-result', host, port, headers)
    
    
# sign in
def signin_route(req_size, host, port):
    args = parser.parse_args()
    data = {"username": args.username,"password": args.password}
    send_multiple_requests(data, req_size, 'signin', host, port) 

# confirm link
def confirm_route(req_size, host, port):
    args = parser.parse_args()
    data = {"confirm_link": args.confirm_link}
    send_multiple_requests(data, req_size, 'confirm', host, port)

# sign up
def signup_route(req_size, host, port):
    args = parser.parse_args()
    data = {"username": args.username,"password": args.password,"email": args.email}
    send_multiple_requests(data, req_size, 'signup', host, port)

# hide text
def hide_text(req_size, host, port):
    args = parser.parse_args()
    data = {"params":{"url": args.url, "text": args.text}} 
    headers = {'Authorization': args.token}
    send_multiple_requests(data, req_size, 'hide-text', host, port, headers)
    

# get text
def get_text(req_size, host, port):
    args = parser.parse_args()
    data = {"params":{"url": args.url}} 
    headers = {'Authorization': args.token}
    send_multiple_requests(data, req_size, 'get-text', host, port, headers)    
    
    
def main():
    add_argument_parser()
    
    host = parser.parse_args().host
    port = parser.parse_args().port
    route = parser.parse_args().route
    try:
        req_size = int(parser.parse_args().size)
    except:
        req_size = 1
        
    if host is None:
        host = 'localhost'
    if port is None:
        port = '5000' 
    if req_size is None or req_size < 1 :
        req_size = 1
    
    if route == 'add' :
        add_route(req_size, host,port)
        
    elif route == 'get-result' :
        get_result_route(req_size, host, port)
    
    elif route == 'signin':
        signin_route(req_size, host, port)
    
    elif route == 'confirm':
        confirm_route(req_size, host, port)
        
    elif route == 'signup':
        signup_route(req_size, host, port)
        
    elif route == 'hide-text':
        hide_text(req_size, host, port)
    
    elif route == 'get-text':
        get_text(req_size, host, port)
    
    else:
        print("Invalid Route")
        
main()