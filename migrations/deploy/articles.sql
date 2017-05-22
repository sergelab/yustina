-- Deploy yustina:articles to pg

BEGIN;

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    in_trash BOOLEAN NOT NULL DEFAULT FALSE,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

COMMIT;
