-- Verify yustina:persons on pg

BEGIN;

SELECT * FROM practices;
SELECT * FROM workcases;
SELECT * FROM workcase_practice_assotiation;
SELECT * FROM workcase_person_assotiation;

ROLLBACK;
