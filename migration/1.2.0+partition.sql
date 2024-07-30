CREATE TABLE IF NOT EXISTS tmp_participation_information (
    competition_participant_id INTEGER NOT NULL,
    type RESULT_TYPE NOT NULL,
    place SMALLINT NOT NULL,
    points FLOAT(2) NOT NULL,
    PRIMARY KEY (competition_participant_id, type)
) PARTITION BY LIST (type);

CREATE TABLE IF NOT EXISTS type_1 PARTITION OF tmp_participation_information FOR VALUES IN ('total');
CREATE TABLE IF NOT EXISTS type_2 PARTITION OF tmp_participation_information FOR VALUES IN ('short_program');
CREATE TABLE IF NOT EXISTS type_3 PARTITION OF tmp_participation_information FOR VALUES IN ('free_skate');

INSERT INTO tmp_participation_information SELECT * FROM participation_information;

ALTER TABLE participation_information RENAME TO old_participation_information;
ALTER TABLE tmp_participation_information RENAME TO participation_information;

ALTER TABLE type_1 ADD CONSTRAINT fk_1 FOREIGN KEY (competition_participant_id) REFERENCES competition_participants(competition_participant_id);
ALTER TABLE type_2 ADD CONSTRAINT fk_1 FOREIGN KEY (competition_participant_id) REFERENCES competition_participants(competition_participant_id);
ALTER TABLE type_3 ADD CONSTRAINT fk_1 FOREIGN KEY (competition_participant_id) REFERENCES competition_participants(competition_participant_id);
