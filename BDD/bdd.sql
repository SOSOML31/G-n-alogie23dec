
CREATE TABLE individus (
    id SERIAL PRIMARY KEY,                          -- Identifiant unique pour chaque individu
    first_name VARCHAR(255) NOT NULL,              -- Prénom obligatoire
    last_name VARCHAR(255),                        -- Nom de famille (peut être null pour les cas particuliers)
    birth_date DATE NOT NULL,                      -- Date de naissance obligatoire
    death_date DATE,                               -- Date de décès (peut être null si la personne est vivante)
    CHECK (birth_date <= death_date OR death_date IS NULL)  -- Vérification : la date de décès doit être après la date de naissance
);

-- Création de la table 'relations'
CREATE TABLE relations (
    id SERIAL PRIMARY KEY,                         -- Identifiant unique pour chaque relation
    parent_id INT NOT NULL,                        -- Identifiant du parent (référence)
    child_id INT NOT NULL,                         -- Identifiant de l'enfant (référence)
    relation_type VARCHAR(50) NOT NULL,            -- Type de relation (biologique, adoptif, beau-parent)
    CONSTRAINT fk_parent FOREIGN KEY (parent_id) REFERENCES individus (id) ON DELETE CASCADE,
    CONSTRAINT fk_child FOREIGN KEY (child_id) REFERENCES individus (id) ON DELETE CASCADE,
    CONSTRAINT chk_relation_type CHECK (relation_type IN ('biologique', 'adoptif', 'beau-parent')),
    CONSTRAINT unique_relation UNIQUE (parent_id, child_id, relation_type)  -- Évite les doublons de relations
);

-- Index pour améliorer les performances des recherches
CREATE INDEX idx_individus_name ON individus (first_name, last_name);
CREATE INDEX idx_relations ON relations (parent_id, child_id);