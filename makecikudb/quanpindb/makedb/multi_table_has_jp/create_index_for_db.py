"""
3. This is third step.

Create index for key and jp.

Each table can hold tens of thousands of rows, indexes are necessary for query performance.
"""

import sqlite3
from pathlib import Path

repo_root = Path(__file__).resolve().parents[4]
db_path = repo_root / "out" / "msime.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

create_index_key_sql = """
create index {} on {}(key);
"""
create_index_jp_sql = """
create index {} on {}(jp);
"""

base_tbl = "tbl_{}_{}"
base_index_key = "idx_key_{}_{}"
base_index_jp = "idx_jp_{}_{}"

legal_letters = "abcdefghjklmnopqrstwxyz"
for i in range(8):
    for c in legal_letters:
        cur_tbl = base_tbl.format(i + 1 if i < 7 else "others", c)
        cur_index_key = base_index_key.format(i + 1 if i < 7 else "others", c)
        cur_index_jp = base_index_jp.format(i + 1 if i < 7 else "others", c)
        cursor.execute(create_index_key_sql.format(cur_index_key, cur_tbl))
        cursor.execute(create_index_jp_sql.format(cur_index_jp, cur_tbl))

conn.commit()
conn.close()
