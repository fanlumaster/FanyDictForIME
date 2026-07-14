"""3. Verify and optimize the generated English database."""

from pathlib import Path
import sqlite3


SCRIPT_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = SCRIPT_DIR.parents[2]
DB_PATH = REPOSITORY_ROOT / "out" / "english.db"


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(DB_PATH)

    with sqlite3.connect(DB_PATH) as conn:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"SQLite integrity check failed: {integrity}")

        count, distinct_words = conn.execute(
            """
            SELECT COUNT(*), COUNT(DISTINCT word)
            FROM english_words
            """
        ).fetchone()
        if count == 0 or count != distinct_words:
            raise RuntimeError(
                f"Unexpected row counts: rows={count}, distinct_words={distinct_words}"
            )
        conn.execute("ANALYZE")
        conn.execute("PRAGMA optimize")
        examples = conn.execute(
            """
            SELECT word, display
            FROM english_words
            WHERE word >= 'hel' AND word < 'hel{'
            ORDER BY CASE WHEN word = 'hel' THEN 0 ELSE 1 END,
                     length(word),
                     word
            LIMIT 5
            """
        ).fetchall()

    print(f"Integrity: {integrity}")
    print(f"Rows: {count}")
    print("Prefix sample for 'hel':")
    for word, display in examples:
        print(f"  {word}\t{display}")


if __name__ == "__main__":
    main()
