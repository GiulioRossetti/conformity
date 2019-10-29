import networkx as nx
from itertools import combinations
from tqdm import tqdm
from collections import defaultdict

__all__ = ["attribute_conformity"]


def __label_frequency(g: nx.Graph, u: object, nodes: list, labels: list) -> float:
    """
    Compute the similarity of node profiles

    :param g: a networkx Graph object
    :param u: node id
    :param v: node id
    :param labels: list of node categorical labels
    :return: node profiles similarity score in [-1, 1]
    """
    s = 1
    for l in labels:
        a_u = g.node[u][l]
        # set of nodes at given distance
        sgn = {}
        for v in nodes:
            sgn[v] = 1 if a_u == g.node[v][l] else -1
            v_neigh = list(g.neighbors(v))
            # compute the frquency for give node at distance n over neighbors label
            f_label = (len([x for x in v_neigh if g.node[x][l] == g.node[v][l]]) / len(v_neigh))
            f_label = f_label if f_label > 0 else 1
            sgn[v] *= f_label
        s *= sum(sgn.values())/len(nodes)

    return s


def __normalize(u: object, scores: list, max_dist: int, alphas: list):
    """
    Normalize the computed scores in [-1, 1]

    :param u: node
    :param scores: datastructure containing the computed scores for u
    :param alphas: list of damping factor
    :return: scores updated
    """
    for alpha in alphas:
        norm = sum([(d ** -alpha) for d in range(1, max_dist+1)])

        for profile in scores[str(alpha)]:
            scores[str(alpha)][profile][u] /= norm

    return scores


def attribute_conformity(g, alphas: list, labels: list, profile_size: int = 1) -> dict:
    """
    Compute the Attribute-Profile Conformity for the considered graph
    :param g: a networkx Graph object composed by a single component
    :param alphas: list of damping factors
    :param labels: list of node categorical labels
    :param profile_size:
    :return: clumpiness value for each node in [-1, 1]

    -- Example --
    >> g = nx.karate_club_graph()
    >> pc = profile_conformity(g, 1, ['club'])
    """

    if not nx.is_connected(g):
        raise nx.NetworkXError("The provided graph is not connected")

    if profile_size > len(labels):
        raise ValueError("profile_size must be <= len(labels)")

    if len(alphas) < 1 or len(labels) < 1:
        raise ValueError("At list one value must be specified for both alphas and labels")

    profiles = []
    for i in range(1, profile_size+1):
        profiles.extend(combinations(labels, i))

    # Attribute value frequency
    labels_value_frequency = defaultdict(lambda: defaultdict(int))
    for _, metadata in g.nodes.items():
        for k, v in metadata.items():
            labels_value_frequency[k][v] += 1

    # Normalization
    df = defaultdict(lambda: defaultdict(int))
    for k, v in labels_value_frequency.items():
        tot = 0
        for p, c in v.items():
            tot += c

        for p, c in v.items():
            df[k][p] = c/tot

    res = {str(a): {"_".join(profile): {n: 0 for n in g.nodes()} for profile in profiles} for a in alphas}

    for u in tqdm(g.nodes()):
        sp = dict(nx.shortest_path_length(g, u))

        dist_to_nodes = defaultdict(list)
        for node, dist in sp.items():
            dist_to_nodes[dist].append(node)
        sp = dist_to_nodes

        for dist, nodes in sp.items():
            if dist != 0:
                for profile in profiles:
                    sim = __label_frequency(g, u, nodes, list(profile))

                    for alpha in alphas:
                        partial = sim / (dist**alpha)
                        p_name = "_".join(profile)
                        res[str(alpha)][p_name][u] += partial

        res = __normalize(u, res, max(sp.keys()), alphas)

    return res
