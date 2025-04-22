from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.user import User
from database import get_db
from pydantic import BaseModel
from datetime import datetime
from middlewares.hash_password import hash_password, verify_password
from schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()

# crear usuario
@router.post("/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# info de todos los usuarios
@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users

# obtener info de los usuarios que coincidan con q en cualquier parametro publico
@router.get("/searchBy", response_model=list[UserResponse])
async def search_users(q: str, db: Session = Depends(get_db)):
    users = db.query(User).filter( #busca todo lo que coincida con q
        (User.username.ilike(f"%{q}%")) | 
        (User.first_name.ilike(f"%{q}%")) | 
        (User.last_name.ilike(f"%{q}%")) | 
        (User.email.ilike(f"%{q}%"))
    ).all()
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    return users

# obtener info de un solo usuario
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# modificar usuario
@router.put("/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.username:
        db_user.username = user_update.username
    if user_update.first_name:
        db_user.first_name = user_update.first_name
    if user_update.last_name:
        db_user.last_name = user_update.last_name
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.password = hash_password(user_update.password)

    db.commit()
    db.refresh(db_user)
    return db_user

# modificar usuario parcialmente
@router.patch("/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")    
    if user_update.username not in [None, ""]:
        db_user.username = user_update.username
    if user_update.first_name not in [None, ""]:
        db_user.first_name = user_update.first_name
    if user_update.last_name not in [None, ""]:
        db_user.last_name = user_update.last_name
    if user_update.email not in [None, ""]:
        db_user.email = user_update.email
    if user_update.password not in [None, ""]:
        db_user.password = hash_password(user_update.password)
    db.commit()
    db.refresh(db_user)
    return db_user


# eliminar un usuario
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}
