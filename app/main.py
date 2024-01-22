from fastapi import FastAPI, Response, status, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from . import models
from .database import engine, get_db
from .schemas import PostCreate, PostResponse, UserCreate, UserResponse
from .exception import MyException
from fastapi.responses import JSONResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(MyException)
async def my_exception_handler(request: Request, exc: MyException):
    return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content={"message": f"{exc.name} already exists!!!!" })


@app.get("/")
def root():
    return {"message": "Hello World!!!"}


@app.get("/posts/posts")
def posts(db: Session = Depends(get_db)):
    print(db.query(models.Posts))
    print(db.query(models.Posts).join(models.Users))
    all_posts = db.query(models.Posts).all()
    return all_posts


@app.get("/posts/{id}", response_model=PostResponse)
def get_post(input_id: int, db: Session = Depends(get_db)):
    one_post = db.query(models.Posts).filter(models.Posts.id == input_id).first()
    if one_post:
        return one_post
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        f" post with Id {input_id} is not found")


@app.post("/posts/create_posts",
          status_code=status.HTTP_201_CREATED,
          response_model=PostResponse)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    new_posts = models.Posts(**payload.model_dump())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@app.delete("/posts/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_to_be_deleted = db.query(models.Posts).filter(models.Posts.id == id)

    if post_to_be_deleted.first():
        post_to_be_deleted.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f" post with Id {id} cannot be deleted")


@app.put("/posts/update/{id}", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def update_post(post: PostCreate, id: int, db: Session = Depends(get_db)):
    post_to_be_updated = db.query(models.Posts).filter(models.Posts.id == id)

    if post_to_be_updated.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f" post with Id {id} cannot be Found")

    post_to_be_updated.update(post.model_dump())
    db.commit()
    return post_to_be_updated.first()



@app.post("/users/create_user",
          status_code=status.HTTP_201_CREATED,
          response_model=UserResponse|str)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):

    all_users = db.query(models.Users).all()
    if all_users:
        for user in all_users:
            if user.email_id == payload.email_id:
                raise MyException(name=user.email_id)
    new_user = models.Users(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/users", response_model=List[UserResponse])
def posts(db: Session = Depends(get_db)):
    all_users = db.query(models.Users).all()
    return all_users
