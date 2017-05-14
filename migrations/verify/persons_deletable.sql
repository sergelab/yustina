-- Verify yustina:persons_deletable on pg

BEGIN;

SELECT in_trash FROM positions;
SELECT in_trash FROM persons;

ROLLBACK;
