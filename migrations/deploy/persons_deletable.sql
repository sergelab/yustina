-- Deploy yustina:persons_deletable to pg

BEGIN;

ALTER TABLE positions ADD COLUMN in_trash BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE persons ADD COLUMN in_trash BOOLEAN NOT NULL DEFAULT FALSE;

COMMIT;
