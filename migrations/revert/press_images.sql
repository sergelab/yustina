-- Revert yustina:press_images from pg

BEGIN;

ALTER TABLE news DROP COLUMN list_photo;
ALTER TABLE news DROP COLUMN photo;

COMMIT;
