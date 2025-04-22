from bcrypt import hashpw, gensalt, checkpw

def hash_password(password: str):
    salt = gensalt()
    return hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))