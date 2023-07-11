import requests
import threading
import argparse


parser = argparse.ArgumentParser()

# Configes
# parser.add_argument('--host', type=int, help='host')
# parser.add_argument('--port', type=int, help='port')

parser.add_argument('--route', type=str , help='route -> ex: /add')
route = parser.parse_args().route

# /add
if route == '/add' :
    print('/add')
    parser.add_argument('--num1', type=int, help='first number')
    parser.add_argument('--num2', type=int, help='second number')
    parser.add_argument('--token', type=int, help='token (JWT)')
    # Get args
    args = parser.parse_args()
    num1 = args.num1
    num2 = args.num2
    token = args.token
    
elif route == 'get-result' :
    parser.add_argument('--reqid', type=int, help='your request id')
    parser.add_argument('--token', type=int, help='token (JWT)')
    # Get args
    args = parser.parse_args()
    request_id = args.reqid
    token = args.token
    
elif route == '/signin':
    parser.add_argument('--username', type=int, help='your username')
    parser.add_argument('--password', type=int, help='your password')
    # Get args
    args = parser.parse_args()
    username = args.username
    password = args.password


elif route == '/confirm':
    pass


elif route == '/signup':
    pass


parser.add_argument('--token', type=int, help='token (JWT)')






def send_request(url, data, headers):
    response = requests.post(url, json=data, headers=headers)
    print(response.text)


def send_multiple_requests(url, data, headers, num_requests):
    for _ in range(num_requests):
        t = threading.Thread(target=send_request, args=(url, data, headers))
        t.start()


url = 'http://localhost:5000/add'
data = {"params":{"num1": 200, "num2": 3100}}
# data = {"request_id": "2555"}
headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1vaGFtbWFkIiwiZXhwaXJhdGlvbl90aW1lIjoxNjg5MDY4NDgyfQ.YNeLBjBNmG3ohGp8-RIu7UAhGrYWIiM6MSO83D0DuNg'}

# num_requests = 10
# send_multiple_requests(url, data, headers, num_requests)
