import requests

url = "http://localhost:8000/api/v1/casts"
data = {
    "name": "Harsh",
    "nationality": "Indian"
   
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=data, headers=headers)

print(response.content)
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")
