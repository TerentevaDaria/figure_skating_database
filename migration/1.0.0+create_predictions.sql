CREATE TABLE IF NOT EXISTS predictions (
    user_id INTEGER NOT NULL,
    competition_participant_id INTEGER NOT NULL,
    place smallint NOT NULL,
    PRIMARY KEY (user_id, competition_participant_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (competition_participant_id) REFERENCES competition_participants(competition_participant_id)
);