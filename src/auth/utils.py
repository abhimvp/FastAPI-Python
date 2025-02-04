# define alogorithems we are going to use to hash our password
import uuid
import logging
from datetime import timedelta, datetime
from itsdangerous import URLSafeTimedSerializer
from passlib.context import CryptContext
import jwt
from src.config import Config

passwd_context = CryptContext(schemes=["bcrypt"])

# seconds
ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}
    payload["user"] = user_data
    expiry_time = datetime.utcnow() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["exp"] = expiry_time.timestamp()  # Convert to Unix timestamp
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )
    return token


# decode the token
def decode_token(token: str):
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


# USER vERIFICATION

serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET, salt="email-configuration"
)


def create_url_safe_token(data: dict):
    """Serialize a dict into a URLSafe token"""

    token = serializer.dumps(data)

    return token


def decode_url_safe_token(token: str):
    """Deserialize a URLSafe token to get data"""
    try:
        token_data = serializer.loads(token)

        return token_data

    except Exception as e:
        logging.error(str(e))
