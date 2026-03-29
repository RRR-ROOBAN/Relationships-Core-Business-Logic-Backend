from models.user import User
from passlib.context import CryptContext
from core.security import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_user(db, user):
    hashed_pw = hash_password(user.password)

    db_user = User(
        username=user.username,
        password=hashed_pw
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



def authenticate_user(db, username, password):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user

def login_user(db, user_data):
    user = authenticate_user(db, user_data.username, user_data.password)

    if not user:
        return None

    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}