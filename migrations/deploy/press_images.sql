-- Deploy yustina:press_images to pg

BEGIN;

ALTER TABLE news ADD COLUMN list_photo JSONB;
ALTER TABLE news ADD COLUMN photo JSONB;

COMMIT;
