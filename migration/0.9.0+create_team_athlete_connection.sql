CREATE TABLE IF NOT EXISTS team_athlete_connection (
    team_id INTEGER NOT NULL,
    athlete_id INTEGER NOT NULL,
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id),
    PRIMARY KEY (team_id, athlete_id)
);