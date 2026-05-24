"""
2. This is second step.

插入数据到数据库中。
"""

import os.path
import sqlite3
import string

single_char_path = os.path.join(
    os.path.dirname(__file__), "../../../../cn/SingleCharsAllV1.txt"
)
basedict_part1_path = os.path.join(
    os.path.dirname(__file__), "../../../../cn/BaseDictAllV1Part1.txt"
)
basedict_part2_path = os.path.join(
    os.path.dirname(__file__), "../../../../cn/BaseDictAllV1Part2.txt"
)


db_path = os.path.join(os.path.dirname(__file__), "./out/quanpin_multi_tbl_has_jp.db")
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


def choose_tbl(pinyin_str: str) -> str:
    """
    pinyin_str: 分好词的全拼字符串，看有几个部分，就知道是几个字的词条了，不能使用汉字个数来划分，因为有些词条中不止包含汉字。
    """
    word_len = pinyin_str.count("'") + 1
    base_tbl = "tbl_{}_{}"
    return base_tbl.format(word_len if word_len < 8 else "others", pinyin_str[0])


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
            cur_jp = "".join(pinyin[0] for pinyin in cur_line_list[1].split("'"))
            cur_line_tuple = tuple(
                [
                    cur_line_list[1],  # 拼音 key
                    cur_jp,  # 简拼 jp
                    cur_line_list[0],  # 汉字 value
                    cur_line_list[2],  # 权重 weight
                ]
            )
            count += 1
            cursor.execute(
                insert_data_sql.format(choose_tbl(cur_line_list[1])), cur_line_tuple
            )
    print(count)


# 插入单个汉字
insert_lines_from_file_to_db_tbl(single_char_path)
# 插入词语
insert_lines_from_file_to_db_tbl(basedict_part1_path)
insert_lines_from_file_to_db_tbl(basedict_part2_path)

conn.commit()
conn.close()
