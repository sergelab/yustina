-- Verify yustina:persons on pg

BEGIN;

SELECT * FROM persons;
SELECT * FROM positions;
SELECT * FROM person_positions_association;

ROLLBACK;
