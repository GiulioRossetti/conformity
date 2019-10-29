import unittest
from conformity import *
import networkx as nx
import numpy as np
import json


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


if __name__ == '__main__':
    unittest.main()
