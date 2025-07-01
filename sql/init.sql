CREATE SCHEMA minicrud;

CREATE TABLE minicrud.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    api_token VARCHAR(128) UNIQUE
);

CREATE TABLE minicrud.data (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    last_modified TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES minicrud.users (id)
);
