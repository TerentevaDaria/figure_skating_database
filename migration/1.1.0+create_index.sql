CREATE INDEX IF NOT EXISTS competition_participant_team_id ON competition_participants USING BTREE (team_id);
CREATE INDEX IF NOT EXISTS competition_participants_competition_id ON competition_participants USING BTREE (competition_id);
CREATE INDEX IF NOT EXISTS team_discipline ON team USING BTREE (discipline);