from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Post(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String , nullable = False)
    author = Column(String, nullable = False)
    synopsis = Column(String, nullable = False)
    published_on: Column(Boolean, default= True )