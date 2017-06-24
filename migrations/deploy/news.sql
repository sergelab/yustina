-- Deploy yustina:news to pg

BEGIN;

CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    in_trash BOOLEAN NOT NULL DEFAULT FALSE,
    title TEXT NOT NULL,
    subtitle TEXT,
    date_publishing DATE NOT NULL,
    annotation TEXT,
    content TEXT NOT NULL,
    source TEXT,
    source_link TEXT
);

COMMIT;
