# Epistemic Inequality

Replication data and code for "Prestige drives epistemic inequality in the diffusion of scientific ideas"

##### `cache`

Contains [pickles](https://docs.python.org/2/library/pickle.html) of epidemic size and length. The script `summary.py` will return how many simulations were run for each transmission probability, and each particular starting node. The files `updatebusinessresults.py`, `updatecompsciresults.py`, and `updatehistoryresults.py`, will add more runs of each epidemic simulation to the files in `cache`.

##### `data`

Contains the edge and vertex lists of the [faculty hiring networks](http://tuvalu.santafe.edu/~aaronc/facultyhiring/). Data was released under the [CC BY-NC 2.0](https://creativecommons.org/licenses/by-nc/2.0/) license.

##### `epidemic`

The script `epidemic.py` describes the simulation we've implemented.

##### `imports`

The files `importbusiness.py`, `importcompsci.py`, and `importhistory.py` generate [networkx](https://networkx.github.io) networks and parse prestige metadata from the edge and vertex lists from `data`.

##### `results`

Contains all of the plots from the paper. Code to generate these plots can be found in `getplots.py`. The file `plot_utils.py` has been reproduced from [`samplotlib`](https://github.com/samfway/samplotlib) under the [`BSD 2-Clause "Simplified"`](https://github.com/samfway/samplotlib/blob/master/LICENSE) license.





