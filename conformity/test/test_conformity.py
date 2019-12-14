import unittest
from conformity import *
import networkx as nx
import numpy as np
import json
import random

class ConformityTestCase(unittest.TestCase):

    def test_attribute_conformity(self):
        g = nx.karate_club_graph()
        nodes = list(g.nodes())
        for n in nodes:
            g.add_node(n, pippo="si", topolino="op")

        res = attribute_conformity(g, list(np.arange(1, 4, 0.2)), ['club', 'pippo', 'topolino'], profile_size=3)

        with open(f"conformity.json", "w") as o:
            json.dump(res, o)

        for k, v in res.items():
            for z, t in v.items():
                for _, val in t.items():
                    self.assertTrue(-1 <= val <= 1)

    def test_hierarchical_attribute_conformity(self):

        labels = ['one', 'two', 'three', 'four']
        age = ["A", "B", "C"]
        hierarchy = {'labels': {'one': 1, 'two': 2, 'three': 3, 'four': 4}}

        g = nx.barabasi_albert_graph(100, 5)

        for node in g.nodes():
            g.add_node(node, labels=random.choice(labels), age=random.choice(age))

        res = attribute_conformity(g, list(np.arange(1, 4, 0.2)), ['labels', 'age'], profile_size=2,
                                   hierarchies=hierarchy)

        with open(f"conformity_hierarchy.json", "w") as o:
            json.dump(res, o)

        for k, v in res.items():
            for z, t in v.items():
                for _, val in t.items():
                    self.assertTrue(-1 <= val <= 1)


if __name__ == '__main__':
    unittest.main()
