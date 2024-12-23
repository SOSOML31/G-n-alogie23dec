from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuration de la base de données PostgreSQL
DATABASE_URL = "postgresql://postgres:931752@localhost:5432/genealogie"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Base pour les modèles SQLAlchemy
Base = declarative_base()

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)