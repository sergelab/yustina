-- Deploy yustina:persons_4 to pg

BEGIN;

ALTER TABLE persons ADD COLUMN short_bio TEXT;

COMMIT;
