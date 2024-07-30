CREATE TABLE IF NOT EXISTS competition_participants (
    competition_participant_id SERIAL,
    competition_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    PRIMARY KEY (competition_participant_id),
    FOREIGN KEY (competition_id) REFERENCES competition(competition_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id)
);