-- Verify yustina:persons_slug on pg

BEGIN;

SELECT slug FROM persons;

ROLLBACK;
