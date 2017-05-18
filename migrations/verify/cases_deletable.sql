-- Verify yustina:cases_deletable on pg

BEGIN;

SELECT in_trash FROM practices;
SELECT in_trash FROM workcases;

ROLLBACK;
