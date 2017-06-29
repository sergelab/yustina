-- Verify yustina:press_slug on pg

BEGIN;

SELECT slug FROM news;

ROLLBACK;
