# About

- `makecikudb/englishdb/extract_oaldpe_headwords.py` 可从 OALDPE 的 MDX 索引中提取英文单词。

```powershell
python makecikudb/englishdb/extract_oaldpe_headwords.py "C:\path\to\oaldpe.mdx"
```

默认输出为 `en/oaldpe_words.txt`，保留纯 ASCII 字母组成的主词条，以及“纯字母键 → 纯字母目标”的复数、时态和派生词形，并转为小写、去重和排序。由短语或连字符词去标点形成的连写别名、OALDPE 内部配置页不会被导出，输出可用于过滤 `google_count_1_w.txt`。如需导出包含短语、别名和标点的全部 MDX 索引键，可添加 `--all-headwords`。

英文数据库由 `oaldpe_words.txt` 和 `BaseDictIceEn.txt` 合并去重生成，不使用 Google 词频数据。BaseDict 只插入纯 ASCII 字母组成的显示词，两个来源不设权重。查询时依次按完整匹配、词长和字母顺序排序。