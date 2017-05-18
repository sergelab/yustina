-- Revert yustina:cases_deletable from pg

BEGIN;

ALTER TABLE practices DROP COLUMN in_trash;
ALTER TABLE workcases DROP COLUMN in_trash;

COMMIT;