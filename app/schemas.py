import strawberry
from datetime import datetime


@strawberry.type
class UserResponse:
    id : int
    username: str
    password: str
    time_created : datetime

@strawberry.type
class Token:
    access_token : str
    token_type : str

@strawberry.type
class MessageResponse:
    author: int
    content: str
    time_created : datetime



@strawberry.type
class LoginSuccess:
    token: str
    tokenType : str


@strawberry.type
class LoginError:
    message: str
LoginResult = strawberry.union("LoginResult", (LoginSuccess, LoginError))
