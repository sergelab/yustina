-- Verify yustina:analytics on pg

BEGIN;

SELECT * FROM themes;
SELECT * FROM analytics;
SELECT * FROM analytics_person_association;

ROLLBACK;
