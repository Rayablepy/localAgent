CREATE TABLE IF NOT EXISTS messages (
    id integer PRIMARY KEY AUTOINCREMENT,
    role text NOT NULL,
    CONTENT text NOT NULL
);
