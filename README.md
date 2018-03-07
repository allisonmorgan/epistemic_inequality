# Epistemic Inequality

Replication data and code for "Prestige drives epistemic inequality in the diffusion of scientific ideas"

##### `cache`

Contains [pickles](https://docs.python.org/2/library/pickle.html) of epidemic size and length. The script `summary.py` will return how many simulations were run for each transmission probability, and each particular starting node. Each cache of the SI model contains 1000 trials for each node, transmission probability pair. Each cache of the SI model allowing for random jumps contains 500 trials for each node, transmission probability pair. 

The files `updatebusinessresults.py`, `updatecompsciresults.py`, and `updatehistoryresults.py` will add more runs of each epidemic simulation to the files in `cache`.

##### `data`

Contains the edge and vertex lists of the [faculty hiring networks](http://tuvalu.santafe.edu/~aaronc/facultyhiring/). Data was released under the [CC BY-NC 2.0](https://creativecommons.org/licenses/by-nc/2.0/) license.

##### `epidemic`

The script `epidemic.py` describes the SI simulation we've implemented.

##### `imports`

The files `importbusiness.py`, `importcompsci.py`, and `importhistory.py` generate [networkx](https://networkx.github.io) networks and parse prestige metadata from the edge and vertex lists from `data`.

##### `publications`

The files called `deep_learning_titles.txt`, `incremental_titles.txt`, and `topic_modeling_titles.txt` contain the titles extracted under our choice of keywords for each topic. These titles have been selected from the computer science bibliography, [dblp](http://dblp.uni-trier.de). This data is available under the [Open Data Commons ODC-BY 1.0](http://dblp.uni-trier.de/faq/Under+what+license+is+the+data+from+dblp+released.html) license. The pickle files `deep_learning.p`, `incremental.p`, and `topic_modeling.p` contain the fraction of transmissions due to hiring under 10,000 permutation tests. The notebook `spread_of_research_ideas.ipynb` documents our permutation test.

##### `results`

Contains all of the plots from the paper. Code to generate these plots can be found in `getplots.py`. The file `plot_utils.py` has been reproduced from [`samplotlib`](https://github.com/samfway/samplotlib) under the [`BSD 2-Clause "Simplified"`](https://github.com/samfway/samplotlib/blob/master/LICENSE) license.





