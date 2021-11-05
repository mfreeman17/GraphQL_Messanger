from fastapi import FastAPI
from fastapi.responses import JSONResponse
from . import schemas
from strawberry.fastapi import GraphQLRouter
from . import oath2
from .utils import hash_password, verify
import strawberry
from typing  import List
from strawberry.fastapi import GraphQLRouter
from . import models
from strawberry.permission import BasePermission
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


class isAuthenticated(BasePermission):
    message = "User is not authenticated"


@strawberry.type
class Query():

    @strawberry.field
    def getPosts(self)->List[schemas.PostResponse]:
        db = next(get_db())
        posts = db.query(models.Post).all()
        return posts

    @strawberry.field
    def getPostById(self, id :int) -> schemas.PostResponse:
        db = next(get_db())
        post = db.query(models.Post).filter(models.Post.id==id).first()
        return post





@strawberry.type
class Mutation:
    @strawberry.mutation
    def createUser(self, username: str, password: str)-> str:
        db = next(get_db())
        db.add(models.Users(username=username, password= hash_password(password)))
        db.commit()
        return f"created user {username}"

    @strawberry.field
    def login(self, username: str, password: str) -> schemas.LoginResult:

        db = next(get_db())
        user = db.query(models.Users).filter(models.Users.username == username).first()
        if not user or not verify(password, user.password):
            return schemas.LoginError(message="Login Unsuccessful")
        access_token = oath2.create_access_token(data = {"user_id" : user.id})
        return schemas.LoginSuccess(token = access_token)



schema = strawberry.Schema(query=Query, mutation=Mutation)


graphql_app = GraphQLRouter(schema)


app = FastAPI()







app.include_router(graphql_app, prefix="/graphql")
