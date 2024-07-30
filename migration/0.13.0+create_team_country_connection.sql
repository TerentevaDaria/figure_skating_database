CREATE TABLE IF NOT EXISTS team_country_connection (
    connection_id SERIAL,
    team_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    PRIMARY KEY (connection_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);