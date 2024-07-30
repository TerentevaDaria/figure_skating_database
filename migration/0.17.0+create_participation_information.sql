CREATE TABLE IF NOT EXISTS participation_information (
    competition_participant_id INTEGER NOT NULL,
    type RESULT_TYPE NOT NULL,
    place SMALLINT NOT NULL,
    points FLOAT(2) NOT NULL,
    PRIMARY KEY (competition_participant_id, type),
    FOREIGN KEY (competition_participant_id) REFERENCES competition_participants(competition_participant_id)
);