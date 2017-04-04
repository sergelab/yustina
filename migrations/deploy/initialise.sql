-- Deploy yustina:initialise to pg

BEGIN;

-- Пользователи админки
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(200) NOT NULL UNIQUE,
    pw_hash VARCHAR(68) NOT NULL
);

-- Инициализация пользователей админки
INSERT INTO users (username, pw_hash) VALUES (
    'admin', 'pbkdf2:sha1:1000$uArm3CSE$59d1e08f1889f5670f85f65ccc93540acac29e95'
);

COMMIT;
