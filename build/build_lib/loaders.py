import csv
from typing import TextIO

from .union_find import UnionFind


# NOTE 韻典的數據錯誤暫直接寫在代碼這裡
EXCLUDED_CHARS = {  # 不收入這些字的任何異體關係
    '苎',  # 「蒙懞矇朦苎」誤列為全等異體，應為「蒙懞」交疊、「蒙朦矇」交疊
    '蒙',
    '懞',
    '矇',
    '朦',
    '芸',  # 誤列為「藝」全等異體，應為簡體
    '弁',  # 誤列為「辨辯」等字全等異體，應為簡體
    '皝',  # 誤列為「皓顯」交疊異體
}
EXCLUDED_EQUIVALENT_PAIRS = {  # 不收入這些全等異體關係
    ('瀋', '沉'),
    ('干', '乾'),
    ('榦', '乾'),
    ('搋', '弌'),
}

# 忽略 OpenCC 以下繁簡對應
EXCLUDED_OPENCC = {
    ('閒', '闲'),  # 韻典的「閑>闲」更能有效區分「間」「閑」兩者
}


def initialize_results(
    equivalents: UnionFind[str] = None,
    intersecting_groups: set[str] | None = None,
    simplifications: dict[str, set[str]] | None = None,
):
    if equivalents is None:
        equivalents = UnionFind()
    if intersecting_groups is None:
        intersecting_groups = set()
    if simplifications is None:
        simplifications = {}
    return equivalents, intersecting_groups, simplifications


def load_ytenx_csv(
    file: TextIO,
    equivalents: UnionFind[str] = None,
    intersecting_groups: set[str] | None = None,
    simplifications: dict[str, set[str]] | None = None,
):
    equivalents, intersecting_groups, simplifications = initialize_results(
        equivalents, intersecting_groups, simplifications
    )

    for row in csv.DictReader(file):
        entry = row['#字']

        if entry not in EXCLUDED_CHARS and (equiv := row.get('全等')):
            chs = [
                ch
                for ch in equiv
                if ch not in EXCLUDED_CHARS
                and (entry, ch) not in EXCLUDED_EQUIVALENT_PAIRS
                and (ch, entry) not in EXCLUDED_EQUIVALENT_PAIRS
            ]
            if len(chs):
                equivalents.add(entry)
                for ch in chs:
                    equivalents.add(ch)
                    equivalents.union(entry, ch)

        if inter := row.get('語義交疊', '') + row.get('其他異體', ''):
            chs = [ch for ch in entry + inter if ch not in EXCLUDED_CHARS]
            intersecting_groups.add(''.join(sorted(set(chs))))

        if simp := row.get('簡體'):
            simplifications.setdefault(entry, set()).update(simp)
        if trad := row.get('繁體'):
            for ch in trad:
                simplifications.setdefault(ch, set()).add(entry)

    return equivalents, intersecting_groups, simplifications


def load_ytenx(
    equivalents: UnionFind[str] = None,
    intersecting_groups: set[str] | None = None,
    simplifications: dict[str, set[str]] | None = None,
) -> tuple[UnionFind[str], set[str], dict[str, set[str]]]:
    res = (equivalents, intersecting_groups, simplifications)
    for filepath in ('data/ytenx/JihThex.csv', 'data/ytenx/ThaJihThex.csv'):
        with open(filepath) as fin:
            res = load_ytenx_csv(fin, *res)
    return res


def load_opencc(simplifications: dict[str, set[str]] | None = None):
    if simplifications is None:
        simplifications = {}

    for filepath in ('data/opencc/TSCharacters.txt', 'data/opencc/TSPhrases.txt'):
        with open(filepath) as fin:
            for line in fin:
                t_phrase, s_phrases = line.rstrip().split('\t')
                for s_phrase in s_phrases.split():
                    assert len(t_phrase) == len(
                        s_phrase
                    ), f'Length mismatch: {repr(t_phrase)} {repr(s_phrase)}'
                    for t, s in zip(t_phrase, s_phrase):
                        if t != s and (t, s) not in EXCLUDED_OPENCC:
                            simplifications.setdefault(t, set()).add(s)
    return simplifications


def load_yitizi_txt(
    equivalents: UnionFind[str] = None,
    intersecting_groups: set[str] | None = None,
    simplifications: dict[str, set[str]] | None = None,
):
    equivalents, intersecting_groups, simplifications = initialize_results(
        equivalents, intersecting_groups, simplifications
    )
    with open('data/yitizi.txt') as fin:
        for lineno, line in enumerate(fin, 1):
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            num_ascii = sum(1 for ch in line if ch.isascii())
            assert num_ascii <= 1
            if num_ascii == 0:
                intersecting_groups.add(''.join(sorted(line)))
            elif len(line) >= 3 and line.startswith('='):
                equivalents.add(line[1])
                for ch in line[2:]:
                    equivalents.add(ch)
                    equivalents.union(line[1], ch)
            elif len(line) >= 3 and line[1] == '>':
                simplifications.setdefault(line[0], set()).update(line[2:])
            else:
                raise ValueError(f'line {lineno}: unknown format: {line}')
    return equivalents, intersecting_groups, simplifications


def load_all():
    equiv, inter, simp = load_ytenx()
    load_opencc(simp)
    load_yitizi_txt(equiv, inter, simp)
    return equiv, inter, simp
