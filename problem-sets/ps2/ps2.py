# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding the shortest paths through MIT buildings
#

import unittest
from graph import Digraph, Node, WeightedEdge

# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
"""The graph's nodes represent buildings. The graph's edges represent the distances between said 
buildings, and the distance traveled outside of those buildings. The distances are represented 
in the graph.edges dictionary and each edge in the dictionary has the distance and outside distance
values stored."""


def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    generated_map = Digraph()
    with open(map_filename, "r") as file:
        for line in file.read().split("\n"):
            data_list = line.split(" ")
            start_node = Node(data_list[0])
            end_node = Node(data_list[1])
            new_edge = WeightedEdge(start_node, end_node, data_list[2], data_list[3])
            try:
                generated_map.add_node(start_node)
            except ValueError:
                pass
            try:
                generated_map.add_node(end_node)
            except ValueError:
                pass
            generated_map.add_edge(new_edge)
    return generated_map


# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
"""The objective function is to find the best possible path in the shortest amount of distance. 
The constraints are that some paths only go one way, and that there are many paths to take."""


# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, max_dist_outdoors):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    if not digraph.has_node(start) or not digraph.has_node(end):
        raise ValueError("Invalid nodes in parameters")

    def gen_lists(list_sub):
        empty_list = []
        children_found = 0
        for edge in digraph.get_edges_for_node(list_sub[-1]):
            children_found += 1
            child_node = edge.get_destination()
            empty_list.append(list_sub[:] + [child_node])
        if children_found == 0:
            return [list_sub]
        return empty_list

    def get_path_weight(path_l):
        total_weight = 0
        outside_weight = 0
        for x, node in enumerate(path_l[:-1]):
            for edge in digraph.get_edges_for_node(node):
                if edge.get_destination() == path_l[x+1]:
                    total_weight += edge.get_total_distance()
                    outside_weight += edge.get_outdoor_distance()
        return total_weight, outside_weight

    start_list = [[start],]
    while True:
        start_list2 = []
        for LIST in start_list:
            start_list2 += gen_lists(LIST)
        if start_list2 == start_list:
            break
        start_list = start_list2

    found_paths = []
    for branch in start_list:
        if branch[0] == start and branch[-1] == end:
            found_paths.append(branch)
    path_with_values = {}
    for pathl in found_paths:
        pathl = tuple(pathl)
        path_with_values[pathl] = get_path_weight(pathl)

    shortest_path = None
    shortest_distance = 9999999999
    for pathv in path_with_values.keys():
        if path_with_values[pathv][1] < max_dist_outdoors:
            if path_with_values[pathv][0] < shortest_distance:
                shortest_distance = path_with_values[pathv][0]
                shortest_path = pathv

    return shortest_path


def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    results = None
    if not digraph.has_node(start) or not digraph.has_node(end):
        raise ValueError("Invalid nodes in parameters")
    for edge in digraph.get_edges_for_node(start):
        child_node = edge.get_destination()
        if child_node == end:
            return [start, end]
        found_path = directed_dfs(digraph, child_node, end, max_total_dist, max_dist_outdoors)
        results = [start] + found_path
    return tuple(results)


if __name__ == "__main__":
    # unittest.main()
    # mit = load_map("mit_map.txt")
    g = Digraph()
    na = Node('a')
    nb = Node('b')
    nc = Node('c')
    g.add_node(na)
    g.add_node(nb)
    g.add_node(nc)
    e1 = WeightedEdge(na, nb, 15, 10)
    e2 = WeightedEdge(na, nc, 14, 6)
    e3 = WeightedEdge(nb, nc, 3, 1)
    g.add_edge(e1)
    g.add_edge(e2)
    g.add_edge(e3)
    print(directed_dfs(g, na, nc, 50, 20))
