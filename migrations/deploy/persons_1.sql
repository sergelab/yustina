-- Deploy yustina:persons_1 to pg

BEGIN;

ALTER TABLE positions ALTER COLUMN name SET NOT NULL;

COMMIT;
