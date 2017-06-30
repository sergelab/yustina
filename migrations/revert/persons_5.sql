-- Revert yustina:persons_5 from pg

BEGIN;

ALTER TABLE persons DROP COLUMN photo;
ALTER TABLE persons DROP COLUMN list_photo;
ALTER TABLE persons DROP COLUMN video;

COMMIT;
