# dbg_codon.py — Codon port matching the original dbg.py API (idx-based nodes)

from typing import List, Dict, Set, Optional
import copy

def reverse_complement(key: str) -> str:
    complement: Dict[str, str] = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    # reverse then complement (assume valid ACGT like original)
    key_rev: List[str] = list(key[::-1])
    i: int
    for i in range(len(key_rev)):
        c: str = key_rev[i]
        key_rev[i] = complement[c] if c in complement else c
    return "".join(key_rev)

class Node:
    def __init__(self, kmer: str) -> None:
        self._children: Set[int] = set()
        self._count: int = 0
        self.kmer: str = kmer
        self.visited: bool = False
        self.depth: int = 0
        self.max_depth_child: Optional[int] = None

    def add_child(self, idx: int) -> None:
        self._children.add(idx)

    def increase(self) -> None:
        self._count += 1

    def reset(self) -> None:
        self.visited = False
        self.depth = 0
        self.max_depth_child = None

    def get_count(self) -> int:
        return self._count

    def get_children(self) -> List[int]:
        return list(self._children)

    def remove_children(self, target: Set[int]) -> None:
        # set difference without relying on .difference_update
        if target and len(target) > 0:
            newset: Set[int] = set()
            ch: int
            for ch in self._children:
                if ch not in target:
                    newset.add(ch)
            self._children = newset

class DBG:
    def __init__(self, k: int, data_list: List[List[str]]) -> None:
        self.k: int = k
        self.nodes: Dict[int, Node] = {0: Node("__seed__")}  # seed dict type for Codon
        del self.nodes[0]
        # private
        self.kmer2idx: Dict[str, int] = {}
        self.kmer_count: int = 0
        # build
        self._check(data_list)
        self._build(data_list)

    def _check(self, data_list: List[List[str]]) -> None:
        # check data list (match original assertions)
        assert len(data_list) > 0
        assert self.k <= len(data_list[0][0])

    def _build(self, data_list: List[List[str]]) -> None:
        k: int = self.k
        data: List[str]
        for data in data_list:
            original: str
            for original in data:
                rc: str = reverse_complement(original)
                # match original bound: len(original) - self.k - 1
                limit: int = len(original) - k - 1
                if limit <= 0:
                    continue
                i: int
                for i in range(limit):
                    self._add_arc(original[i:i+k], original[i+1:i+1+k])
                    self._add_arc(rc[i:i+k],        rc[i+1:i+1+k])

    def show_count_distribution(self) -> None:
        # optional: keep behavior (safe in Codon)
        count: List[int] = [0] * 30
        idx: int
        for idx in self.nodes:
            c = self.nodes[idx].get_count()
            if 0 <= c < len(count):
                count[c] += 1
        print(count[0:10])

    def _add_node(self, kmer: str) -> int:
        if kmer in self.kmer2idx:
            idx: int = self.kmer2idx[kmer]
            self.nodes[idx].increase()
            return idx
        else:
            idx = self.kmer_count
            self.kmer2idx[kmer] = idx
            self.nodes[idx] = Node(kmer)
            self.nodes[idx].increase()
            self.kmer_count = idx + 1
            return idx

    def _add_arc(self, kmer1: str, kmer2: str) -> None:
        idx1: int = self._add_node(kmer1)
        idx2: int = self._add_node(kmer2)
        self.nodes[idx1].add_child(idx2)

    def _get_count(self, child: int) -> int:
        return self.nodes[child].get_count()

    def _get_sorted_children(self, idx: int) -> List[int]:
        children: List[int] = self.nodes[idx].get_children()
        children.sort(key=self._get_count, reverse=True)
        return children

    def _get_depth(self, idx: int) -> int:
        node: Node = self.nodes[idx]
        if not node.visited:
            node.visited = True
            children: List[int] = self._get_sorted_children(idx)
            max_depth: int = 0
            max_child: Optional[int] = None
            ch: int
            for ch in children:
                depth: int = self._get_depth(ch)
                if depth > max_depth:
                    max_depth = depth
                    max_child = ch
            node.depth = max_depth + 1
            node.max_depth_child = max_child
        return node.depth

    def _reset(self) -> None:
        idx: int
        for idx in self.nodes.keys():
            self.nodes[idx].reset()

    def _get_longest_path(self) -> List[int]:
        max_depth: int = 0
        max_idx: Optional[int] = None
        idx: int
        for idx in self.nodes.keys():
            depth: int = self._get_depth(idx)
            if depth > max_depth:
                max_depth = depth
                max_idx = idx
        path: List[int] = []
        while max_idx is not None:
            path.append(max_idx)
            max_idx = self.nodes[max_idx].max_depth_child
        return path

    def _delete_path(self, path: List[int]) -> None:
        i: int
        for i in path:
            if i in self.nodes:
                del self.nodes[i]
        path_set: Set[int] = set(path)
        idx: int
        for idx in self.nodes.keys():
            self.nodes[idx].remove_children(path_set)

    def _concat_path(self, path: List[int]) -> Optional[str]:
        if len(path) < 1:
            return None
        concat: str = copy.copy(self.nodes[path[0]].kmer)
        i: int
        for i in range(1, len(path)):
            concat += self.nodes[path[i]].kmer[-1]
        return concat

    def get_longest_contig(self) -> Optional[str]:
        self._reset()
        path: List[int] = self._get_longest_path()
        contig: Optional[str] = self._concat_path(path)
        self._delete_path(path)
        return contig
