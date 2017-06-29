-- Revert yustina:press_slug from pg

BEGIN;

ALTER TABLE news DROP COLUMN slug;

COMMIT;
