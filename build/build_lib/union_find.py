from typing import Iterable


class UnionFind[T]:

    def __init__(self, it: Iterable[T] = None):
        self._elems = list[T]()
        self._index = dict[T, int]()
        self._uf = list[int]()
        if it is not None:
            for e in it:
                self.add(e)

    def __len__(self) -> int:
        return len(self._elems)
    
    def __contains__(self, elem: T) -> bool:
        return elem in self._index

    def add(self, elem: T) -> bool:
        if elem in self._index:
            return False
        idx = len(self._uf)
        self._index[elem] = idx
        self._elems.append(elem)
        self._uf.append(-1)
        return True

    def find(self, elem: T) -> T:
        return self._elems[self._find_idx(self._index[elem])]

    def union(self, elem1: T, elem2: T) -> bool:
        return self._union_idx(self._index[elem1], self._index[elem2])

    def same_set(self, elem1: T, elem2: T) -> bool:
        return (self._find_idx(self._index[elem1])
                == self._find_idx(self._index[elem2]))

    def dump(self) -> dict[T, list[T]]:
        res = dict[T, list[T]]()
        for e in self._elems:
            res.setdefault(self.find(e), []).append(e)
        return res

    def _find_idx(self, idx: int) -> int:
        if self._uf[idx] < 0:
            return idx
        else:
            res = self._uf[idx] = self._find_idx(self._uf[idx])
            return res

    def _union_idx(self, idx1: int, idx2: int) -> bool:
        idx1 = self._find_idx(idx1)
        idx2 = self._find_idx(idx2)
        if idx1 == idx2:
            return False
        if self._uf[idx1] <= self._uf[idx2]:
            self._uf[idx1] -= 1
            self._uf[idx2] = idx1
        else:
            self._uf[idx2] -= 1
            self._uf[idx1] = idx2
        return True
