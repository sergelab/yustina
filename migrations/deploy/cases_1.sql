-- Deploy yustina:cases_1 to pg

BEGIN;

ALTER TABLE workcases ADD COLUMN description TEXT;

COMMIT;
