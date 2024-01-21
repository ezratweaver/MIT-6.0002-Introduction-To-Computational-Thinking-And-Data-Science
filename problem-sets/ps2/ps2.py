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


def node_list_to_string(diagraph, path):
    new_list = []
    for node in path:
        new_list.append(node.get_name())
    return new_list


def string_list_to_nodes(digraph, path):
    new_list = []
    for node in path:
        new_list.append(digraph.get_node(node))
    return new_list


def get_path_weight(digraph, path_l):
    total_weight = 0
    outside_weight = 0
    for x, node in enumerate(path_l[:-1]):
        for edge in digraph.get_edges_for_node(node):
            if edge.get_destination() == path_l[x + 1]:
                total_weight += edge.get_total_distance()
                outside_weight += edge.get_outdoor_distance()
    return total_weight, outside_weight


def get_best_path(digraph, start, end, path, best_path, max_outside_dist):
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
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.
        max_outside_dist: int
            The maximum outdoor distance allowed
    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    if isinstance(start, str) or isinstance(end, str):
        start = digraph.get_node(start)
        end = digraph.get_node(end)
    path = path + [start]
    if not digraph.has_node(start) and not digraph.has_node(end):
        raise ValueError("One or both nodes are not in digraph.")
    if start == end:
        return path
    for edge in digraph.get_edges_for_node(start):
        node = edge.get_destination()
        path_weight, out_path_weight = get_path_weight(digraph, path)
        if best_path is not None:
            best_path_weight, best_out_path_weight = get_path_weight(digraph, best_path)
        else:
            best_path_weight, best_out_path_weight = float('inf'), float('inf')
        if node not in path:  # avoid cycles
            if path_weight < best_path_weight and out_path_weight <= max_outside_dist:
                new_path = get_best_path(digraph, node, end, path, best_path, max_outside_dist)
                if new_path is not None:
                    new_path_weight, new_out_path_weight = get_path_weight(digraph, new_path)
                    if new_path_weight < best_path_weight and new_out_path_weight <= max_outside_dist:
                        best_path = new_path
    return best_path


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
    results = get_best_path(digraph, start, end, [], None, max_dist_outdoors)
    if results is None:
        raise ValueError("Cannot find result that satisfies max_dist_outdoors constraints")
    if get_path_weight(digraph, results)[0] > max_total_dist:
        raise ValueError("Cannot find result that satisfies max_total_dist constraints")
    print(results)
    results = node_list_to_string(digraph, results)
    return results


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
