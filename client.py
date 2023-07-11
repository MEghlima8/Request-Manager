import requests
import threading

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

num_requests = 10
send_multiple_requests(url, data, headers, num_requests)
