from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from .models import Base, Individu, Relation
from .schemas import IndividuSchema, RelationSchema
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from .models import Base

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware


# Autoriser toutes les origines
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Création des tables automatiquement
Base.metadata.create_all(bind=engine)

# Dépendance pour la session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes API
@app.post("/individus/")
def create_individu(individu: IndividuSchema, db: Session = Depends(get_db)):
    db_individu = Individu(
        first_name=individu.first_name,
        last_name=individu.last_name,
        birth_date=individu.birth_date,
        death_date=individu.death_date,
    )
    db.add(db_individu)
    db.commit()
    db.refresh(db_individu)
    return db_individu

@app.get("/individus/")
def get_individus(db: Session = Depends(get_db)):
    return db.query(Individu).all()

@app.post("/relations/")
def create_relation(relation: RelationSchema, db: Session = Depends(get_db)):
    parent = db.query(Individu).filter(Individu.id == relation.parent_id).first()
    child = db.query(Individu).filter(Individu.id == relation.child_id).first()

    if not parent or not child:
        raise HTTPException(status_code=404, detail="Parent or child not found")

    db_relation = Relation(
        parent_id=relation.parent_id,
        child_id=relation.child_id,
        relation_type=relation.relation_type,
    )
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation

@app.get("/arbre/")
def get_arbre(db: Session = Depends(get_db)):
    individus = db.query(Individu).all()
    arbre = []
    for individu in individus:
        arbre.append({
            "id": individu.id,
            "first_name": individu.first_name,
            "last_name": individu.last_name,
            "birth_date": str(individu.birth_date),
            "death_date": str(individu.death_date) if individu.death_date else None,
            "parents": [relation.parent_id for relation in individu.parents]
        })
    return arbre