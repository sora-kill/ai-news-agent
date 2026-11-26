import sqlite3

import pytest

from vocab.db import connect, create_schema


@pytest.fixture
def conn(tmp_path):
    connection = connect(tmp_path / "test.db")
    create_schema(connection)
    yield connection
    connection.close()


def column_names(conn, table):
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {row[1] for row in rows}


def add_article(conn, url="https://example.com/a"):
    cursor = conn.execute(
        "INSERT INTO article (url, title, processed_date) VALUES (?, ?, ?)",
        (url, "Title", "2026-11-26"),
    )
    return cursor.lastrowid


def add_concept(conn, canonical="large language model"):
    cursor = conn.execute(
        "INSERT INTO concept (canonical_term, english_term) VALUES (?, ?)",
        (canonical, "Large Language Model"),
    )
    return cursor.lastrowid


def add_occurrence(conn, article_id, concept_id, start_pos=0):
    conn.execute(
        "INSERT INTO occurrence"
        " (article_id, concept_id, start_pos, end_pos, occurrence_number)"
        " VALUES (?, ?, ?, ?, ?)",
        (article_id, concept_id, start_pos, start_pos + 20, 1),
    )


def test_tables_have_expected_columns(conn):
    assert column_names(conn, "article") == {
        "article_id", "url", "title", "processed_date",
    }
    assert column_names(conn, "concept") == {
        "concept_id", "canonical_term", "english_term", "japanese_term",
        "vietnamese_term", "occurrence_count", "first_seen", "last_seen",
        "category", "flashcard_id",
    }
    assert column_names(conn, "occurrence") == {
        "occurrence_id", "article_id", "concept_id", "start_pos", "end_pos",
        "occurrence_number",
    }


def test_create_schema_twice_is_safe(conn):
    create_schema(conn)


def test_new_concept_count_starts_at_zero(conn):
    concept_id = add_concept(conn)
    count = conn.execute(
        "SELECT occurrence_count FROM concept WHERE concept_id = ?",
        (concept_id,),
    ).fetchone()[0]
    assert count == 0


def test_duplicate_canonical_term_rejected(conn):
    add_concept(conn)
    with pytest.raises(sqlite3.IntegrityError):
        add_concept(conn)


def test_duplicate_article_url_rejected(conn):
    add_article(conn)
    with pytest.raises(sqlite3.IntegrityError):
        add_article(conn)


def test_duplicate_occurrence_position_rejected(conn):
    article_id = add_article(conn)
    concept_id = add_concept(conn)
    add_occurrence(conn, article_id, concept_id, start_pos=5)
    with pytest.raises(sqlite3.IntegrityError):
        add_occurrence(conn, article_id, concept_id, start_pos=5)


def test_occurrence_with_unknown_concept_rejected(conn):
    article_id = add_article(conn)
    with pytest.raises(sqlite3.IntegrityError):
        add_occurrence(conn, article_id, concept_id=999)
