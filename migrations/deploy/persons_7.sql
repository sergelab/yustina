-- Deploy yustina:persons_7 to pg

BEGIN;

CREATE TABLE persons_categories (
    id SERIAL PRIMARY KEY,
    ru_name TEXT,
    en_name TEXT,
    priority INTEGER NOT NULL DEFAULT 1,
    in_trash BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO persons_categories VALUES (1, 'Управляющие партнеры', 'Managing partners', 1, FALSE);
INSERT INTO persons_categories VALUES (2, 'Старшие партнеры', 'Senior partners', 2, FALSE);
INSERT INTO persons_categories VALUES (3, 'Партнеры', 'Partners', 3, FALSE);
INSERT INTO persons_categories VALUES (4, 'Юристы', 'Lawyers', 4, FALSE);

-- Должности
ALTER TABLE positions DROP COLUMN heading;

ALTER TABLE positions ADD COLUMN ru_name TEXT;
ALTER TABLE positions ADD COLUMN en_name TEXT;

-- Все существующие данные переводим в русский язык
UPDATE positions SET ru_name = name;

ALTER TABLE positions DROP COLUMN name;

-- Персона
ALTER TABLE persons ADD COLUMN category_id INTEGER REFERENCES persons_categories(id);
UPDATE persons SET category_id = 3; -- Всех сделаем партнерами
ALTER TABLE persons ALTER COLUMN category_id SET NOT NULL;

COMMIT;
