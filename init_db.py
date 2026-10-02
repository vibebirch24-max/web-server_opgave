import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db" / "fanfic.db"

SCHEMA_SQL = """
DROP TABLE IF EXISTS stories;

CREATE TABLE stories
(
    uid   serial      primary key,
    title varchar(32) unique not null,
    filename varchar(32) unique not null
);
"""

SEED_ROWS = [
    (1, "Unknown Rider", "unknown-rider.html"),
    (2, "Unknown Rider 2", "unknown-rider-2.html"),
]


def init_db(db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.executemany(
            "INSERT INTO stories (uid, title, filename) VALUES (?, ?, ?);",
            SEED_ROWS,
        )
        conn.commit()


if __name__ == "__main__":
    init_db()
    print(f"Database oprettet: {DB_PATH}")