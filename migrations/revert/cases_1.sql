-- Revert yustina:cases_1 from pg

BEGIN;

ALTER TABLE workcases DROP COLUMN description;

COMMIT;
