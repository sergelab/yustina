-- Deploy yustina:persons to pg

BEGIN;

CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE persons (
    id SERIAL PRIMARY KEY,
    surname TEXT,
    firstname TEXT,
    middlename TEXT,
    bio TEXT
);

CREATE TABLE person_positions_association (
    person_id INTEGER REFERENCES persons(id),
    position_id INTEGER REFERENCES positions(id),
    PRIMARY KEY (person_id, position_id)
);

COMMIT;
