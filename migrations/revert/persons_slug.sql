-- Revert yustina:persons_slug from pg

BEGIN;

ALTER TABLE persons DROP COLUMN slug;

COMMIT;
