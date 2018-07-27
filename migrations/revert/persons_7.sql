-- Revert yustina:persons_7 from pg

BEGIN;

ALTER TABLE positions ADD COLUMN heading TEXT NOT NULL DEFAULT '';

ALTER TABLE positions ADD COLUMN name TEXT;

-- Все существующие данные переводим в русский язык
UPDATE positions SET name = ru_name;

ALTER TABLE positions DROP COLUMN ru_name;
ALTER TABLE positions DROP COLUMN en_name;

ALTER TABLE persons DROP COLUMN category_id;

DROP TABLE persons_categories;

COMMIT;
