-- Revert yustina:cases_2 from pg

BEGIN;

ALTER TABLE workcase_branch_association RENAME CONSTRAINT "workcase_branch_association_branch_id_fkey" TO "workcase_practice_assotiation_practice_id_fkey";
ALTER TABLE workcase_branch_association RENAME CONSTRAINT "workcase_branch_assotiation_workcase_id_fkey" TO "workcase_practice_assotiation_workcase_id_fkey";

ALTER TABLE workcase_branch_association RENAME TO workcase_practice_assotiation;
ALTER TABLE workcase_practice_assotiation RENAME COLUMN branch_id TO practice_id;

ALTER INDEX workcase_branch_association_pkey RENAME TO workcase_practice_assotiation_pkey;

ALTER TABLE workcase_person_association RENAME TO workcase_person_assotiation;

COMMIT;
