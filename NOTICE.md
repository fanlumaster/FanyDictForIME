# 来源与授权说明

本仓库**不对外提供统一的开源许可**，因为其中绝大部分词库并非本项目的作品，而是从其他项目收集、合并、去重而来（见 [README](README.md)）。给整个仓库挂一份 LICENSE 等于替上游作者重新授权，因此这里改为逐项说明来源与上游条款。使用或再分发本仓库的数据时，请以对应上游的条款为准。

## 中文词库

| 文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `source/BaseDict.txt`、`cn/BaseDictV1.txt` | [wuhgit/CustomPinyinDictionary](https://github.com/wuhgit/CustomPinyinDictionary) | **未声明** |
| `source/BaseDictIce.txt`、`cn/BaseDictIceV1.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | GPL-3.0 |
| `cn/BaseDictAllV1Part1.txt`、`cn/BaseDictAllV1Part2.txt` | 上面两者合并去重 | GPL-3.0 与**未声明**的混合 |
| `cn/SingleCharsAllV1.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice)，读音以 [mozillazg/pinyin-data](https://github.com/mozillazg/pinyin-data) 校正 | GPL-3.0 + MIT |
| `source/SampleIMESimplifiedQuanPin.txt` | [microsoft/Windows-classic-samples](https://github.com/microsoft/Windows-classic-samples) | MIT |
| `source/Wubi86.txt` | [KyleBing/rime-wubi86-jidian](https://github.com/KyleBing/rime-wubi86-jidian) | Apache-2.0 |
| `source/FanyExtDict.txt`、`cn/phrases.txt` | 本项目自建 | 见下方「本项目自建部分」 |
| `cn/HelpCode.txt` | 规则参考小鹤形码 | 权利归小鹤方案作者 |

## 英文与符号词库

| 文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `source/BaseDictIceEn.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | GPL-3.0 |
| `en/google_count_1_w.txt` | [Google 1/3 million 词频表](https://www.norvig.com/ngrams/count_1w.txt) | 以来源页面说明为准 |
| `en/oaldpe_words.txt` | 自 oaldpe.mdx 提取的词形列表 | 权利归词典出版方 |
| `kaomoji/` | [aoguai/rime_kaomoji_dict](https://github.com/aoguai/rime_kaomoji_dict) | MIT |
| 候选翻译数据 | [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT) | MIT |

## 下游影响

由 `cn/BaseDictAllV1Part1.txt` 与 `cn/BaseDictAllV1Part2.txt` 构建出的 `msime.db` 同时包含 rime-ice（GPL-3.0）与 CustomPinyinDictionary（未声明许可）的内容。使用该数据库的前端（如 [MSIME-Linux](https://github.com/metasequoiaime/MSIME-Linux) 的 DEB／RPM 包）本身以 GPL-3.0 分发，与 rime-ice 兼容，但**必须保留对 rime-ice 的署名**。

## 待解决

以下部分目前没有明确的再分发授权，需要与上游作者确认后才能补上：

- [wuhgit/CustomPinyinDictionary](https://github.com/wuhgit/CustomPinyinDictionary) 未声明任何许可，而它是 `msime.db` 的主体。
- `en/oaldpe_words.txt` 提取自商业词典。词典本体 `en/oaldpe.mdx` 曾经也在本仓中，现已移除——构建只需要提取好的词形列表，不需要词典本体。需要重新生成词表时，自备 `.mdx` 并作为参数传给 `makecikudb/englishdb/extract_oaldpe_headwords.py`。**注意移除只影响当前版本，该文件仍留在 git 历史中。**
- 辅助码规则参考自小鹤形码，权利归方案作者。

在这些条目澄清之前，请不要假定本仓库的数据可以自由再分发。

## 本项目自建部分

`source/FanyExtDict.txt`、`cn/phrases.txt` 以及 `makecikudb/` 下的构建脚本由本项目编写，依据 GPL-3.0 提供，与组织内其他仓库一致。
