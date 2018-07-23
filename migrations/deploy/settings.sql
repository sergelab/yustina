-- Deploy yustina:settings to pg

BEGIN;

CREATE TYPE settings_values_types AS ENUM ('Integer', 'Text', 'Boolean');
CREATE TABLE settings (
    name TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    value_type settings_values_types NOT NULL,
    int_value INTEGER NOT NULL DEFAULT 0,
    text_value TEXT NOT NULL DEFAULT '',
    use_textarea BOOLEAN NOT NULL DEFAULT FALSE,
    textarea_rows INTEGER,
    bool_value BOOLEAN NOT NULL DEFAULT FALSE,
    priority INTEGER
);

INSERT INTO settings (priority, name, title, value_type, int_value) VALUES (10, 'total_cases', 'Total cases label', 'Integer', 4321);
INSERT INTO settings (priority, name, title, value_type, bool_value) VALUES (20, 'language_switcher', 'Switch languages label', 'Boolean', TRUE);
INSERT INTO settings (priority, name, title, value_type, text_value, use_textarea, textarea_rows, description) VALUES (30, 'company_phone', 'Company phone label', 'Text', E'+7 495 695-35-25\n+7 495 697-43-53', TRUE, 2, 'Company phone description');
INSERT INTO settings (priority, name, title, value_type, text_value, use_textarea, textarea_rows) VALUES (40, 'ru_company_address', 'Company address (RU) label', 'Text', 'Компания «Юстина»: 119002, г. Москва, Глазовский пер., д. 7.', TRUE, 2);
INSERT INTO settings (priority, name, title, value_type, text_value, use_textarea, textarea_rows) VALUES (50, 'en_company_address', 'Company address (EN) label', 'Text', 'Company «Justina»: 119002, Moscow, Glazovsky, 7.', TRUE, 2);
INSERT INTO settings (priority, name, title, value_type, text_value, use_textarea, textarea_rows) VALUES (60, 'ru_legal', 'Legal info (RU) label', 'Text', 'Исключительные права на результаты интеллектуальной деятельности, размещенные на настоящем информационном ресурсе, принадлежат адвокатскому бюро «Адвокатская фирма „Юстина“» и охраняются в соответствии с законодательством РФ. Любое использование результатов интеллектуальной деятельности допускается исключительно с предварительного письменного согласия правообладателя. Несанкционированное использование влечет предусмотренную законом ответственность.', TRUE, 5);
INSERT INTO settings (priority, name, title, value_type, text_value, use_textarea, textarea_rows) VALUES (70, 'en_legal', 'Legal info (EN) label', 'Text', 'Some legal info', TRUE, 5);

COMMIT;
