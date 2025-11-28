# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# URL de connexion PostgreSQL (vient de config.py)
#SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Création du moteur
engine = create_engine(settings.DATABASE_URL, future=True)

# Session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour SQLAlchemy
Base = declarative_base()


# ⚠️ La fonction manquante : get_db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
