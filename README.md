# Epistemic Inequality

Replication data and code for "Prestige drives epistemic inequality in the diffusion of scientific ideas".

#### `cache`

Contains [pickles](https://docs.python.org/2/library/pickle.html) of epidemic size and length. The script `summary.py` will return how many simulations were run for each transmission probability, and each particular starting node.

#### `data`

Contains the vertex and edgelists of the [faculty hiring networks](http://tuvalu.santafe.edu/~aaronc/facultyhiring/). Data was released under the [CC BY-NC 2.0](https://creativecommons.org/licenses/by-nc/2.0/) license. The files `importbusiness.py`, `importcompsci.py`, and `importhistory.py` generate [networkx](https://networkx.github.io) networks from this data.

#### `results`

Contains all of the plots from the paper. Code to generate these plots can be found in `getplots.py`.

### References

