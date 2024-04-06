CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE chambers (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    chamber_id INTEGER REFERENCES chambers,
    title TEXT,
    content TEXT,
    echo INTEGER,
    created_at TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    thread_id INTEGER,
    messages TEXT,
    echo INTEGER,
    created_at TIMESTAMP
);

