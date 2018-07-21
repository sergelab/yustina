-- Deploy yustina:persons_6 to pg

BEGIN;

ALTER TABLE positions ADD COLUMN heading TEXT;
UPDATE positions SET heading = '';
ALTER TABLE positions ALTER COLUMN heading SET NOT NULL;

COMMIT;
