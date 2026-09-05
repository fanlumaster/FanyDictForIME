# AGENTS.md — MSIME-Dict

产品级约定与跨仓契约以 [MSIME-Windows 的 AGENTS.md](https://github.com/metasequoiaime/MSIME-Windows/blob/main/AGENTS.md) 为准，那一份统领整个水杉输入法项目。本文件只记录本仓自己的规则。

本仓是词库数据与构建脚本：源数据是 `cn/`、`en/`、`emoji/`、`kaomoji/`、`symbols/`、`mix/` 下的文本，产物是四个二进制数据文件。引擎只读取产物，不解析这里的源数据。

## 构建

```bash
python -m pip install -r requirements.txt
python build_all.py --clean --fetch-references
python tools/verify_dictionaries.py
```

`build_all.py` 把 `makecikudb/` 下各目录的分步脚本按正确顺序串成 11 个 stage，全量 clean build 大约 20 秒。**各分步脚本仍是权威**，编排器只是按顺序调用它们，单独执行的用法不变。

产物写到 `out/`（已 gitignore，**不要提交构建产物**）：

| 产物 | 内容 |
|---|---|
| `msime.db` | 全拼分表、86 五笔、快捷短语、日语词表 |
| `english.db` | 英文候选词表与 ECDICT 双向释义表 |
| `others.db` | emoji、颜文字、符号目录 |
| `dict_japanese.dat` | 日语整句解码的只读 Viterbi 模型 |
| `mozc_dictionary_oss_README.txt` | Mozc 授权声明，**必须随模型一起分发** |

## 加了 stage 要同时改三处

新增或改动产物时，`build_all.py` 的 `STAGES`、`SHIPPING_ARTIFACTS`、以及 `tools/verify_dictionaries.py` 的检查项要一起改，workflow 上传和发布的文件列表也要跟上。少改一处的典型后果是：stage 跑成功、产物没进 release、下游安装包缺文件，而且没有任何环节报错。

`tools/verify_dictionaries.py` 的行数下限刻意设得远低于当前值，日常增删词条不会触发，它拦的是「表空了」这类事故。

## 全拼分表命名（跨仓硬约定）

`msime.db` 按音节数加首音节首字母分表，1–7 音节是 `tbl_{N}_{首字母}`，≥8 音节是 `tbl_others_{首字母}`。

**权威实现在 MSIME-Engine 的 `quanpin/quanpin_query.cpp::build_table_name`**，本仓的建库脚本必须与它一致，另外两处一致方是设置页加词和 `user_dictionary_journal.cpp` 的用户词库回放。四处不一致时，安装升级的词库回放会整批回滚并中止安装。

**禁止对 ≥8 音节拼出 `tbl_8_*`**，建库脚本不会创建这些表。

## 外部数据

两个 stage 读仓外数据，`--fetch-references` 会按固定 revision clone 到仓库同级的 `ReferenceProjects/`：

- `skywind3000/ECDICT` — 候选窗中英释义的来源
- `Selaube/rime-jp_sela` — 日语词表

**revision 是刻意固定的**，为的是同一个 commit 重建能得到相同的词库。升级时连同 `build_all.py` 里的 `MOZC_REVISION` 一起当作有意的数据变更来评审，不要顺手跟到最新。

不加 `--fetch-references` 时依赖它们的 stage 会被跳过而不是报错，方便本地做部分构建；发布构建用 `--require-all` 让缺失直接失败。

日语整句模型的 Mozc 原始数据由 `build_sentence_model.py --download` 自己拉。**它的 `README.txt` 含 IPAdic / ICOT / 冲绳授权声明，发布二进制模型时必须一并分发**，`japanese-model` stage 会把它复制成 `out/mozc_dictionary_oss_README.txt`。

## 步骤顺序以脚本自己的说明为准

各目录的执行顺序不统一，编排器逐个遵循各自的声明，不要强行统一：

- `makecikudb/quanpindb/makedb/multi_table_has_jp/` 的三个脚本 docstring 写了编号，是**建表 → 插数据 → 建索引**
- 同目录的 `README.md` 却写成建表 → 建索引 → 插数据，**与脚本自己的编号矛盾**，编排器按 docstring 走，因为对空表先建索引只会拖慢插入
- `wubi86db/` 和 `mixdb/` 的顺序在文件名编号里（`01`、`02`、`03`、`04`）

## 发布

CI 每次 push 和 PR 都跑完整构建加校验。手动触发 `Build dictionaries` 并勾选 `publish` 时，会把产物和 `SHA256SUMS.txt` 发成 `dict-YYYY.MM.DD` 的 release，供 MSIME-Windows 的安装包发布流程下载并校验。

**词库改了要先发一个新的 `dict-*` release，Windows 端的下一个安装包版本才会带上。** 只合进 main 不发 release 的话，用户拿到的还是旧词库。

## 隐私

示例数据不得使用真实可拨的手机号、真实地址或真实人名，即便只是 mock。手机号用 `13800000000` 这类保留号段，地址用明显虚构串。这条来自 MSIME-Windows#74。

## 提交

提交信息用 `type(scope): 摘要`。不要添加 `Co-Authored-By`、`Generated with` 或其他 AI 生成标记。
