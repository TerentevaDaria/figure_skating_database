CREATE TABLE IF NOT EXISTS country (
    country_id SERIAL,
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (country_id)
);