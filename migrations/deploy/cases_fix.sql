-- Deploy yustina:cases_fix to pg

BEGIN;

ALTER TABLE workcase_person_association RENAME COLUMN persone_id TO person_id;

COMMIT;
