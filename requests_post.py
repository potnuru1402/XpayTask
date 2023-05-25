import requests

url = "http://127.0.0.1:6451/users/"

data = {
    "full_name": "aqqoaok144",
    "email": "aqqoaok133@example.com",
    "password": "aqm*!*password",
    "phone": "116809021345",
    "profile_picture": "image1.jpg"
}

response = requests.post(url, json=data)

# Check the response status code
if response.status_code == 200:
    print("Data sent successfully.")
if response.status_code == 422:
    error_message = response.json().get("detail")
    print(f"Validation Error: {error_message}")
else:
    print("Failed to send data.")
