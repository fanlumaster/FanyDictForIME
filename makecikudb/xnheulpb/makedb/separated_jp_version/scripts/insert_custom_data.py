import os.path
import sqlite3
import string


custom_words_path = os.path.join(
    os.path.dirname(__file__), "../../../../../MyCustomDictForIme/words.txt"
)

local_app_data_dir = os.environ.get("LOCALAPPDATA")
db_path = os.path.join(
    local_app_data_dir, "MetasequoiaImeTsf", "cutted_flyciku_with_jp.db"
)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
insert_data_sql = """
insert into {} (
    key,
    jp,
    value,
    weight
) values (?, ?, ?, ?);
"""


def choose_tbl(sp_str: str) -> str:
    word_len = len(sp_str) // 2
    base_tbl = "tbl_{}_{}"
    return base_tbl.format(word_len if word_len < 8 else "others", sp_str[0])


def record_exists(tbl: str, key: str, value: str) -> bool:
    cursor.execute(
        f"SELECT 1 FROM {tbl} WHERE key = ? AND value = ? LIMIT 1", (key, value)
    )
    return cursor.fetchone() is not None


def insert_lines_from_file_to_db_tbl(file_path: str):
    count = 0
    with open(file_path, "rb") as file:
        all_lines = file.readlines()
        for line in all_lines:
            cur_line = line.decode()
            if cur_line.startswith("#"):  # 跳过注释
                continue
            cur_line_list = cur_line.strip().split("\t")
            if cur_line_list[1][0] not in string.ascii_lowercase:  # 滤掉一些如 ê 这样的
                continue
            cur_line_tuple = tuple(
                [
                    cur_line_list[1],
                    cur_line_list[1][::2],
                    cur_line_list[0],
                    cur_line_list[2],
                ]
            )
            print(cur_line_tuple)
            if record_exists(
                choose_tbl(cur_line_list[1]), cur_line_list[1], cur_line_list[0]
            ):
                continue
            count += 1
            cursor.execute(
                insert_data_sql.format(choose_tbl(cur_line_list[1])), cur_line_tuple
            )
    print(count)


insert_lines_from_file_to_db_tbl(custom_words_path)

conn.commit()
conn.close()
