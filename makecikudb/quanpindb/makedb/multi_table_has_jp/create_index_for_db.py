"""
3. This is third step.

Create index for key and jp.

TODO: 感觉小词库不需要创建索引也可以，好像还能更快一点。
"""

import os.path
import sqlite3
import string

db_path = os.path.join(os.path.dirname(__file__), "./out/quanpin_multi_tbl_has_jp.db")
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
