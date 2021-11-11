from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "$1$q19fea4a$dseqxgotnrcfiur8tzeyik0cx8sd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id = payload.get("user_id")
        if not id:
            raise JWTError("Could not validate credintials")
        return  id
    except JWTError:
            raise JWTError("Could not validate credintials")
def get_user_id(token: str):
    return verify_access_token(token)
