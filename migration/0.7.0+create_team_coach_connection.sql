CREATE TABLE IF NOT EXISTS team_coach_connection (
    connection_id SERIAL,
    team_id INTEGER NOT NULL,
    coach_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    PRIMARY KEY (connection_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (coach_id) REFERENCES coach(coach_id)
);