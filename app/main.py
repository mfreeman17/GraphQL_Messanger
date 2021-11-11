from fastapi import FastAPI, Request, Response, BackgroundTasks, WebSocket
from . import schemas
from strawberry.fastapi import GraphQLRouter
from jose import JWTError
from strawberry.types import Info
from . import oath2
from .utils import hash_password, verify
import strawberry
from typing  import List
from . import models
from strawberry.permission import BasePermission
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


class isAuthenticated(BasePermission):
    message = "User is not authenticated"


async def get_context(background_tasks: BackgroundTasks = None, request: Request = None, ws: WebSocket = None, response: Response = None):
    return {"request": request, "background_tasks": background_tasks, "response": response}


@strawberry.type
class Query():

    @strawberry.field
    def getYourMessages(self, jwt_token: str)->List[schemas.MessageResponse]:
        try:
            user_id = oath2.get_user_id(jwt_token)
        except:
            raise JWTError("Could not validate token")
        db = next(get_db())
        print(user_id)
        messages = db.query(models.Message).filter(models.Message.recipient==user_id).all()
        return messages





@strawberry.type
class Mutation:
    @strawberry.mutation
    def createUser(self, username: str, password: str)-> str:
        db = next(get_db())
        db.add(models.Users(username=username, password= hash_password(password)))
        db.commit()
        return f"created user {username}"

    @strawberry.mutation
    def sendMessage(self, recipientUsername: str,  message: str, jwt_token:str,) -> str:
        try:
            user_id = oath2.get_user_id(jwt_token)
        except:
            raise JWTError("Could not validate token")
        db = next(get_db())
        recipient_id = db.query(models.Users).filter(models.Users.username == recipientUsername).first().id
        #gets the id of the recipient from the username
        if not recipient_id:
             # if could not  recipient
            return "could not find recipient"
        db.add(models.Message(author=user_id, recipient=recipient_id, content=message))
        db.commit()
        return "message sent"

    @strawberry.field
    def login(self, username: str, password: str, info: Info ) -> schemas.LoginResult:
        db = next(get_db())
        user = db.query(models.Users).filter(models.Users.username == username).first()
        if not user or not verify(password, user.password):
            return schemas.LoginError(message="Login Unsuccessful")
        access_token = oath2.create_access_token(data = {"user_id" : user.id})
        return schemas.LoginSuccess(token = access_token, tokenType = "bearer")



schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app =  GraphQLRouter(schema, context_getter=get_context)
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
