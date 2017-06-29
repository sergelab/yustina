-- Verify yustina:persons_4 on pg

BEGIN;

SELECT short_bio FROM persons;

ROLLBACK;
