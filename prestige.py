from collections import defaultdict, OrderedDict
from scipy.stats import pearsonr
from importcompsci import school_metadata as meta_cs, faculty_graph as g_cs, faculty_graph_weighted as gw_cs

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import networkx as nx
import numpy as np
import pandas as pd
import pickle
import statsmodels.api as sm

DIR_CS_SI = "cache/CS_SI.p"

def graph_of_dir(directory):
    if "CS" in directory:
        if "weighted" in directory:
            return gw_cs
        return g_cs

def meta_of_dir(directory):
    if "CS" in directory:
        return meta_cs

# Remove the node denoting "other"
def bad_node_of_dir(cache_dir):
    if "CS" in cache_dir:
        return 206

# How do other network measures correlate with epidemic size?
def pearson_correlation(cache_dirs, value=0.1):
    (title, cache_dir) = cache_dirs
    print("title: {0}".format(title))
    
    # Load up all the data
    cache = pickle.load(open(cache_dir, 'rb'))
    meta = meta_of_dir(cache_dir)
    graph = graph_of_dir(cache_dir)
    weighted_graph = nx.DiGraph()
    for u, v, data in graph.edges(data=True):
        if weighted_graph.has_edge(v, u): weighted_graph[v][u]['weight'] += 1.0
        else: weighted_graph.add_edge(v, u, weight = 1.0)
    
    # Average across all infection probabilities and prestige values
    results_size = defaultdict(list)
    for p in cache["size"].keys():
        for node, sizes in cache["size"][p].items():
            if node is bad_node_of_dir(cache_dir):
                continue

            avg = np.average(sizes)
            if not np.isnan(avg) and not np.isinf(avg):
                result = (meta[node]["pi"], avg)
                results_size[p].append(result)

        results_size[p] = sorted(results_size[p], key=lambda x: x[0])

    # Other (non-prestige) parameters
    ind = OrderedDict(sorted(nx.in_degree_centrality(graph).items()))
    outd = OrderedDict(sorted(nx.out_degree_centrality(graph).items()))
    d = OrderedDict(sorted(nx.degree_centrality(graph).items()))
    close = OrderedDict(sorted(nx.closeness_centrality(graph).items()))
    eigen = OrderedDict(sorted(nx.eigenvector_centrality(weighted_graph, weight='weight').items()))
    parameters = {
        "in_degree": [v for i, v in ind.iteritems()], 
        "out_degree": [v for i, v in outd.iteritems()],
        "degree": [v for i, v in d.iteritems()],
        "closeness": [v for i, v in close.iteritems()],
        "eigenvector": [v for i, v in eigen.iteritems()]}

    filtered = sorted(cache["size"].keys())
    length_of_results = len(filtered)
    
    # Generate table of correlations
    tab = {}
    for p, data in sorted(results_size.items(), key=lambda x: x[0]):
        # Gondition on a particular infection probability
        if p == value:
            x, y = zip(*data)
            coef, p = pearsonr(x, y)
            tab["prestige"] = {"coefficient": coef, "p-value": p}
            # Consider the other network measures
            for key, parameter in parameters.items():
                coef, p = pearsonr(parameter, y)
                tab[key] = {"coefficient": coef, "p-value": p}
            
            break
    
    return pd.DataFrame(data=tab)


if __name__ == "__main__":
    print pearson_correlation(("Computer Science", DIR_CS_SI))
