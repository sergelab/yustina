-- Deploy yustina:settings to pg

BEGIN;

CREATE TYPE settings_values_types AS ENUM ('Integer', 'Text', 'Boolean');
CREATE TABLE settings (
    name TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    value_type settings_values_types NOT NULL,
    int_value INTEGER NOT NULL DEFAULT 0,
    text_value TEXT NOT NULL DEFAULT '',
    bool_value BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO settings (name, title, value_type, int_value) VALUES ('total_cases', 'Total cases label', 'Integer', 4321);

COMMIT;
