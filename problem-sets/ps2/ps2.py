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
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
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



# Problem 3c: Implement directed_dfs
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
    # TODO
    pass


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
    # mit = load_map("mit_map.txt")
