from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from .models import Base, Individu, Relation
from .schemas import IndividuSchema, RelationSchema
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

# **1. Création d'un individu**
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

# **2. Récupération de tous les individus**
@app.get("/individus/")
def get_individus(db: Session = Depends(get_db)):
    return db.query(Individu).all()

# **3. Création d'une relation**
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

# **4. Visualisation de l'arbre généalogique**
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

# **5. Ajouter un individu avec validation**
@app.post("/ajouter", response_model=IndividuSchema)
def ajouter_individu(individu: IndividuSchema, db: Session = Depends(get_db)):
    if individu.parents:
        parents = db.query(Individu).filter(Individu.id.in_(individu.parents)).all()
        for parent in parents:
            if individu.birth_date < parent.birth_date:
                raise HTTPException(status_code=400, detail="Un enfant ne peut pas être né avant ses parents.")
    new_individu = Individu(
        first_name=individu.first_name,
        last_name=individu.last_name,
        birth_date=individu.birth_date,
        death_date=individu.death_date
    )
    db.add(new_individu)
    db.commit()
    db.refresh(new_individu)
    return new_individu

# **6. Modification d'un individu**
@app.put("/modifier/{individu_id}")
def modifier_individu(individu_id: int, individu: IndividuSchema, db: Session = Depends(get_db)):
    db_individu = db.query(Individu).filter(Individu.id == individu_id).first()
    if not db_individu:
        raise HTTPException(status_code=404, detail="Individu non trouvé")
    db_individu.first_name = individu.first_name or db_individu.first_name
    db_individu.last_name = individu.last_name or db_individu.last_name
    db_individu.birth_date = individu.birth_date or db_individu.birth_date
    db_individu.death_date = individu.death_date or db_individu.death_date
    db.commit()
    db.refresh(db_individu)
    return {"message": "Individu modifié avec succès", "individu": db_individu}

# **7. Suppression d'un individu**
@app.delete("/supprimer/{individu_id}")
def supprimer_individu(individu_id: int, db: Session = Depends(get_db)):
    db_individu = db.query(Individu).filter(Individu.id == individu_id).first()
    if not db_individu:
        raise HTTPException(status_code=404, detail="Individu non trouvé")
    db.delete(db_individu)
    db.commit()
    return {"message": "Individu supprimé avec succès"}

# **8. Modification des relations**
@app.put("/modifier-relation/{relation_id}")
def modifier_relation(relation_id: int, relation: RelationSchema, db: Session = Depends(get_db)):
    db_relation = db.query(Relation).filter(Relation.id == relation_id).first()
    if not db_relation:
        raise HTTPException(status_code=404, detail="Relation non trouvée")
    db_relation.parent_id = relation.parent_id or db_relation.parent_id
    db_relation.child_id = relation.child_id or db_relation.child_id
    db_relation.relation_type = relation.relation_type or db_relation.relation_type
    db.commit()
    db.refresh(db_relation)
    return {"message": "Relation modifiée avec succès", "relation": db_relation}