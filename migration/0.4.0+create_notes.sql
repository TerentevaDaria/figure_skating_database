CREATE TABLE IF NOT EXISTS notes (
    note_id SERIAL,
    user_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    PRIMARY KEY (note_id),
    FOREIGN KEY (user_id) references users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) references team(team_id) ON DELETE CASCADE
);
