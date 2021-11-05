from fastapi import FastAPI, HTTPException, Depends
from .schemas import Post, PostResponse
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.sql import text
import strawberry
from typing  import List
from strawberry.fastapi import GraphQLRouter
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


@strawberry.type
class Query():

    @strawberry.field
    def getPosts(self)->List[PostResponse]:
        db = next(get_db())
        posts = db.query(models.Post).all()
        return posts

    @strawberry.field
    def getPostById(self, id :int) -> PostResponse:
        db = next(get_db())
        post = db.query(models.Post).filter(models.Post.id==id).first()
        return post


@strawberry.type
class Mutation:
    @strawberry.mutation
    def createPost(self, title: str, content: str) -> Post:
        post = Post(title, content)
        db = next(get_db())
        db.add(models.Post(title=title, content= content))
        db.commit()
        return post

schema = strawberry.Schema(query=Query, mutation=Mutation)


graphql_app = GraphQLRouter(schema)


app = FastAPI()






"""
PostResponse(
    id = post[0]
    title = post[1]
    content = post[2]
    time_created = post[3]
)
@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return posts

@app.post("/posts", status_code = 201)
def create_posts(post: Post):
    sql = "INSERT INTO posts (title, content) VALUES (%s, %s)"
    vals = (post.title, post.content)
    cursor.execute(sql, vals)
    mydb.commit()

    return post



@app.get("/posts/{id}")
def get_post_by_id(id: int):
        cursor.execute(f"SELECT * FROM posts WHERE id = {str(id)}")
        post = cursor.fetchone()
        if not post:
            raise HTTPException(status_code = 404,
            detail = "post not found")

        return post

@app.delete("/posts/{id}", status_code = 204)
def delete_post(id : int):
    cursor.execute(f"DELETE FROM posts WHERE id = {str(id)}")
    success = cursor.fetchone()
    if not success:
        raise HTTPException(status_code = 404,
        detail = "post not found")
    mydb.commit()
"""
app.include_router(graphql_app, prefix="/graphql")
