CREATE TABLE IF NOT EXISTS team_club_connection (
    connection_id SERIAL,
    team_id INTEGER NOT NULL,
    club_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    PRIMARY KEY (connection_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (club_id) REFERENCES club(club_id)
);