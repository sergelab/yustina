-- Revert yustina:persons from pg

BEGIN;

DROP TABLE person_positions_association;
DROP TABLE positions;
DROP TABLE persons;

COMMIT;
