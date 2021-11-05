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
class PostResponse:
    id : int
    title: str
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
