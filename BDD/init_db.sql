-- Créer la base de données
CREATE DATABASE genealogie;

-- Créer un utilisateur pour gérer la BDD
CREATE USER genealogie_user WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE genealogie TO genealogie_user;

-- Se connecter à la base de données
\c genealogie

-- Créer les tables
CREATE TABLE Individu (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    death_date DATE,
    CONSTRAINT birth_before_death CHECK (death_date IS NULL OR death_date > birth_date),
    CONSTRAINT unique_individual UNIQUE (first_name, last_name, birth_date)
);






CREATE TABLE Relations (
    id SERIAL PRIMARY KEY,
    parent_id INT NOT NULL,
    child_id INT NOT NULL,
    relation_type VARCHAR(50) CHECK (relation_type IN ('biologique', 'adoptif', 'beau-parent')),
    CONSTRAINT fk_parent FOREIGN KEY (parent_id) REFERENCES Individu (id) ON DELETE CASCADE,
    CONSTRAINT fk_child FOREIGN KEY (child_id) REFERENCES Individu (id) ON DELETE CASCADE,
    CONSTRAINT no_self_parenting CHECK (parent_id <> child_id)
);

-- Ajouter des contraintes métier pour les relations
CREATE OR REPLACE FUNCTION check_birth_dates()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Individu parent, Individu child
        WHERE NEW.parent_id = parent.id
          AND NEW.child_id = child.id
          AND parent.birth_date > child.birth_date
    ) THEN
        RAISE EXCEPTION 'Un enfant ne peut pas être né avant ses parents biologiques';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER birth_date_check
BEFORE INSERT OR UPDATE ON Relations
FOR EACH ROW
EXECUTE FUNCTION check_birth_dates();