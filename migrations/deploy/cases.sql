-- Deploy yustina:cases to pg

BEGIN;

CREATE TABLE practices (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES practices(id),
    title TEXT
);

CREATE TABLE workcases (
    id SERIAL PRIMARY KEY,
    title TEXT
);

CREATE TABLE workcase_practice_assotiation (
    workcase_id INTEGER REFERENCES workcases(id),
    practice_id INTEGER REFERENCES practices(id),
    PRIMARY KEY (workcase_id, practice_id)
);

CREATE TABLE workcase_person_assotiation (
    workcase_id INTEGER REFERENCES workcases(id),
    persone_id INTEGER REFERENCES persons(id),
    PRIMARY KEY (workcase_id, persone_id)
);

COMMIT;
