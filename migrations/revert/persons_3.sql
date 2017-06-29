-- Revert yustina:persons_3 from pg

BEGIN;

ALTER TABLE positions DROP COLUMN priority;
ALTER TABLE positions DROP COLUMN public_group;

COMMIT;
