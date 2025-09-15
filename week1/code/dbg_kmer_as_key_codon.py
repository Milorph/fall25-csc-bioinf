#!/usr/bin/env python3
# dbg_kmer_as_key_codon.py — Codon-compatible De Bruijn graph (k-mer as key)
from typing import Dict, List, Optional, Set

def reverse_complement(key: str) -> str:
    comp = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    # reverse then complement (assumes input is uppercase A/C/G/T)
    return ''.join(comp[ch] for ch in key[::-1])

class Node:
    __slots__ = ("_children", "_count", "visited", "depth", "max_depth_child")
    def __init__(self) -> None:
        self._children: Set[str] = set()
        self._count: int = 0
        self.visited: bool = False
        self.depth: int = 0
        self.max_depth_child: Optional[str] = None

    def add_child(self, kmer: str) -> None:
        self._children.add(kmer)

    def increase(self) -> None:
        self._count += 1

    def reset(self) -> None:
        self.visited = False
        self.depth = 0
        self.max_depth_child = None

    def get_count(self) -> int:
        return self._count

    def get_children(self) -> List[str]:
        return list(self._children)

    def remove_children(self, target: Set[str]) -> None:
        if not target:
            return
        self._children = self._children - target

class DBG:
    def __init__(self, k: int, data_list: List[List[str]]) -> None:
        self.k: int = k
        self.nodes: Dict[str, Node] = {}
        self._check(data_list)
        self._build(data_list)

    def _check(self, data_list: List[List[str]]) -> None:
        assert len(data_list) > 0
        # guard against empty sequences
        assert len(data_list[0]) > 0 and len(data_list[0][0]) >= self.k

    def _build(self, data_list: List[List[str]]) -> None:
        k = self.k
        for data in data_list:
            for original in data:
                rc = reverse_complement(original)
                lim = len(original) - k - 1
                if lim < 0:
                    continue
                for i in range(lim):
                    self._add_arc(original[i:i+k], original[i+1:i+1+k])
                    self._add_arc(rc[i:i+k],        rc[i+1:i+1+k])

    def _add_node(self, kmer: str) -> None:
        node = self.nodes.get(kmer)
        if node is None:
            node = Node()
            self.nodes[kmer] = node
        node.increase()

    def _add_arc(self, kmer1: str, kmer2: str) -> None:
        self._add_node(kmer1)
        self._add_node(kmer2)
        self.nodes[kmer1].add_child(kmer2)

    def _get_count(self, child: str) -> int:
        return self.nodes[child].get_count()

    def _get_sorted_children(self, kmer: str) -> List[str]:
        children = self.nodes[kmer].get_children()
        children.sort(key=self._get_count, reverse=True)
        return children

    def _get_depth(self, kmer: str) -> int:
        node = self.nodes[kmer]
        if not node.visited:
            node.visited = True
            children = self._get_sorted_children(kmer)
            max_depth = 0
            max_child: Optional[str] = None
            for child in children:
                d = self._get_depth(child)
                if d > max_depth:
                    max_depth = d
                    max_child = child
            node.depth = max_depth + 1
            node.max_depth_child = max_child
        return node.depth

    def _reset(self) -> None:
        # Iterate over keys list to avoid surprises if dict changes elsewhere
        for kmer in list(self.nodes.keys()):
            self.nodes[kmer].reset()

    def _get_longest_path(self) -> List[str]:
        max_depth = 0
        max_kmer: Optional[str] = None
        for kmer in self.nodes.keys():
            d = self._get_depth(kmer)
            if d > max_depth:
                max_depth = d
                max_kmer = kmer
        path: List[str] = []
        while max_kmer is not None:
            path.append(max_kmer)
            max_kmer = self.nodes[path[-1]].max_depth_child
        return path

    def _delete_path(self, path: List[str]) -> None:
        # Remove nodes in path
        for kmer in path:
            if kmer in self.nodes:
                del self.nodes[kmer]
        # Remove edges pointing to removed nodes
        path_set = set(path)
        for kmer in list(self.nodes.keys()):
            self.nodes[kmer].remove_children(path_set)

    def _concat_path(self, path: List[str]) -> str:
        if not path:
            return ""
        concat = path[0]  # strings are immutable; copy() unnecessary
        for i in range(1, len(path)):
            concat += path[i][-1]
        return concat

    def get_longest_contig(self) -> Optional[str]:
        self._reset()
        path = self._get_longest_path()
        if not path:
            return None
        contig = self._concat_path(path)
        self._delete_path(path)
        return contig
