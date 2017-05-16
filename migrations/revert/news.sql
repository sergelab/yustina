-- Revert yustina:news from pg

BEGIN;

DROP TABLE news;

COMMIT;
