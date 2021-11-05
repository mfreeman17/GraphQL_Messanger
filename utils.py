from passlib.context import CryptContext
#hashing algorithm used
pwd_context = CryptContext("md5_crypt")
def hash_password(password):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    
