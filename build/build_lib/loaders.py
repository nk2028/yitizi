import csv
from itertools import chain, islice
from typing import Dict, Optional, Set, Tuple, Union

from .union_find import UnionFind


# HACK 韻典的數據錯誤暫直接寫在代碼這裡
EXCLUDED_CHARS = {  # 不收入這些字的任何異體關係
    '苎',  # 誤列為「蒙懞矇朦」全等異體
    '芸',  # 誤列為「藝」全等異體，應為簡體
    '弁',  # 誤列為「辨辯」等字全等異體，應為簡體
}
EXCLUDED_PAIRS = {  # 不收入這些異體關係（不論關係種類）
    ('瀋', '沉'),  # 誤列為全等異體
    ('干', '乾'),  # 同上
    ('榦', '乾'),  # 同上
    ('搋', '弌'),  # 同上
}


VariantUnionFind = UnionFind[str]
Simplifications = Dict[str, Set[str]]


def load_ytenx_csv(
    file_path: Union[str, bytes],
    vars_unionfind: VariantUnionFind,
    simps: Simplifications,
    use_excluded: bool = True,
) -> None:
    csv_file = csv.DictReader(open(file_path))
    for row in csv_file:
        entry = row['#字']
        vars_unionfind.add(entry)
        var_fields = [f for f in ['全等', '語義交疊', '其他異體'] if f in row]
        for ch in chain.from_iterable(row[f] for f in var_fields):
            vars_unionfind.add(ch)
            if use_excluded:
                if entry in EXCLUDED_CHARS or ch in EXCLUDED_CHARS:
                    continue
                if ((entry, ch) in EXCLUDED_PAIRS
                        or (ch, entry) in EXCLUDED_PAIRS):
                    continue
            vars_unionfind.union(entry, ch)
        if (simp := row.get('簡體')) is not None:
            for ch in simp:
                simps.setdefault(entry, set()).add(ch)
        if (trad := row.get('繁體')) is not None:
            for ch in trad:
                simps.setdefault(ch, set()).add(entry)


def load_ytenx(
    vars_unionfind: Optional[VariantUnionFind] = None,
    simps: Optional[Simplifications] = None,
) -> Tuple[VariantUnionFind, Simplifications]:
    if vars_unionfind is None:
        vars_unionfind = UnionFind()
    if simps is None:
        simps = {}

    for fpath, use_excluded in [
        ('data/ytenx/JihThex.csv', True),
        ('data/ytenx/ThaJihThex.csv', True),
        ('data/yitizi.csv', False),
    ]:
        load_ytenx_csv(fpath, vars_unionfind, simps, use_excluded)

    return vars_unionfind, simps


def load_opencc(simps: Optional[Simplifications] = None) -> Simplifications:
    if simps is None:
        simps = {}

    opencc_data = chain(
        open('data/opencc/TSCharacters.txt'),
        open('data/opencc/TSPhrases.txt'),
    )
    for line in opencc_data:
        t_phrase, s_phrases = line.rstrip().split('\t')
        for s_phrase in s_phrases.split():
            assert len(t_phrase) == len(s_phrase), \
                f'Length mismatch: {repr(t_phrase)} {repr(s_phrase)}'
            for t, s in zip(t_phrase, s_phrase):
                if t != s:
                    simps.setdefault(t, set()).add(s)

    return simps
