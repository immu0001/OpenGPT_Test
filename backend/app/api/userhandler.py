from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasicCredentials
from pymongo import MongoClient
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
import secrets
import os

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
users_collection = db["users"]



# Secret key for JWT
secret_key = secrets.token_hex(32)
ALGORITHM = "HS256"
os.environ["SECRET_KEY"] = secret_key

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
    return users_collection.find_one({"username": username})


def authenticate_user(credentials: HTTPBasicCredentials):
    user = get_user(credentials.username)
    if not user or not verify_password(credentials.password, user["password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("auth/login")
async def login(credentials: HTTPBasicCredentials = Depends()):
    user = authenticate_user(credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username or password",
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

class UserCreate(BaseModel):
    username: str
    password: str


# API endpoint for creating new users
@app.post("auth/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    # Check if the username already exists
    existing_user = get_user(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    # Hash the password before saving to the database
    hashed_password = pwd_context.hash(user_data.password)

    # Save the user data to the database
    user_data_db = {
        "username": user_data.username,
        "password": hashed_password
    }
    users_collection.insert_one(user_data_db)

    return {"message": "User created successfully"}