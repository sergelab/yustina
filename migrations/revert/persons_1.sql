-- Revert yustina:persons_1 from pg

BEGIN;

ALTER TABLE positions ALTER COLUMN name DROP NOT NULL;

COMMIT;
