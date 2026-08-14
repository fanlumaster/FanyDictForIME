# -*- coding: utf-8 -*-
"""Build the emoji table inside MetasequoiaImeDict/out/others.db."""

from collections import defaultdict, OrderedDict
from pathlib import Path
import os
import sqlite3

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
EMOJI_DIR = REPO_ROOT / "emoji"
OUT_DIR = REPO_ROOT / "out"
DB_PATH = OUT_DIR / "others.db"

CATEGORY_TITLES = {
    "Smileys & Emotion": "Smileys and emotion",
    "People & Body": "People and body",
    "Animals & Nature": "Animals and nature",
    "Food & Drink": "Food and drink",
    "Travel & Places": "Travel and places",
    "Activities": "Activities",
    "Objects": "Objects",
    "Symbols": "Symbols",
    "Flags": "Flags",
}

TEST_LINE = (
    r"^(?P<codes>[0-9A-Fa-f ]+?)\s*;\s*(?P<status>fully-qualified|component)\s*"
    r"#\s*(?P<emoji>\S+)\s+E[0-9.]+\s+(?P<name>.+)$"
)


VS16 = "\ufe0f"


def strip_vs(text: str) -> str:
    return text.replace(VS16, "")


def load_keyword_map(path: Path) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = defaultdict(list)
    seen: dict[str, set[str]] = defaultdict(set)
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        keyword, emoji = stripped.split("\t", 1)
        keyword = keyword.strip()
        emoji = emoji.strip()
        if not keyword or not emoji or keyword in seen[emoji]:
            continue
        seen[emoji].add(keyword)
        mapping[emoji].append(keyword)
    return mapping


