from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from  .import models
from .database import engine ,SessionLocal

models.Base.metadata.create_all(bind = engine) 

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title : str
    author: str
    synopsis: str
    published_on: str


while True:    
    try:
        conn = psycopg2.connect(host= 'localhost', database= 'project_1', user= 'postgres',
        password= 'Jaredcaleb#1', cursor_factory=RealDictCursor)   
        cursor = conn.cursor()
        print("Database connection was succesfull!!!")
        break
    except Exception as error:
        print('Connecting to Database failed')
        print("Error: ", error)
        time.sleep(2)
    

my_posts = [{"title": "title of Book 1", "content": "content of book 1", "id": 7}, {
    "title": "title of Book 2", "content": "content of book 2",  "id": 3}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get_db("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return{"status": "success"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM books """)
    books = cursor.fetchall()
    return {"data": books}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(book : Post):
    cursor.execute("""INSERT INTO books (title, author, synopsis, published_on ) VALUES (%s, %s, %s, %s) RETURNING
     * """,
                (book.title, book.author, book.synopsis, book.published_on))

    new_book = cursor.fetchone()

    conn.commit()

    return  {"data": new_book}

@app.get("/post/{id}")
def get_posts(id: int):
    cursor.execute("""SELECT * from books WHERE id2 = %s """, (str(id)))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail = "post was not found :)" )
    return {"post_detail": book}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM books WHERE id2 = %s returning * """, (str(id)))
    deleted_book = cursor.fetchone()
    conn.commit()
     
    if deleted_book== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"post with id: {id} does not exist")

    return {'message': "post was succefully deleted"}



@app.put("/post/{id}")
def update_post(id: int, book: Post):
    cursor.execute("""UPDATE books SET title = %s, author = %s, synopsis = %s, published_on = %s WHERE id2 = %s RETURNING * """, 
    (book.title, book.author, book.synopsis, book.published_on ,(str(id))))
    
    updated_post = cursor.fetchone()
    
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"post with id: {id} does not exist")

    
    return  {"data": updated_post}