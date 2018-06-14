# 6.0002 Problem Set 2
# Graph Optimization
# Name: Elaheh Ahmadi
# Collaborators: TA(s)
# Time: +10h

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer: The graph nodes represent the buildings and the edges are paths from one buildig to other buildings and the
# distance represent the distance from one building to another building


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following three positive
        integers, separated by a blank space:
            From To TotalDistance
        e.g.
            32 76 54
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print("Loading map from file...")
    # opens the file
    map_file = open(map_filename)
    # Reads the file
    map_str = map_file.read()
    # Closes the file
    map_file.close()
    # Gets all of the lines in the file and put them into a list
    map_lines = map_str.split('\n')
    graph = Digraph()
    # Iterates over the lines in the file and creates the graph
    for line in map_lines:
        data = line.split()
        if len(data) > 1:
            node_1 = Node(data[0])
            node_2 = Node(data[1])
            edge = WeightedEdge(node_1, node_2, int(data[2]))
            if not graph.has_node(node_1):
                graph.add_node(node_1)
            if not graph.has_node(node_2):
                graph.add_node(node_2)
            graph.add_edge(edge)
    return graph

# Problem 2c: Testing load_map
# g = load_map('test_mit_map_2.txt')
# print('Printing graph:')
# print(g)
# print(g.get_nodes())
# nodes = g.get_nodes()
# print(nodes)
# node = Node('1')
# print(g.has_node(node))
# print(g.get_edges_for_node(g.get_nodes()[0]))
# Problem 3: Finding the Shortest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer: Constraint is the max_sum_buildings. Objective function would be trying to find the shortest path between two
# buildings by using DFS and also considering the constraint.
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_sum_buildings, best_dist, best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: instance of Digraph or one of its subclasses
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            sum of building numbers.
        max_sum_buildings: int
            Maximum sum of building numbers a path can visit
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple of the form (best_dist, best_path).
        The first item is an integer, the length (distance traveled)
        of the best path.
        The second item is the shortest-path from start to end, represented by
        a list of building numbers (in strings).

        If there exists no path that satisfies max_total_dist and
        max_sum_buildings constraints, then return None.
    """
    # Checkes if start and end nodes are valid and inside the graph
    if Node(start) not in digraph.get_nodes() or Node(end) not in digraph.get_nodes():
        raise ValueError('Either start or end is not in the nodes.')
    # Checks if we reached the end of the graph and we did not go over the limit
    if start == end and path[2] <= max_sum_buildings:
        return path[1], path[0]
    # Checks if we did not go ove rthe limit for sum buildings
    if path[2] > max_sum_buildings:
        return None, None
    # Iterates over the edges of each node and recursively finds the new distance and new path
    for edge in digraph.get_edges_for_node(Node(start)):
        dest_name = edge.get_destination().get_name()
        if dest_name not in path[0]:
            if best_path == None or path[1] < best_dist:
                start_name = dest_name
                temp_path = [path[0][:], path[1], path[2]]
                temp_path[0] += [start_name]
                temp_path[1] += edge.get_total_distance()
                temp_path[2] += int(start_name)
                (new_dist, new_path) = get_best_path(digraph, start_name, end, temp_path, max_sum_buildings, best_dist, best_path)
                # Checks if the new distance that we found is less than the best distance
                if new_path != None and new_dist < best_dist:
                    best_path = new_path
                    best_dist = new_dist
    return best_dist, best_path

# print(g.get_edges_for_node(Node('13')))
# print(get_best_path(g,  '1', '16', [['1'],0,0], 100, 100000000,None))


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_sum_buildings):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the sum of building numbers on this path must
    not exceed max_sum_buildings.

    Parameters:
        digraph: instance of Digraph or one of its subclasses
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_sum_buildings: int
            Maximum sum of building numbers a path can visit

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings).

        If there exists no path that satisfies max_total_dist and
        max_sum_buildings constraints, then raises a ValueError.
    """
    # Initializing the best_distance equal to maximum possible value
    best_dist = max_total_dist
    # Initializing the best path to None so that the recursive function works
    best_path = None
    # Based on my implementation the path should be initialized as followed
    path = [[start],0,int(start)]
    # Finding the best distance and best path by using the get_best_path that I implemented
    best_dist, best_path = get_best_path(digraph, start, end, path,
                                         max_sum_buildings, best_dist,
                                         best_path)
    if best_path is None:
        raise ValueError("No path from {} to {}".format(start, end))
    return best_path


class Ps2Test(unittest.TestCase):
    LARGE_NUM_NODES = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 133)

    def _print_path_description(self, start, end, total_dist, buildings_sum):
        constraint = ""
        if buildings_sum != Ps2Test.LARGE_NUM_NODES:
            constraint = "visiting buildings whose numbers add up to no more than {}".format(
                buildings_sum)
        if total_dist != Ps2Test.LARGE_NUM_NODES:
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
                   total_dist=LARGE_NUM_NODES,
                   buildings_sum=LARGE_NUM_NODES):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, buildings_sum)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, buildings_sum)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_path_multi_options(self,
                   expectedPath,
                   total_dist=LARGE_NUM_NODES,
                   buildings_sum=LARGE_NUM_NODES):
        start, end = expectedPath[0][0], expectedPath[0][-1]
        self._print_path_description(start, end, total_dist, buildings_sum)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, buildings_sum)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertTrue(dfsPath in expectedPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_NUM_NODES,
                              buildings_sum=LARGE_NUM_NODES):
        self._print_path_description(start, end, total_dist, buildings_sum)
        try:
            path = directed_dfs(self.graph, start, end, total_dist, buildings_sum)
            print(path)
            self.fail()
        except:
            with self.assertRaises(ValueError):
                directed_dfs(self.graph, start, end, total_dist, buildings_sum)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_unlimited_sum(self):
        self._test_path(
            expectedPath=['10','13', '9'], buildings_sum=Ps2Test.LARGE_NUM_NODES)

    def test_path_smaller_sum(self):
        self._test_path(
            expectedPath=['10','4', '9'], buildings_sum=23)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_with_no_limit_sum(self):
        self._test_path_multi_options(
            expectedPath=[['1', '3', '10', '13', '31', '37'],['1', '5', '7', '9', '33', '35', '37']],
            buildings_sum=Ps2Test.LARGE_NUM_NODES)

    def test_with_exact_sum(self):
        self._test_path(
            expectedPath=['1', '3', '10', '13', '31', '37'],
            buildings_sum=sum([1, 3,10, 13, 31, 37]))

    def test_with_exact_sum_minus_one(self):
        self._test_path(
            expectedPath=['1', '2', '10', '13', '31', '37'],
            buildings_sum=sum([1, 3,10, 13, 31, 37])-1)

    def test_with_start_end_sum(self):
        self._test_path(
            expectedPath=['32', '76'],
            buildings_sum=108)

    def test_without_start_end_sum(self):
        self._test_path(
            expectedPath=['32', '57', '76'],
            buildings_sum=Ps2Test.LARGE_NUM_NODES)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '8', '16', '56', '32'], buildings_sum=Ps2Test.LARGE_NUM_NODES  )

    def test_impossible_path1(self):
        self._test_impossible_path('2', '1', buildings_sum=2)

    def test_impossible_path2(self):
        self._test_impossible_path('31', '38', buildings_sum=39)

    def test_impossible_path3(self):
        self._test_impossible_path('37', '33', buildings_sum=69)

    def test_impossible_path4(self):
        self._test_impossible_path('1', '10', buildings_sum=11)



if __name__ == "__main__":
    unittest.main(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(Ps2Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
