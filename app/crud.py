from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Post).filter(models.Post.user_id == user_id).offset(skip).limit(limit).all()

def get_all_posts(db: Session):
    return db.query(models.Post).all()

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    new_post = models.Post(**post.dict(), user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def delete_post(db: Session, post: schemas.Post):
    db.delete(post)
    db.commit()
