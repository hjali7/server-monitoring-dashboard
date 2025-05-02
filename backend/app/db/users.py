from passlib.context import CryptContext

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": "$2b$12$B/1H3v/inQ7wN0iWkOQ1X.6a1Q8N4gQWc9bOq6q8g.9qP3y3G9Q8K"  # password: admin
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(username: str):
    user = fake_users_db.get(username)
    if user:
        return user
    return None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)