-- Deploy yustina:persons_slug to pg

BEGIN;

ALTER TABLE persons ADD COLUMN slug TEXT UNIQUE;
UPDATE persons SET slug = md5(persons.id::TEXT);
ALTER TABLE persons ALTER COLUMN slug SET NOT NULL;

COMMIT;
