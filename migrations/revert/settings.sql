-- Revert yustina:settings from pg

BEGIN;

DROP TABLE settings;
DROP TYPE settings_values_types;

COMMIT;
