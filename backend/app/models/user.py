from pydantic import BaseModel

class UserModel(BaseModel):
    username: str
    password: str

class UserInDb(UserModel):
    hashed_password: str