# 介绍

## 初始词库的来源

以下是 5 个中文词库。

- `BaseDict.txt` 词库来自[这里](https://github.com/wuhgit/CustomPinyinDictionary)，取的是 `2023-09-28(No.82)` 这个版本，条目目前有 `1415159` 个条目。
- `BaseDictIce.txt` 词库来自[这里](https://github.com/iDvel/rime-ice)
- `SampleIMESimplifiedQuanPin.txt` 词库来自[这里](https://github.com/microsoft/Windows-classic-samples/tree/main/Samples/IME/cpp/SampleIME/Dictionary)。

上面三个都是原封不动搬过来的。

- `SingleChars.txt` 来自[这里](https://github.com/iDvel/rime-ice)。但是，经过了我的处理，把一些原来不对的拼音，比如，绿(lv)给使用这个[仓库](https://github.com/mozillazg/pinyin-data/blob/master/pinyin.txt)中的数据纠正了过来，保留了原有的雾凇的 8105 简体常用字的同时，对新加入的没有权重的字作了去重，去重的逻辑是把在 8105 中存在的条目给去掉。
- `FanyExtDict.txt` 我自己根据上面的基础添加的一些不与上面的词库重复的一些条目的词库。

以下是 1 个英文词库。

- BaseDictIceEn.txt 词库来自[这里](https://github.com/iDvel/rime-ice)

## 说明

词库的 txt 文件打开时最好使用思源系列的字体或者花园明朝应该也可以，因为有些生僻的汉字在 Windows 下的很多字体是不支持的。

对于从别的仓库搜集来的词库，我不会在其中添加新的条目，但是，如果发现有错误的地方，会作相应的修改。

我自己添加的条目会放到 FanyExtDict.txt 中。

### cn 目录

- BaseDictIceV1.txt 经过我处理的 BaseDictIce.txt 的修改版。
- BaseDictV1.txt 经过我处理的 BaseDict.txt 修改版。
- BaseDictAllV1Part1.txt 和 BaseDictAllV1Part2 这两个合起来就是我把上面那两个去重的结果
- 53013_single.txt 这个是我对所有 unicode 现在支持的汉字

## 额外说明

由于 Github 的单个文件的限制，我将 ./cn/BaseDictV1.txt 拆成了两个文件，分别是，

- ./cn/BaseDictAllV1Part1.txt
- ./cn/BaseDictAllV1Part2.txt

然后，逐个解释每个词库的来源/里面到底装的是什么东西，

- 53013_single.txt: 汉字的单字，来自 unicode 的文档       
- BaseDictAllV1Part1.txt: 把上面所说的百万词库和雾凇的短语词库结合在一起，然后去重，拆分出来的 part1
- BaseDictAllV1Part2.txt: 把上面所说的百万词库和雾凇的短语词库结合在一起，然后去重，拆分出来的 part2
- BaseDictIceV1.txt: 雾凇词库
- BaseDictV1.txt: 这是上面所说的百万词库(https://github.com/wuhgit/CustomPinyinDictionary)
- HelpCode.txt: 辅助码，规则主要参考小鹤的形码
- phrases.txt: 自造短语
- SingleCharsAllV1.txt: 结合了雾凇词库中的单字，然后补充了 uniocde 中的剩下几万个比较常见的字，虽然国家规范常用字只有 8000 个左右

---

感谢：

- <https://github.com/iDvel/rime-ice>
- <https://github.com/wuhgit/CustomPinyinDictionary>


