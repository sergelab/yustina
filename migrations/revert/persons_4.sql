-- Revert yustina:persons_4 from pg

BEGIN;

ALTER TABLE persons DROP COLUMN short_bio;

COMMIT;
