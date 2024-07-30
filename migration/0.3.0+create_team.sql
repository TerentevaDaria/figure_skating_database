CREATE TABLE IF NOT EXISTS team (
    team_id serial,
    number_of_bears INTEGER NOT NULL DEFAULT '0',
    discipline DISCIPLINE  NOT NULL,
    PRIMARY KEY (team_id)
);
