-- Deploy yustina:news_1 to pg

BEGIN;

ALTER TABLE news ALTER COLUMN annotation DROP NOT NULL;
ALTER TABLE news ALTER COLUMN content DROP NOT NULL;

COMMIT;
