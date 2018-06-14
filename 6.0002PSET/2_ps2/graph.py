# 6.0002 Problem Set 2
# Graph Optimization
# Name: Elaheh Ahmadi
# Collaborators: N/A
# Time: +2h

import unittest

#
# A set of data structures to represent graphs
#

class Node(object):
    """Represents a node in the graph"""
    def __init__(self, name):
        self.name = str(name)

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        # This function is necessary so that Nodes can be used as
        # keys in a dictionary, even though Nodes are mutable
        return self.name.__hash__()
        
    def get_building_num(self):
        return int(self.name)


class Edge(object):
    """Represents an edge in the dictionary. Includes a source Node and
    a destination Node."""
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def get_source(self):
        return self.src

    def get_destination(self):
        return self.dest

    def __str__(self):
        return '{}->{}'.format(self.src, self.dest)


class WeightedEdge(Edge):
    """An Edge with an integer weight"""
    def __init__(self, src, dest, total_distance):
        Edge.__init__(self,src, dest)
        self.distance = int(total_distance)
        
    def get_total_distance(self):
        return self.distance

    def __str__(self):
        return '{}->{} ({})'.format(self.src, self.dest, self.distance)


class Digraph(object):
    """Represents a directed graph of Node and Edge objects"""
    def __init__(self):
        self.nodes = set([])
        self.edges = {}  # must be a dict of Node -> list of edges

    def __str__(self):
        edge_strs = []
        for edges in self.edges.values():
            for edge in edges:
                edge_strs.append(str(edge))
        edge_strs = sorted(edge_strs)  # sort alphabetically
        return '\n'.join(edge_strs)  # concat edge_strs with "\n"s between them

    def get_nodes(self):
        return self.nodes

    def get_edges_for_node(self, node):
        if node in self.edges:
            return self.edges[node]
        # It has to return an empty list if the node is dead end
        return []

    def has_node(self, node):
        return node in self.nodes

    def add_node(self, node):
        """Adds a Node object to the Digraph. Raises a ValueError if it is
        already in the graph."""
        # Checks if the node is already in the node set or not before adding it
        if node in self.nodes:
            raise ValueError(' Node already in graph.')
        else:
            self.nodes.add(node)

    def add_edge(self, edge):
        """Adds an Edge or WeightedEdge instance to the Digraph. Raises a
        ValueError if either of the nodes associated with the edge is not
        in the  graph."""
        # Checks if the edge is valid before adding it to the edge dictionary
        if edge.get_source() not in self.nodes or edge.get_destination() not in self.nodes:
            raise ValueError('Either source or destination node does not exist in the graph.')
        else:
            if edge.get_source() not in self.edges:
                self.edges[edge.get_source()] = [edge]
            else:
                self.edges[edge.get_source()].append(edge)

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.g = Digraph()
        self.na = Node('a')
        self.nb = Node('b')
        self.nc = Node('c')
        self.g.add_node(self.na)
        self.g.add_node(self.nb)
        self.g.add_node(self.nc)
        self.e1 = WeightedEdge(self.na, self.nb, 15)
        self.e2 = WeightedEdge(self.na, self.nc, 14)
        self.e3 = WeightedEdge(self.nb, self.nc, 3)
        self.g.add_edge(self.e1)
        self.g.add_edge(self.e2)
        self.g.add_edge(self.e3)

    def test_weighted_edge_str(self):
        self.assertEqual(str(self.e1), "a->b (15)")
        self.assertEqual(str(self.e2), "a->c (14)")
        self.assertEqual(str(self.e3), "b->c (3)")

    def test_weighted_edge_total_distance(self):
        self.assertEqual(self.e1.get_total_distance(), 15)
        self.assertEqual(self.e2.get_total_distance(), 14)
        self.assertEqual(self.e3.get_total_distance(), 3)


    def test_add_edge_to_nonexistent_node_raises(self):
        node_not_in_graph = Node('q')
        no_src = WeightedEdge(self.nb, node_not_in_graph, 5)
        no_dest = WeightedEdge(node_not_in_graph, self.na, 5)

        with self.assertRaises(ValueError):
            self.g.add_edge(no_src)
        with self.assertRaises(ValueError):
            self.g.add_edge(no_dest)

    def test_add_existing_node_raises(self):
        with self.assertRaises(ValueError):
            self.g.add_node(self.na)

    def test_graph_str(self):
        expected = "a->b (15)\na->c (14)\nb->c (3)"
        self.assertEqual(str(self.g), expected)


if __name__ == "__main__":
    unittest.main()
    # g = Digraph()
    # na = Node('a')
    # nb = Node('b')
    # nc = Node('c')
    # g.add_node(na)
    # g.add_node(nb)
    # g.add_node(nc)
    # e1 = WeightedEdge(na, nb, 15)
    # e2 = WeightedEdge(na, nc, 14)
    # e3 = WeightedEdge(nb, nc, 3)
    # g.add_edge(e1)
    # g.add_edge(e2)
    # g.add_edge(e3)
    data = [32, 36, 70]
    g = Digraph()
    na  = Node('32')
    nb = Node('36')
    g.add_node(na)
    g.add_node(nb)
    e1 = WeightedEdge(na, nb, 70)
    g.add_edge(e1)
    print('na:', na)
    print('nb:', nb)
    print('e1:', e1)
    print('g:', g)
