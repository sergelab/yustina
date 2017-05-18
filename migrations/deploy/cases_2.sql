-- Deploy yustina:cases_2 to pg

BEGIN;

ALTER TABLE workcase_practice_assotiation RENAME COLUMN practice_id TO branch_id;
ALTER TABLE workcase_practice_assotiation RENAME TO workcase_branch_association;

ALTER INDEX workcase_practice_assotiation_pkey RENAME TO workcase_branch_association_pkey;

ALTER TABLE workcase_branch_association RENAME CONSTRAINT "workcase_practice_assotiation_practice_id_fkey" TO "workcase_branch_association_branch_id_fkey";
ALTER TABLE workcase_branch_association RENAME CONSTRAINT "workcase_practice_assotiation_workcase_id_fkey" TO "workcase_branch_assotiation_workcase_id_fkey";

ALTER TABLE workcase_person_assotiation RENAME TO workcase_person_association;

COMMIT;
