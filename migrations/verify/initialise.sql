-- Verify yustina:initialise on pg

BEGIN;

-- Проверим выборку из users
SELECT * FROM users;

ROLLBACK;
