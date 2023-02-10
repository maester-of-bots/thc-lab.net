DROP TABLE IF EXISTS urls_biscuit;

CREATE TABLE urls_biscuit (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    original_url TEXT NOT NULL,
    clicks INTEGER NOT NULL DEFAULT 0
);
