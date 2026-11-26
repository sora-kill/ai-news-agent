import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS article (
    article_id     INTEGER PRIMARY KEY,
    url            TEXT NOT NULL UNIQUE,
    title          TEXT,
    processed_date TEXT
);

CREATE TABLE IF NOT EXISTS concept (
    concept_id       INTEGER PRIMARY KEY,
    canonical_term   TEXT NOT NULL UNIQUE,
    english_term     TEXT NOT NULL,
    japanese_term    TEXT,
    vietnamese_term  TEXT,
    occurrence_count INTEGER NOT NULL DEFAULT 0,
    first_seen       TEXT,
    last_seen        TEXT,
    category         TEXT,
    flashcard_id     TEXT
);

CREATE TABLE IF NOT EXISTS occurrence (
    occurrence_id     INTEGER PRIMARY KEY,
    article_id        INTEGER NOT NULL REFERENCES article (article_id),
    concept_id        INTEGER NOT NULL REFERENCES concept (concept_id),
    start_pos         INTEGER NOT NULL,
    end_pos           INTEGER NOT NULL,
    occurrence_number INTEGER NOT NULL,
    UNIQUE (article_id, start_pos)
);
"""


def connect(path):
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn):
    conn.executescript(SCHEMA)
