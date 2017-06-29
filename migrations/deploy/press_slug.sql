-- Deploy yustina:press_slug to pg

BEGIN;

ALTER TABLE news ADD COLUMN slug TEXT UNIQUE;
UPDATE news SET slug = md5(news.id::TEXT);
ALTER TABLE news ALTER COLUMN slug SET NOT NULL;

COMMIT;
