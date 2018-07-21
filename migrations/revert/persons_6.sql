-- Revert yustina:persons_6 from pg

BEGIN;

ALTER TABLE positions DROP COLUMN heading;

COMMIT;
