import strawberry
from datetime import datetime
from typing  import List


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
    id : int
    author: int
    recipient: int
    content: str
    time_created : datetime
    


@strawberry.type
class LoginSuccess:
    token: str


@strawberry.type
class LoginError:
    message: str

LoginResult = strawberry.union("LoginResult", (LoginSuccess, LoginError))

@strawberry.type
class TokenData:
    id : str
@strawberry.type
class TokenError:
    msg : str

tokenResult = strawberry.union("tokenResult", (TokenData, TokenError))
messageResult = strawberry.union("messageResult", (MessageResponse, LoginError))
