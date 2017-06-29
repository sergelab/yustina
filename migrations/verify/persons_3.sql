-- Verify yustina:persons_3 on pg

BEGIN;

SELECT priority, public_group FROM positions;

ROLLBACK;
