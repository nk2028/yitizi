#!/usr/bin/env pyton

import os
import sys

sys.path.append(os.path.dirname(__file__))

import json

from build_lib import UnionFind, load_all, make_graph, sorted_graph


def dump(equiv: UnionFind[str], inter: set[str], simp: dict[str, set[str]]):
    with open('yitizi-equiv', 'w') as fout:
        dumped = equiv.dump()
        for chs in dumped.values():
            if len(chs) == 1:
                continue
            print('=', ''.join(chs), sep='', file=fout)
    with open('yitizi-inter', 'w') as fout:
        for chs in inter:
            print(chs, file=fout)
    with open('yitizi-simp', 'w') as fout:
        for t, ss in simp.items():
            print(t, '>', ''.join(ss), sep='', file=fout)


def main():
    data = load_all()
    #dump(*data)
    graph = sorted_graph(make_graph(*data))
    out_data = {k: ''.join(v) for k, v in graph.items()}
    with open('yitizi.json', 'w', newline='') as fout:
        json.dump(out_data, fout, ensure_ascii=False, indent=0, separators=(',', ':'))


if __name__ == '__main__':
    main()
