from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Modèle Individu
class Individu(Base):
    __tablename__ = "individus"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    death_date = Column(Date, nullable=True)

    parents = relationship("Relation", back_populates="child", foreign_keys="[Relation.child_id]")
    children = relationship("Relation", back_populates="parent", foreign_keys="[Relation.parent_id]")

# Modèle Relation
class Relation(Base):
    __tablename__ = "relations"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("individus.id"), nullable=False)
    child_id = Column(Integer, ForeignKey("individus.id"), nullable=False)
    relation_type = Column(String, nullable=False)

    parent = relationship("Individu", back_populates="children", foreign_keys=[parent_id])
    child = relationship("Individu", back_populates="parents", foreign_keys=[child_id])