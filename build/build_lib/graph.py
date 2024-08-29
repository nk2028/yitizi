from collections.abc import Iterable
from typing import Sequence, TypeVar

from .union_find import UnionFind


T = TypeVar('T')
Graph = dict[T, set[T]]


def connect(graph: Graph[T], u: T, v: T):
    if u == v:
        graph.setdefault(u, set())
        return
    graph.setdefault(u, set()).add(v)
    graph.setdefault(v, set()).add(u)


def connect_all(graph: Graph[T], vertices: Sequence[T]):
    for i, u in enumerate(vertices[:-1]):
        for v in vertices[i + 1 :]:
            connect(graph, u, v)


def connect_groups(graph: Graph[T], us: Iterable[T], vs: Iterable[T]):
    for u in us:
        for v in vs:
            connect(graph, u, v)


def get_group(union_find: UnionFind[T], dumped: dict[T, list[T]], elem: T) -> list[T]:
    if elem in union_find:
        return dumped[union_find.find(elem)]
    else:
        return [elem]


def make_graph(
    equivalents: UnionFind[str],
    intersecting_groups: set[str],
    simplifications: dict[str, set[str]],
) -> Graph:
    graph: Graph[str] = {}

    equiv_groups = equivalents.dump()
    for group in equiv_groups.values():
        connect_all(graph, group)

    for group in intersecting_groups:
        for i, u_char in enumerate(group[:-1]):
            for v_char in group[i + 1 :]:
                us = get_group(equivalents, equiv_groups, u_char)
                vs = get_group(equivalents, equiv_groups, v_char)
                connect_groups(graph, us, vs)

    graph_without_simp = {k: v.copy() for k, v in graph.items()}

    for trad_char, simps in simplifications.items():
        trads = [trad_char]
        trads.extend(graph_without_simp.get(trad_char, []))
        connect_groups(graph, trads, simps)
        connect_all(graph, list(simps))

    return graph


def sorted_graph(graph: Graph[T]) -> dict[T, list[T]]:
    return {k: sorted(graph[k]) for k in sorted(graph)}
