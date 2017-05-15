-- Revert yustina:books from pg

BEGIN;

DROP TABLE book_person_association;
DROP TABLE books;
DROP TABLE books_series;

COMMIT;
