from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail=f"User name: {user.name} already exists.")
    
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User ID: {user_id} not found")
    
    return user

@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_task_for_user(user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    task = crud.create_post(db=db, post=post, user_id=user_id)
    return task


@app.get("/users/{user_id}/posts/", response_model=list[schemas.Post])
def get_tasks_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db=db, user_id=user_id, skip=skip, limit=limit)
    return posts

@app.get("/posts/", response_model=list[schemas.Post])
def get_posts_all(db: Session = Depends(get_db)):
    posts = crud.get_all_posts(db=db)
    return posts
        

# @app.delete("posts/{post_id}", response_model=None)
# def delete_post(post_id: int, db: Session = Depends(get_db)):
#     post = crud.