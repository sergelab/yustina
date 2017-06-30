-- Deploy yustina:persons_5 to pg

BEGIN;

ALTER TABLE persons ADD COLUMN photo JSONB;
ALTER TABLE persons ADD COLUMN list_photo JSONB;
ALTER TABLE persons ADD COLUMN video JSONB;

COMMIT;
