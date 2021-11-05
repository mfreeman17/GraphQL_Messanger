import strawberry
from typing  import Optional
from datetime import datetime
@strawberry.type
class Post:
    title: str
    content: str
    rating : Optional[int] = None

@strawberry.type
class PostResponse:
    id : int
    title: str
    content: str
    time_created : datetime
