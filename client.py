import requests
import threading

def send_request(url, data, headers):
    response = requests.post(url, json=data, headers=headers)
    print(f"Response from {url}: {response.text}")


def send_multiple_requests(url, data, headers, num_requests):
    for _ in range(num_requests):
        t = threading.Thread(target=send_request, args=(url, data, headers))
        t.start()


url = 'http://localhost:5000/get-result'
# data = {"params":{"num1": 1000, "num2": 3100}}
data = {"request_id": "2403"}
headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1vaGFtbWFkIiwiZXhwaXJhdGlvbl90aW1lIjoxNjg5MDY4NDgyfQ.YNeLBjBNmG3ohGp8-RIu7UAhGrYWIiM6MSO83D0DuNg'}

num_requests = 1
send_multiple_requests(url, data, headers, num_requests)
