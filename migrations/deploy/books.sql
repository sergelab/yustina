-- Deploy yustina:books to pg

BEGIN;

CREATE TABLE books_series (
    id SERIAL PRIMARY KEY,
    in_trash BOOLEAN NOT NULL DEFAULT FALSE,
    name TEXT,
    annotation TEXT
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    in_trash BOOLEAN NOT NULL DEFAULT FALSE,
    title TEXT NOT NULL,
    series_id INTEGER REFERENCES books_series(id),
    annotation TEXT,
    publisher_info TEXT,
    authors TEXT
);

CREATE TABLE book_person_association (
    person_id INTEGER REFERENCES persons(id),
    book_id INTEGER REFERENCES books(id),
    PRIMARY KEY (person_id, book_id)
);

COMMIT;
