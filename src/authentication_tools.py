import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv

# Define your secret key
SECRET_KEY = os.environ["SECRET_KEY"]


# Function to generate a token
def generate_token(username, expiration_duration=timedelta(days=3650)):
    # Define the payload (data to be encoded in the token)
    payload = {
        "sub": username,  # Subject (usually the user ID)
        "exp": datetime.now(timezone.utc) + expiration_duration,  # Expiration time
    }
    # Generate the token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token


# Function to validate a token
def validate_token(token):
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Check if the token is expired
        expiration_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        if expiration_time < datetime.now(timezone.utc):
            return False, "Token has expired"

        # If no exceptions are raised during decoding and expiration check,
        # the token is considered valid
        return True, "Token is valid", payload["sub"], expiration_time

    except jwt.ExpiredSignatureError:
        # Token has expired
        return False, "Token has expired"
    except jwt.InvalidTokenError:
        # Token is invalid
        return False, "Invalid token"


if __name__ == "__main__":
    # Generate a token
    username = input("username for token:")
    token = generate_token(username)
    print("Generated Token:", token)
