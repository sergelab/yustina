-- Verify yustina:persons_5 on pg

BEGIN;

SELECT photo, list_photo, video FROM persons;

ROLLBACK;
