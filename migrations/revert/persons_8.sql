-- Revert yustina:persons_8 from pg

BEGIN;

ALTER TABLE persons DROP COLUMN gender;
DROP TYPE persons_genders;

COMMIT;
