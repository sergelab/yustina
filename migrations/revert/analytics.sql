-- Revert yustina:analytics from pg

BEGIN;

DROP TABLE analytics_person_association;
DROP TABLE analytics;
DROP TABLE themes;

COMMIT;
