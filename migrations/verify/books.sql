-- Verify yustina:books on pg

BEGIN;

SELECT * FROM books_series;
SELECT * FROM books;
SELECT * FROM book_person_association;

ROLLBACK;
