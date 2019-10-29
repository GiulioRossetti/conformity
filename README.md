# Conformity
``Conformity`` implements the path-aware homophily measure as introduced in:

> Conformity: a Path-Aware Homophily measure for Node-Attributed Networks
> G. Rossetti, S. Citraro and L. Milli1
> (Submitted to CompleNet 2020)

## Installation

``Conformity`` *requires* python>=3.6.

To install the latest version of our library just download (or clone) the current project, open a terminal and run the following commands:

```bash
pip install -r requirements.txt
pip install .
```

Alternatively use pip:
```bash
pip install conformity
```

## Usage

To compute the conformity score for the network nodes follow this example:

```bash
from conformity import attribute_conformity

g = nx.karate_club_graph()
node_to_conformity = attribute_conformity(g, list(np.arange(1, 4, 0.2)), ['club'], profile_size=1)

```