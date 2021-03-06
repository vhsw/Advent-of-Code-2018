"""Day 18 Answers part 1"""
import heapq
from typing import (
    NamedTuple,
    Dict,
    Set,
    Tuple,
    Optional,
    FrozenSet,
    Iterator,
)
from collections import deque
from itertools import combinations
import networkx as nx

INPUT = "2019/Day 18/input"


class Vec(NamedTuple):
    """2D Vec"""

    line: int
    col: int

    def __add__(self, other):
        return Vec(self.line + other.line, self.col + other.col)


def parse(data: str) -> Tuple[Dict[Vec, str], Dict[str, Vec]]:
    """Parse map"""
    field: Dict[Vec, str] = {}
    objects: Dict[str, Vec] = {}
    for line, row in enumerate(data.splitlines()):
        for col, char in enumerate(row):
            if char != "#":
                p = Vec(line, col)
                field[p] = char
                if char != ".":
                    objects[char] = p
    return field, objects


def neighbors(p: Vec) -> Iterator[Vec]:
    """yield points near p"""
    for dp in [
        Vec(0, 1),
        Vec(0, -1),
        Vec(1, 0),
        Vec(-1, 0),
    ]:
        yield p + dp


def field_graph(field, objects) -> nx.Graph:
    """make graph form field"""
    graph = nx.Graph()
    entrance = objects["@"]
    visited: Set[Vec] = set()
    queue = deque([entrance])
    while queue:
        src = queue.popleft()
        if src in visited:
            continue
        visited.add(src)
        for dst in neighbors(src):
            if dst in field:
                graph.add_edge(src, dst)
                queue.append(dst)
    return graph


def key_to_key_graph(fg, field, objects) -> nx.Graph:
    """return graph with distances between nodes, required open doors and collected keys"""
    pois = [obj for obj in objects if obj.islower() or obj == "@"]
    graph = nx.Graph()
    for obj1, obj2 in combinations(pois, 2):
        p1 = objects[obj1]
        p2 = objects[obj2]
        path = nx.shortest_path(fg, p1, p2)
        doors = frozenset(field[p] for p in path if field[p].isupper())
        keys = frozenset(field[p].upper() for p in path if field[p].islower())
        if len(keys) <= 2:
            closed_doors = doors - keys
            graph.add_edge(p1, p2, length=len(path) - 1, doors=closed_doors, keys=keys)
    return graph


def dijkstra(k2k: nx.Graph, start: Vec, all_doors) -> int:
    """return shortest path between all keys or rises ValueError"""
    visited: Set[Tuple[Vec, FrozenSet[str]]] = set()
    Node = Tuple[int, Vec, FrozenSet[str]]
    node: Node = (0, start, frozenset(""))
    queue = [node]
    while queue:
        cost, pos, open_doors = heapq.heappop(queue)
        if (pos, open_doors) in visited:
            continue
        visited.add((pos, open_doors))

        if open_doors == all_doors:
            return cost

        available_keys = []
        for n, a in k2k[pos].items():
            if open_doors >= a["doors"]:
                available_keys.append(n)
        for dst in available_keys:
            new_cost = cost + k2k.edges[(pos, dst)]["length"]
            keys = k2k.edges[(pos, dst)]["keys"] | open_doors
            heapq.heappush(queue, (new_cost, dst, keys))
    raise ValueError


def shortest_path_length(data) -> int:
    """return shortest path between all keys"""
    field, objects = parse(data)
    fg = field_graph(field, objects)
    k2k = key_to_key_graph(fg, field, objects)
    entrance = objects["@"]
    all_doors = set(k.upper() for k in objects if k.islower())
    return dijkstra(k2k, entrance, all_doors)


def shortest_path_length4(data) -> int:
    """return shortest path between all keys"""
    field, objects = parse(data)
    fg = field_graph(field, objects)
    k2k = key_to_key_graph(fg, field, objects)
    entrance = objects["@"]
    all_doors = set(k.upper() for k in objects if k.islower())
    return dijkstra(k2k, entrance, all_doors)


def part1():
    """Part 1 answer"""
    with open(INPUT) as data:
        data = data.read()
    return shortest_path_length(data)


def part2():
    """Part 2 answer"""
    with open(INPUT) as data:
        data = data.read()

    return shortest_path_length4(data)


if __name__ == "__main__":
    ANSWER = part1()
    print(f"Part 1: {ANSWER}")
