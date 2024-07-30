CREATE TABLE IF NOT EXISTS users (
    user_id serial,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    number_of_bears INTEGER NOT NULL DEFAULT '0',
    PRIMARY KEY (user_id)
);