# Conformity
[![PyPI download month](https://img.shields.io/pypi/dm/node-conformity.svg?color=blue&style=plastic)](https://pypi.python.org/pypi/node-conformity/)

``Conformity`` implements the path-aware homophily measure as introduced in:


> G. Rossetti, S. Citraro and L. Milli.
>
> **Conformity: a Path-Aware Homophily measure for Node-Attributed Networks**
> https://arxiv.org/abs/2012.05195

## Installation

``Conformity`` *requires* python>=3.6.

To install the latest version of our library just download (or clone) the current project, open a terminal and run the following commands:

```bash
pip install -r requirements.txt
pip install .
```

Alternatively use pip:
```bash
pip install node_conformity
```

## Usage

To compute the conformity score for the network nodes follow this example:

```bash
from conformity import attribute_conformity

g = nx.karate_club_graph()
node_to_conformity = attribute_conformity(g, list(np.arange(1, 4, 0.2)), ['club'], profile_size=1)

```
