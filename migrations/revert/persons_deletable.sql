-- Revert yustina:persons_deletable from pg

BEGIN;

ALTER TABLE positions DROP COLUMN in_trash;
ALTER TABLE persons DROP COLUMN in_trash;

COMMIT;
