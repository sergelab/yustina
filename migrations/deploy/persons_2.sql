-- Deploy yustina:persons_2 to pg

BEGIN;

ALTER TABLE persons ADD COLUMN registry_no TEXT;
ALTER TABLE persons ADD COLUMN specialty TEXT;

COMMIT;
