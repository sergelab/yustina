-- Deploy yustina:cases_3 to pg

BEGIN;

-- Drop old workcases
DROP TABLE workcase_person_association;
DROP TABLE workcase_branch_association;
DROP TABLE workcases;

-- New workcases
CREATE TABLE workcases (
    id SERIAL PRIMARY KEY,
    short_description TEXT,
    show_index BOOLEAN DEFAULT FALSE,
    result TEXT,
    in_trash BOOLEAN NOT NULL DEFAULT FALSE,
    person_id INTEGER NOT NULL REFERENCES persons(id)
);

COMMIT;
