-- Deploy yustina:persons_8 to pg

BEGIN;

CREATE TYPE persons_genders AS ENUM ('male', 'female');

ALTER TABLE persons ADD COLUMN gender persons_genders NOT NULL DEFAULT 'male';

COMMIT;
