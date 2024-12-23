from pydantic import BaseModel, Field
from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional
from typing import Optional, List

# Schéma pour les individus
class IndividuSchema(BaseModel):
    first_name: str = Field(min_length=1, example="John")
    last_name: str = Field(min_length=1, example="Doe")
    birth_date: str = Field(example="2000-01-01")
    death_date: Optional[str] = Field(default=None, example="2090-12-31")

# Schéma pour les relations
class RelationSchema(BaseModel):
    parent_id: int
    child_id: int
    relation_type: str = Field(pattern=r"^(biologique|adoptif|beau-parent)$")
    





