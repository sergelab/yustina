-- Revert yustina:persons_2 from pg

BEGIN;

ALTER TABLE persons DROP COLUMN registry_no;
ALTER TABLE persons DROP COLUMN specialty;

COMMIT;
