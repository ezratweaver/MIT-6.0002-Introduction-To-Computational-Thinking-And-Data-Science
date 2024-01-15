"""Finger exercise: Modify the DFS algorithm to find a path that
minimizes the sum of the weights. Assume that all weights are
positive integers."""
from random import randint
"""This is pretty gross looking code, partly because the instructor has god awful coding style, and
partly because of asking me to modify an aglorithm for something it wasnt directly designed to do.
This is just a mess, but it works!"""


class Node:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def __str__(self):
        return self._name


class Edge:

    def __init__(self, src, dest):
        self._src = src
        self._dest = dest

    def get_source(self):
        return self._src

    def get_destination(self):
        return self._dest

    def __str__(self):
        return self._src.get_name() + "->" + self._dest.get_name()


class WeightedEdge(Edge):
    def __init__(self, src, dest, weight=1.0):
        super().__init__(src, dest)
        self._weight = weight

    def get_weight(self):
        return self._weight

    def __str__(self):
        return f"{self._src.get_name()}->{self._weight}" + f"{self._dest.get_name()}"


class Diagraph:

    def __init__(self):
        self._nodes = []
        self._edges = {}

    def add_node(self, node):
        if node in self._nodes:
            raise ValueError(f"{node} node is already in graph")
        else:
            self._nodes.append(node)
            self._edges[node] = []

    def add_edge(self, edge):
        src = edge.get_source()
        dest = edge.get_destination()
        weight = edge.get_weight()
        if not (src in self._nodes and dest in self._nodes):
            raise ValueError("Node not in graph")
        self._edges[src].append((dest, weight))

    def children_of(self, node):
        return self._edges[node]

    def has_nodes(self, node):
        return node in self._nodes

    def get_distance(self, node1, node2):
        for edge in self._edges[node1]:
            if edge[0] == node2:
                return edge[1]

    def __str__(self):
        result = ""
        for src in self._nodes:
            for dest in self._edges[src]:
                result = (result + src.get_name() + "->" + dest.get_name()) + "\n"
        return result[:-1]


class Graph(Diagraph):

    def __init__(self):
        super().__init__()

    def add_edge(self, edge):
        Diagraph.add_edge(self, edge)
        rev = Edge(edge.get_source(), edge.get_source())
        Diagraph.add_edge(self, rev)


def print_path(path):
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + "->"
    return result


def calc_path_distance(graph, nodelist):
    if nodelist is None:
        return 0
    pathdistance = 0
    for x in range(len(nodelist)):
        y = x + 1
        try:
            dist_val = graph.get_distance(nodelist[x], nodelist[y])
        except IndexError:
            dist_val = 0
        pathdistance += dist_val
    return pathdistance


def depth_first_search(graph, start, end, path, pathdistance, shortest, to_print=False):
    path = path + [start]
    pathdistance += calc_path_distance(graph, path)
    if to_print:
        print("Current DFS path:", print_path(path))
    if start == end:
        return path
    for node in graph.children_of(start):
        node = node[0]
        if node not in path:
            shortest_pathdistance = calc_path_distance(graph, shortest)
            if shortest is None or pathdistance < shortest_pathdistance:
                new_path = depth_first_search(graph, node, end, path, pathdistance, shortest, to_print)
                if new_path is not None:
                    shortest = new_path
    return shortest


def shortest_path(graph, start, end, to_print=False):
    return depth_first_search(graph, start, end, [], 0, None, to_print)


def test_shortest_path():
    nodes = []
    for name in range(6):
        nodes.append(Node(str(name)))
    g = Diagraph()
    for node in nodes:
        g.add_node(node)
    edges = [(0, 1), (1, 2), (2, 3), (2, 4), (3, 4), (3, 5), (0, 2), (1, 0), (3, 1), (4, 0)]
    for edge in edges:
        g.add_edge(WeightedEdge(nodes[edge[0]], nodes[edge[1]], randint(1, 10)))
    sp = shortest_path(g, nodes[0], nodes[5], to_print=True)
    print("Shortest path found by DFS:", print_path(sp))


test_shortest_path()
