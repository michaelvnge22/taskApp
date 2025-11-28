from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import LoginSchema, UserCreate, UserResponse, Token
from app.models import User
from app.database import get_db

from app.core.security import (hashed_password, verify_password, create_access_token)

router = APIRouter(prefix="/auth", tags=["Auth"])

# ------------------------------
# REGISTER
# ------------------------------

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # utilise la colonne 'hashed_password' (comme dans app/models.py)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ------------------------------
# LOGIN
# ------------------------------

@router.post("/login", response_model=Token)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Email incorrect")

    # vérifier avec user.hashed_password
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Mot de passe incorrect")

    # Création du token sécurisé (sub = id)
    access_token = create_access_token({"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
