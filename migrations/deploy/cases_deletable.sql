-- Deploy yustina:cases_deletable to pg

BEGIN;

ALTER TABLE practices ADD COLUMN in_trash BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE workcases ADD COLUMN in_trash BOOLEAN NOT NULL DEFAULT FALSE;

COMMIT;
