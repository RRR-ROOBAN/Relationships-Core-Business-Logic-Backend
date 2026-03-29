from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.user import UserCreate
from services import auth_service
from schemas.user import UserLogin
from fastapi import HTTPException

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return auth_service.create_user(db, user)




# @router.post("/login")
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     result = auth_service.login_user(db, user)

#     if not result:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     return result

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth_service.create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}