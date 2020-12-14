#! /usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(__file__))  # nopep8

import json
from typing import Dict, List, Set

from build_lib import (
    load_ytenx,
    load_opencc,
    make_yitizi_groups,
    make_yitizi_json
)


vars_unionfind, simps = load_ytenx()
load_opencc(simps)
varsets = vars_unionfind.dump()

yitizi_groups = make_yitizi_groups(varsets, simps)
yitizi_json = make_yitizi_json(yitizi_groups)


def save_json(yitizi_json: Dict[str, str] = yitizi_json) -> None:
    json.dump(yitizi_json, open('yitizi.json', 'w'),
              ensure_ascii=False, indent=0, separators=(',', ':'))


def save_files(
    varsets: Dict[str, List[str]] = varsets,
    simps: Dict[str, Set[str]] = simps,
    yitizi_groups: List[str] = yitizi_groups,
) -> None:
    with open('yitizi-varsets', 'w') as outfile:
        for varset in varsets.values():
            if len(varset) == 1:
                continue
            print(''.join(varset), file=outfile)

    with open('yitizi-simps', 'w') as outfile:
        for tchar, schars in simps.items():
            print(tchar, ''.join(sorted(schars)), sep='', file=outfile)

    with open('yitizi-groups', 'w') as outfile:
        for groups_line in yitizi_groups:
            print(groups_line, file=outfile)


save_json()
