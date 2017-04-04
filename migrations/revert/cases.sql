-- Revert yustina:persons from pg

BEGIN;

DROP TABLE workcase_practice_assotiation;
DROP TABLE workcase_person_assotiation;
DROP TABLE practices;
DROP TABLE workcases;

COMMIT;
