-- Verify yustina:persons_2 on pg

BEGIN;

SELECT registry_no, specialty FROM persons;

ROLLBACK;
