-- Revert yustina:articles from pg

BEGIN;

DROP TABLE articles;

COMMIT;
