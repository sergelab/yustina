-- Deploy yustina:persons_3 to pg

BEGIN;

ALTER TABLE positions ADD COLUMN priority INTEGER DEFAULT 1;
ALTER TABLE positions ADD COLUMN public_group BOOLEAN DEFAULT TRUE;

COMMIT;
