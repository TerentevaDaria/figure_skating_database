CREATE TABLE IF NOT EXISTS favorite_athletes (
    user_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    PRIMARY KEY (user_id, team_id)
);
