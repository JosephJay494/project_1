from pydantic import BaseModel



class Post(BaseModel):
    title : str
    author: str
    synopsis: str
    published_on: str