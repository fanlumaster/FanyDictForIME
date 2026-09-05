# 第三方数据来源与许可

本仓库同时包含两类内容：水杉输入法自己编写的脚本和自建词条，以及从其它开源项目收集来的词库数据。两类内容的许可不同，本文逐条列出，便于使用者和贡献者判断。

自有部分（`makecikudb/` 下的构建脚本、`MetasequoiaImeCustomDict/`、`source/FanyExtDict.txt` 以及各 `*V1` 处理结果中本项目新增的条目）以 [GPL-3.0](LICENSE) 发布，与水杉输入法其余仓库一致。

## 数据来源

下表的「上游许可」于 2026-09-05 按各上游仓库当时的 LICENSE 文件核对，不是凭印象填写。上游随时可能变更，引用前请复核。

| 本仓文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `source/BaseDict.txt`、`cn/BaseDictV1.txt`、`cn/BaseDictAllV1Part1.txt`、`cn/BaseDictAllV1Part2.txt` | [wuhgit/CustomPinyinDictionary](https://github.com/wuhgit/CustomPinyinDictionary) | **仓库未附带任何 LICENSE 文件** |
| `source/BaseDictIce.txt`、`cn/BaseDictIceV1.txt`、`cn/SingleCharsAllV1.txt`、`en/BaseDictIceEn.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | GPL-3.0 |
| `source/SampleIMESimplifiedQuanPin.txt` | [microsoft/Windows-classic-samples](https://github.com/microsoft/Windows-classic-samples) | MIT |
| `cn/Wubi86.txt` | [KyleBing/rime-wubi86-jidian](https://github.com/KyleBing/rime-wubi86-jidian) | Apache-2.0 |
| 单字拼音读音修正数据 | [mozillazg/pinyin-data](https://github.com/mozillazg/pinyin-data) | MIT |
| 英文释义（`zh_en_glosses` 的生成源） | [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT) | MIT |
| `kaomoji/kaomoji.txt` | [aoguai/rime_kaomoji_dict](https://github.com/aoguai/rime_kaomoji_dict) | MIT |
| `en/google_count_1_w.txt` | <https://www.norvig.com/ngrams/count_1w.txt> | 页面未标注许可 |
| `en/oaldpe.mdx`、`en/oaldpe_words.txt` | 牛津高阶词典的 MDict 文件及从中提取的单词表 | 未标注；商业词典 |

## 两处需要项目所有者定夺

以下两条不是本 PR 能替作者决定的，列出来是为了让它们不再隐没在 README 的行文里。

**1. `CustomPinyinDictionary` 上游没有许可声明。** 它是本仓体量最大的中文词库来源（百万级条目），但上游仓库不含 LICENSE 文件，也未在 README 中声明许可。缺少明示授权时，默认是「保留所有权利」，再分发没有明确的法律依据。可选的处置：向上游作者取得书面授权、换用有明确许可的等价词库、或在评估后接受现状并公开记录这一判断。

**2. 仓库里存有牛津高阶词典的 MDict 文件本体。** `en/oaldpe.mdx` 是完整的商业词典数据文件，不只是派生的词表；`en/oaldpe_words.txt` 是从中提取的单词列表。提取出的词表只保留词形、不含释义，风险较低，但 `.mdx` 本体是受版权保护的商业出版物，随开源仓库分发需要单独评估。若确认不宜分发，注意仅删除当前文件不够，该文件仍留在 git 历史里。

## 许可兼容性说明

自有部分采用 GPL-3.0。上游中 MIT 和 Apache-2.0 均可单向并入 GPL-3.0 作品，rime-ice 本身就是 GPL-3.0，因此这几项与本仓许可不冲突；分发时保留各自的版权声明即可。上表中「未标注」和「无 LICENSE」的两类不在此列，见上一节。

## 修改与回报

对于从其它仓库收集来的词库，本项目原则上不新增条目，只修正明显错误（例如错误读音、重复条目）。自建条目集中放在 `FanyExtDict.txt`；候选窗中英翻译的补丁写在 `MetasequoiaImeCustomDict/translations.txt`，不要直接改 ECDICT 大词库。发现上游本身的错误时，欢迎同时回报给上游项目。
