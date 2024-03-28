## backend

## Authentication and Authorization

Authentication and authorization are managed through designated APIs provided for user verification and access control.

## Shell Environment Tests:
### Registration of a new User Account

To register in the application:
Note: All the fields are required in request Payload

python
import requests
requests.post(
    'http://127.0.0.1:8100/auth/create_user',
    json={
        "username": "imransm001",
        "password": "Test_Password_IM123"
    },
    headers={"content-type": "application/json"}
)



* If user successfully registered:

shell
b'{"message": "User created successfully"}'
status_code = 200

* If user registration failed fue to username conflict:

shell
b'{"detail":{"message":"Username already exists"}}'
status_code = 400


### Login

To authenticate User and to get the JWT token:
fields Required: username, password

python
import requests
requests.post(
    'http://127.0.0.1:8100/auth/login',
    json={
        "username": "imran_test",
        "password": "Test_Password_IM123"
    },
    headers={"content-type": "application/json"}
).content



* Scenario: Successful authentication

shell
b'{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJteXVzZXJuYW1lIiwiZXhwIjoxNjEwNjc3NTYzfQ.rCGejIusVbTEnCZ0kZP6Xjb8mSCfHlV-i8oSKzvAMKs", "token_type": "bearer"}'

* else
shell
b'{"message":"Invalid username or password"}'
status_code=404


## Setup the Mongo DB Database by pulling image from DockerHub:

DockerHub Mongodb: