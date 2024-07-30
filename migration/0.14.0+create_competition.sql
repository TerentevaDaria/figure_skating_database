CREATE TABLE IF NOT EXISTS competition (
    competition_id SERIAL,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    country_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    PRIMARY KEY (competition_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);