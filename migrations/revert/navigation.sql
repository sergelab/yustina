-- Revert yustina:navigation from pg

BEGIN;

DROP TABLE navigation;

COMMIT;
