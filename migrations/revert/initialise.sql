-- Revert yustina:initialise from pg

BEGIN;

DROP TABLE users;

COMMIT;