def keywords_for(emoji: str, mapping: dict[str, list[str]], stripped_index: dict[str, list[str]]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for keyword in mapping.get(emoji, []) + stripped_index.get(strip_vs(emoji), []):
        if keyword not in seen:
            seen.add(keyword)
            result.append(keyword)
    return result


def index_by_stripped(mapping: dict[str, list[str]]) -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    seen: dict[str, set[str]] = defaultdict(set)
    for emoji, keywords in mapping.items():
        key = strip_vs(emoji)
        for keyword in keywords:
            if keyword not in seen[key]:
                seen[key].add(keyword)
                index[key].append(keyword)
    return index


def load_catalog(emoji_test_path: Path) -> OrderedDict[str, tuple[str, int]]:
    import re

    pattern = re.compile(TEST_LINE)
    catalog: OrderedDict[str, tuple[str, int]] = OrderedDict()
    group = ""
    order = 0
    for line in emoji_test_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# group:"):
            group = line.split(":", 1)[1].strip()
            continue
        match = pattern.match(line)
        if not match:
            continue
        name = match.group("name").strip()
        emoji = match.group("emoji")
        status = match.group("status")
        if status == "component":
            continue
        if "skin tone" in name.lower():
            continue
        title = CATEGORY_TITLES.get(group)
        if not title:
            continue
        if emoji in catalog:
            continue
        catalog[emoji] = (title, order)
        order += 1
    return catalog


def write_catalog(catalog: OrderedDict[str, tuple[str, int]], path: Path) -> None:
    lines = ["# emoji<TAB>category<TAB>sort_order"]
    for emoji, (category, order) in catalog.items():
        lines.append(f"{emoji}\t{category}\t{order}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def read_catalog(path: Path) -> OrderedDict[str, tuple[str, int]]:
    catalog: OrderedDict[str, tuple[str, int]] = OrderedDict()
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        emoji, category, order = stripped.split("\t")
        catalog[emoji] = (category, int(order))
    return catalog


def build_rows(
    catalog: OrderedDict[str, tuple[str, int]],
    zh: dict[str, list[str]],
    en: dict[str, list[str]],
) -> list[tuple[str, str, int, str]]:
    zh_index = index_by_stripped(zh)
    en_index = index_by_stripped(en)
    rows = []
    known = {strip_vs(emoji) for emoji in catalog}
    for emoji, (category, order) in catalog.items():
        merged: list[str] = []
        seen: set[str] = set()
        for keyword in keywords_for(emoji, zh, zh_index) + keywords_for(emoji, en, en_index):
            if keyword not in seen:
                seen.add(keyword)
                merged.append(keyword)
        rows.append((emoji, category, order, " ".join(merged)))

    extra_order = max((order for _, order in catalog.values()), default=-1) + 1
    extras = []
    for source in (zh, en):
        for emoji in source:
            key = strip_vs(emoji)
            if key in known:
                continue
            known.add(key)
            merged: list[str] = []
            seen: set[str] = set()
            for keyword in keywords_for(emoji, zh, zh_index) + keywords_for(emoji, en, en_index):
                if keyword not in seen:
                    seen.add(keyword)
                    merged.append(keyword)
            extras.append((emoji, "Symbols", extra_order, " ".join(merged)))
            extra_order += 1
    rows.extend(extras)
    return rows


def create_and_insert(rows: list[tuple[str, str, int, str]]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DROP TABLE IF EXISTS emoji")
        conn.execute("DROP INDEX IF EXISTS idx_emoji_category_order")
        conn.execute(
            """
            CREATE TABLE emoji (
                emoji TEXT NOT NULL,
                category TEXT NOT NULL,
                sort_order INTEGER NOT NULL,
                keywords TEXT NOT NULL,
                PRIMARY KEY (emoji)
            ) WITHOUT ROWID
            """
        )
        conn.execute(
            "CREATE INDEX idx_emoji_category_order ON emoji(category, sort_order)"
        )
        conn.executemany(
            "INSERT INTO emoji (emoji, category, sort_order, keywords) VALUES (?, ?, ?, ?)",
            rows,
        )
        conn.execute("ANALYZE")
        conn.commit()


def copy_to_appdata() -> None:
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        return
    dest_dir = Path(local) / "metasequoiaime"
    if not dest_dir.is_dir():
        return
    dest = dest_dir / "others.db"
    dest.write_bytes(DB_PATH.read_bytes())
    print(f"Copied: {dest}")
    leftover = dest_dir / "emoji.db"
    if leftover.exists():
        leftover.unlink()
        print(f"Removed leftover: {leftover}")


def find_emoji_test() -> Path | None:
    candidates = [
        EMOJI_DIR / "emoji-test.txt",
        Path(
            r"C:\Users\SonnyCalcr\.cursor\projects\c-Users-SonnyCalcr-EDisk-CppCodes-IMECodes"
            r"\agent-tools\ada26963-9205-4561-bfd6-d653d17660ca.txt"
        ),
    ]
    for path in candidates:
        if path.is_file():
            return path
    return None


def main() -> None:
    catalog_path = EMOJI_DIR / "emoji_catalog.txt"
    emoji_test = find_emoji_test()
    if emoji_test:
        catalog = load_catalog(emoji_test)
        write_catalog(catalog, catalog_path)
        print(f"Wrote catalog: {catalog_path} ({len(catalog)} emojis)")
    elif catalog_path.is_file():
        catalog = read_catalog(catalog_path)
        print(f"Loaded catalog: {catalog_path} ({len(catalog)} emojis)")
    else:
        raise FileNotFoundError("Need emoji-test.txt or emoji_catalog.txt")

    zh = load_keyword_map(EMOJI_DIR / "emoji.txt")
    en = load_keyword_map(EMOJI_DIR / "emoji_en.txt")
    rows = build_rows(catalog, zh, en)
    create_and_insert(rows)
    leftover_out = OUT_DIR / "emoji.db"
    if leftover_out.exists():
        leftover_out.unlink()
        print(f"Removed leftover: {leftover_out}")
    copy_to_appdata()

    categories: dict[str, int] = OrderedDict()
    for _, category, _, _ in rows:
        categories[category] = categories.get(category, 0) + 1
    print(f"Created: {DB_PATH}")
    print(f"rows: {len(rows)}")
    for name, count in categories.items():
        print(f"  {name}: {count}")


if __name__ == "__main__":
    main()
