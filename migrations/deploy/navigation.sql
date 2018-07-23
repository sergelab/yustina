-- Deploy yustina:navigation to pg

BEGIN;

CREATE TABLE navigation (
    id SERIAL PRIMARY KEY,
    ru_caption TEXT,
    en_caption TEXT,
    route TEXT,
    route_params JSONB DEFAULT '{}',
    ru_activity BOOLEAN DEFAULT TRUE,
    en_activity BOOLEAN DEFAULT TRUE,
    in_trash BOOLEAN NOT NULL DEFAULT FALSE,
    priority INTEGER
);

INSERT INTO navigation (ru_caption, en_caption, route, route_params, priority) VALUES ('О фирме', 'About', 'about', '{}', 1);
INSERT INTO navigation (ru_caption, en_caption, route, route_params, priority) VALUES ('Партнёры', 'Partners', 'partners.partners', '{}', 2);
INSERT INTO navigation (ru_caption, en_caption, route, route_params, priority) VALUES ('Аналитика', 'Analytics', 'analytics.analytics', '{}', 3);
INSERT INTO navigation (ru_caption, en_caption, route, route_params, priority) VALUES ('Пресс-центр', 'Press', 'press.news', '{}', 4);
INSERT INTO navigation (ru_caption, en_caption, route, route_params, priority) VALUES ('Книги', 'Books', 'books.books', '{}', 5);
INSERT INTO navigation (ru_caption, en_caption, route, route_params, priority) VALUES ('Контакты', 'Contacts', 'contacts', '{}', 6);

COMMIT;
