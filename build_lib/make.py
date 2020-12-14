from typing import Dict, List, Set

VariantSets = Dict[str, List[str]]
Simplifications = Dict[str, Set[str]]


def make_yitizi_groups(
    varsets: VariantSets,
    simps: Simplifications
) -> List[str]:
    yitizi_groups = []
    trad_seen: Set[str] = set()
    for varset in varsets.values():
        group = set(varset)
        trad_seen |= group
        for ch in varset:
            if (schars := simps.get(ch)) is not None:
                group |= schars
        if len(group) == 1:
            continue
        yitizi_groups.append(''.join(sorted(group)))
    for tchar, schars in simps.items():
        if tchar in trad_seen:
            continue
        yitizi_groups.append(tchar + ''.join(sorted(schars)))
    yitizi_groups.sort()
    return yitizi_groups


def make_yitizi_json(yitizi_groups: List[str]) -> Dict[str, str]:
    obj: Dict[str, Set[str]] = {}
    for group in yitizi_groups:
        for i, ch in enumerate(group):
            v = obj.setdefault(ch, set())
            v.update(group[:i])
            v.update(group[i+1:])
    json_obj = dict((k, ''.join(sorted(v))) for k, v in obj.items())
    return json_obj
