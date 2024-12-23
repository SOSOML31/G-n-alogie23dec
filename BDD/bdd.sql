CREATE DATABASE genealogie;

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
    relation_type VARCHAR(50) NOT NULL CHECK (relation_type IN ('biologique', 'adoptif', 'beau-parent')),
    CONSTRAINT fk_parent FOREIGN KEY (parent_id) REFERENCES Individu (id) ON DELETE CASCADE,
    CONSTRAINT fk_child FOREIGN KEY (child_id) REFERENCES Individu (id) ON DELETE CASCADE,
    CONSTRAINT no_self_parenting CHECK (parent_id <> child_id)
);
