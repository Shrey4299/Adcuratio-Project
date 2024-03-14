# test_api.py
import json
import requests
from faker import Faker

# Define the base URL of your API
BASE_URL = "http://127.0.0.1:8000/api/users"

# Define the headers to be sent with the request

# Create a Faker instance
faker = Faker()


def test_sample_endpoint():
    # Send a GET request to the API endpoint with the specified headers
    token_string = "dfsd"
    response = requests.get(
        BASE_URL + "/sample/",
        headers={
            "token": token_string,
        },
    )
    print(response.text)  # or response.content if you prefer bytes

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Parse the JSON response
    response_data = json.loads(response.text)

    # Assert on the response body content
    assert "token" in response_data
    assert response_data["token"] == token_string


def test_signin_endpoint():
    # Define the data to be sent in the POST request
    signin_data = {"email": "user@example.com", "password": "string"}

    # Send a POST request to the API endpoint with the specified data and headers
    response = requests.post(
        BASE_URL + "/signin",
        json=signin_data,
        headers={"Content-Type": "application/json"},
    )

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Parse the JSON response
    response_data = response.json()

    # Assert on the response body content
    assert response_data["success"] == True
    assert response_data["message"] == "User signed in successfully"
    assert "data" in response_data
    assert len(response_data["data"]) == 1
    assert "jwt" in response_data["data"][0]
    assert response_data["status_code"] == 200


def r_signup_endpoint():
    # Generate random data for the signup request
    signup_data = {
        "name": faker.name(),
        "email": faker.email(),
        "phone_number": faker.phone_number(),
        "password": faker.password(
            length=10
        ),  # You can adjust the password length as needed
    }

    # Send a POST request to the API endpoint with the specified data and headers
    response = requests.post(
        BASE_URL + "/signup",
        json=signup_data,
    )

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 201

    # Parse the JSON response
    response_data = response.json()

    # Assert on the response body content
    assert response_data["success"] == True
    assert response_data["message"] == "User created successfully"
    assert "data" in response_data
    assert len(response_data["data"]) == 1
    assert response_data["status_code"] == 201


def test_signup_same_email_endpoint():
    # Define the data to be sent in the POST request
    signup_data = {
        "name": "string3",
        "email": "user@example3.com",
        "phone_number": "string37",
        "password": "string3",
    }

    # Send a POST request to the API endpoint with the specified data and headers
    response = requests.post(
        BASE_URL + "/signup",
        json=signup_data,
    )

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 409

    # Parse the JSON response
    response_data = response.json()

    # Assert on the response body content
    assert response_data["detail"] == "User with this email already exists"
    assert len(["data"]) == 1


def test_signup_same_phone_endpoint():
    # Define the data to be sent in the POST request
    signup_data = {
        "name": "string3",
        "email": "user@example37.com",
        "phone_number": "string3",
        "password": "string3",
    }

    # Send a POST request to the API endpoint with the specified data and headers
    response = requests.post(
        BASE_URL + "/signup",
        json=signup_data,
    )

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 409

    # Parse the JSON response
    response_data = response.json()

    # Assert on the response body content
    assert response_data["detail"] == "User with this phone number already exists"
    assert len(["data"]) == 1
