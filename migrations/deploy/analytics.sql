-- Deploy yustina:analytics to pg

BEGIN;

CREATE TABLE themes (
    id SERIAL PRIMARY KEY,
    in_trash BOOLEAN NOT NULL DEFAULT FALSE,
    name TEXT
);

CREATE TABLE analytics (
    id SERIAL PRIMARY KEY,
    in_trash BOOLEAN NOT NULL DEFAULT FALSE,
    title TEXT NOT NULL,
    theme_id INTEGER REFERENCES themes(id),
    annotation TEXT,
    content TEXT,
    authors TEXT
);

CREATE TABLE analytics_person_association (
    person_id INTEGER REFERENCES persons(id),
    analytics_id INTEGER REFERENCES analytics(id),
    PRIMARY KEY (person_id, analytics_id)
);

COMMIT;
