from collections import defaultdict
from sklearn.linear_model import LinearRegression
from matplotlib.lines import Line2D
from scipy.optimize import curve_fit
from scipy.stats import linregress
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

from imports.importcompsci import school_metadata as meta_cs, faculty_graph as g_cs, faculty_graph_weighted as gw_cs
from imports.importhistory import school_metadata as meta_his, faculty_graph as g_his, faculty_graph_weighted as gw_his
from imports.importbusiness import school_metadata as meta_busi, faculty_graph as g_busi, faculty_graph_weighted as gw_busi

import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import matplotlib
import networkx as nx
import numpy as np
import pickle
import statsmodels.api as sm
import plot_utils

DIR_CS_SI = "cache/CS_SI.p"
DIR_HIS_SI = "cache/HIS_SI.p"
DIR_BUSI_SI = "cache/BUSI_SI.p"

DIR_CS_SI_JUMP_PROBABILITY = "cache/random_jump/CS_SI.p"
DIR_HIS_SI_JUMP_PROBABILITY = "cache/random_jump/HIS_SI.p"
DIR_BUSI_SI_JUMP_PROBABILITY = "cache/random_jump/BUSI_SI.p"

dirs = [DIR_CS_SI, DIR_HIS_SI, DIR_BUSI_SI]

all_departments_SI = [("Business", DIR_BUSI_SI), ("Computer Science", DIR_CS_SI), ("History", DIR_HIS_SI)]
all_departments_SI_random_jump = [("Business", DIR_BUSI_SI_JUMP_PROBABILITY), ("Computer Science", DIR_CS_SI_JUMP_PROBABILITY), ("History", DIR_HIS_SI_JUMP_PROBABILITY)]

def curve(x, h, a, k):
    return h / (1 + np.exp(a * (x - k)))

def avg_geodesic_path_length_from(from_node, graph):
    assert(from_node in graph.nodes())
    geodesic_path_lengths = [nx.shortest_path_length(graph, source=from_node, target=target)
                             for target in graph.nodes()
                             if target is not from_node
                             and nx.has_path(graph, from_node, target)]
    if len(geodesic_path_lengths) == 0.0: return 0.0
    return np.nanmean(geodesic_path_lengths)

def graph_of_dir(directory):
    if "CS" in directory:
        if "weighted" in directory:
            return gw_cs
        return g_cs
    if "HIS" in directory:
        if "weighted" in directory:
            return gw_his
        return g_his
    if "BUSI" in directory:
        if "weighted" in directory:
            return gw_busi
        return g_busi


def meta_of_dir(directory):
    if "CS" in directory:
        return meta_cs
    if "HIS" in directory:
        return meta_his
    if "BUSI" in directory:
        return meta_busi


def normalize(graph, node, length):
    avg_geodesic_path_length = avg_geodesic_path_length_from(node, graph)
    if avg_geodesic_path_length == 0 : return np.nan
    return float(length) / avg_geodesic_path_length

def average_across_infection_probability(tuples):
    dictionary = defaultdict(list)
    for (infection_prob, size) in tuples:
        dictionary[infection_prob].append(size)

    return [(infection_prob, np.average(sizes)) for infection_prob, sizes in dictionary.items()]

# Remove the "other" nodes in these graphs
def bad_node_of_dir(cache_dir):
    if "CS" in cache_dir:
        return 206
    if "HIS" in cache_dir:
        return 145
    if "BUSI" in cache_dir:
        return 113

def plot_centrality():
    colors = iter(cm.rainbow(np.linspace(0, 1, 3)))
    markers = Line2D.filled_markers
    fig = plt.figure(figsize=(6.0, 4.))
    ax = plt.gca()

    for i, (faculty_graph, school_metadata, dept) in enumerate([(g_cs, meta_cs, "Computer Science")]):
        x = []; y = []
        max_pi = 0
        max_c = 0
        ccs = sorted(nx.strongly_connected_components(faculty_graph), key=len, reverse=True)
        cc = ccs[0]
        for vertex in cc:
            c = 0
            path_lengths = nx.single_source_shortest_path_length(faculty_graph, source=vertex).values()
            if len(path_lengths) > 0:
                c = np.nanmean(path_lengths)
            label = school_metadata[vertex]['institution']
            x.append(school_metadata[vertex]['pi'])
            y.append(c)
            if school_metadata[vertex]['pi'] > max_pi:
                max_pi = school_metadata[vertex]['pi']
            if c > max_c:
            	max_c = c

            if label in ['MIT']:
                plt.annotate(label, xy=(school_metadata[vertex]['pi'], c), xytext=(50, 50), textcoords='offset points', ha='center', va='bottom', arrowprops={'arrowstyle': '-', 'ls': 'dashed'}, fontsize = plot_utils.LEGEND_SIZE)
            if label in ['University of Colorado, Boulder']:
                if label == 'University of Colorado, Boulder':
                    label = 'University of Colorado,\nBoulder'
                plt.annotate(label, xy=(school_metadata[vertex]['pi'], c), xytext=(25, -45), textcoords='offset points', ha='center', va='bottom', arrowprops={'arrowstyle': '-', 'ls': 'dashed'}, fontsize = plot_utils.LEGEND_SIZE)
            if label in ['New Mexico State University']:
                if label == 'New Mexico State University':
                    label = 'New Mexico\nState University'
                plt.annotate(label, xy=(school_metadata[vertex]['pi'], c), xytext=(25, -100), textcoords='offset points', ha='center', va='bottom', arrowprops={'arrowstyle': '-', 'ls': 'dashed'}, fontsize = plot_utils.LEGEND_SIZE)

        ax.scatter(x, y, edgecolor='w', clip_on=False, zorder=1, color=next(colors), s=28)

        slope, intercept, r_value, p_value, std_err = linregress(x, y)
       	plt.plot([0, max(x)], [slope*i + intercept for i in [0, max(x)]], color=plot_utils.ALMOST_BLACK, label='Slope: %.4f\n$R^{2}$: %.4f' % (slope, r_value**2))

    plt.xlabel(r'Universities Sorted by Prestige, $\pi$', fontsize=plot_utils.LABEL_SIZE)
    plt.ylabel(r'Average Path Length, $\langle \ell \rangle$', fontsize=plot_utils.LABEL_SIZE)

    plot_utils.finalize(ax)
    plt.xlim(0, max_pi)
    plt.ylim(1, max_c)
    plt.legend(loc='upper left', fontsize=plot_utils.LEGEND_SIZE, frameon=False)
    plt.savefig("results/centrality.eps", bbox_inches='tight', format='eps', dpi=1000)
    plt.clf()


def plot_grouped_adjacency():
  fig, ax = plt.subplots(1, 1, figsize=(6, 4))

  for l, (g, title) in enumerate([(g_cs, "Computer Science")]):
    # Vertices are ordered by prestige in the dataset
    adj = nx.to_numpy_matrix(g, dtype=int)

    # Scale adjacency matrix by a vertex's outdegree.
    # Edges i -> j are from row_i -> col_j
    groups = np.linspace(0, 100, 11)
    grouped_by_row = []
    for i, row in enumerate(adj):
      in_edges = [] 
      for rank, edges in enumerate(row[0].tolist()[0]):
        for j in range(int(edges)):
          in_edges.append(rank)
      grouped_row, _ = np.histogram(in_edges, groups)
      grouped_by_row.append(grouped_row)

    grouped = [np.zeros(len(groups)-1) for i in range(len(groups)-1)]
    for i, row in enumerate(grouped_by_row):
      for j in range(len(groups)-1):
        if i <= groups[j+1]:
          for k, elem in enumerate(row):
            grouped[j][k] += elem
          break

    colors = iter(cm.rainbow(np.linspace(0, 1, 3)))
    r,g,b = next(colors)[:3]  # Unpack RGB vals (0. to 1., not 0 to 255).
    cdict = {'red':   ((0.0,  1.0, 1.0),
                   (1.0,  r, r)),
         'green': ((0.0,  1.0, 1.0),
                   (1.0,  g, g)),
         'blue':  ((0.0,  1.0, 1.0),
                   (1.0,  b, b))}
    custom_cmap = LinearSegmentedColormap('custom_cmap', cdict)
    cax = ax.matshow(grouped, cmap=custom_cmap)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    labels = ['%.0f' % group for group in groups]
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_yticklabels(labels, fontsize=12)

    if l == 0:
      ax.set_ylabel(r"Prestige of PhD Institution, $\pi$", fontsize=16)
      ax.set_xlabel(r"Prestige of Hiring Institution, $\pi$", fontsize=16)
    
  plot_utils.finalize(ax)

  plt.tight_layout()
  plt.savefig("results/grouped_adjacency.eps", format='eps', dpi=1000)
  plt.clf()

# Epidemic size versus prestige for various infection probabilities p
def plot_si_prestige_size(cache_dirs):
    fig, ax = plt.subplots(1, 1, figsize=(6.0, 4.0), sharey=True)

    (title, cache_dir) = cache_dirs
    cache = pickle.load(open(cache_dir, 'rb'))
    meta = meta_of_dir(cache_dir)
    graph = graph_of_dir(cache_dir)
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

    filtered = sorted(cache["size"].keys())[1::2]
    length_of_results = len(filtered)

    colors = iter(cm.rainbow(np.linspace(0, 1, length_of_results)))
    markers = Line2D.filled_markers; count = -1
    for p, data in sorted(results_size.items(), key=lambda x: x[0]):
        if p not in filtered:
            continue
        c = next(colors); count += 1; m = markers[count]
        ax.scatter(*zip(*data), color=c, label='{0:.2f}'.format(p), s=28, marker=m, edgecolor='w', clip_on=False, zorder=1)

        x = [pi for (pi, length) in data if not np.isnan(length) and not np.isinf(length)]
        if p == 0.1:

            prev = data[0][1]
            diffs = []
            for (i, row) in enumerate(data):
                if i in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
                    diffs.append(prev*100.0-row[1]*100.0)
                    prev = row[1]

        max_pi = max(x)
        if p > 0:
            # Fit a logistic curve to this
            y = [length for (pi, length) in data if not np.isnan(length) and not np.isinf(length)]

            popt, pcov = curve_fit(curve, np.array(x), np.array(y), bounds=(0., [1., 2., 200.]), maxfev=100)
            y = curve(x, *popt)

            ax.plot(x, y, color=c)

    ax.set_xlim(0, max_pi)
    ax.tick_params(labelsize=12)
    ax.set_xlabel(r'University Prestige, $\pi$', fontsize=plot_utils.LABEL_SIZE)
    ax.set_ylabel(r'Epidemic Size, $\frac{Y}{N}$', fontsize=plot_utils.LABEL_SIZE)
    plot_utils.finalize(ax)
    plt.ylim(0, 1)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=plot_utils.LEGEND_SIZE, title='Transmission\nProbability, $p$', frameon=False, scatterpoints=1)
    plt.savefig('results/size-results-of-ALL-SI.eps', bbox_inches='tight', format='eps', dpi=1000)

def plot_si_prestige_length(cache_dirs, ylim=(0,5)):
    fig, ax = plt.subplots(1, 1, figsize=(6.0, 4.0), sharey=True)

    (title, cache_dir) = cache_dirs
    cache = pickle.load(open(cache_dir, 'rb'))
    meta = meta_of_dir(cache_dir)
    graph = graph_of_dir(cache_dir)
    results_length = defaultdict(list)
    for p in cache["length"].keys():
        for node, lengths in cache["length"][p].items():
            if node is bad_node_of_dir(cache_dir):
                continue

            avg = np.average(lengths)
            y = normalize(graph, node, avg)
            if not np.isnan(avg) and not np.isinf(avg) and not np.isnan(y):
                result = (meta[node]["pi"], y)
                results_length[p].append(result)

        results_length[p] = sorted(results_length[p], key=lambda x: x[0])

    for ratio, data in results_length.copy().items():
        avg_by_prestige = defaultdict(list)
        for pi, length in data:
            avg_by_prestige[pi].append(length)

        results_length[ratio] = [(pi, np.average(lengths)) for pi, lengths in avg_by_prestige.items()]
        results_length[ratio] = sorted(results_length[ratio], key=lambda x: x[0])

    filtered = sorted(cache["length"].keys())[1::2]
    length_of_results = len(filtered)

    colors = iter(cm.rainbow(np.linspace(0, 1, length_of_results)))
    markers = Line2D.filled_markers; count = -1
    for p, data in sorted(results_length.items(), key=lambda x: x[0]):
        if p not in filtered:
            continue
        c = next(colors); count += 1; m = markers[count]
        ax.scatter(*zip(*data), color=c, label='{0:.2f}'.format(p), s=28, marker=m, edgecolor='w', clip_on=False, zorder=1)

        x = np.array([pi for (pi, length) in data if not np.isnan(length) and not np.isinf(length)])
        max_pi = max(x)
        y = np.array([length for (pi, length) in data if not np.isnan(length) and not np.isinf(length)])

        # Fit a linear curve to this
        # regr = LinearRegression()
        # regr.fit(x.reshape(-1, 1), y.reshape(-1, 1))
        # interval = np.array([min(x), max(x)])
        # ax.plot(interval, interval*regr.coef_[0] + regr.intercept_, color=c)

        # Fit a LOWESS curve to this
        lowess = sm.nonparametric.lowess
        z = lowess(y, x, return_sorted=False)
        ax.plot(x, z, color=c)

    ax.set_xlim(0, max_pi)
    ax.tick_params(labelsize=12)
    ax.set_xlabel(r'University Prestige, $\pi$', fontsize=plot_utils.LABEL_SIZE)
    ax.set_ylabel(r'Normalized Epidemic Length, $\frac{L}{\ell}$', fontsize=plot_utils.LABEL_SIZE)
    plot_utils.finalize(ax)

    plt.ylim(ylim)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=plot_utils.LEGEND_SIZE, title='Transmission\nProbability, $p$', frameon=False, scatterpoints=1)
    plt.savefig('results/length-results-of-ALL-SI.eps', bbox_inches='tight', format='eps', dpi=1000)

def plot_random_hop_size(cache_dirs, ylim=(0, 1)):
    fig, ax = plt.subplots(1, 1, figsize=(6.0, 4.0), sharey=True)

    (title, cache_dir) = cache_dirs
    cache = pickle.load(open(cache_dir, 'rb'))
    meta = meta_of_dir(cache_dir)
    graph = graph_of_dir(cache_dir)
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

    filtered = sorted(cache["size"].keys())[1::2]
    length_of_results = len(filtered)

    colors = iter(cm.rainbow(np.linspace(0, 1, length_of_results)))
    markers = Line2D.filled_markers; count = -1
    for p, data in sorted(results_size.items(), key=lambda x: x[0]):
        if p not in filtered:
            continue
        c = next(colors); count += 1; m = markers[count]
        ax.scatter(*zip(*data), color=c, label='{0:.2f}'.format(p), s=28, marker=m, edgecolor='w', clip_on=False, zorder=1)

        x = [pi for (pi, length) in data if not np.isnan(length) and not np.isinf(length)]
        max_pi = max(x)
        if p > 0:
            # Fit a logistic curve to this
            y = [length for (pi, length) in data if not np.isnan(length) and not np.isinf(length)]

            popt, pcov = curve_fit(curve, np.array(x), np.array(y), bounds=(0., [1., 2., 200.]))
            y = curve(x, *popt)

            ax.plot(x, y, color=c)

    ax.set_xlim(0, max_pi)

    ax.set_xlabel(r'University Prestige, $\pi$', fontsize=plot_utils.LABEL_SIZE)
    ax.set_ylabel(r'Epidemic Size, $\frac{Y}{N}$', fontsize=plot_utils.LABEL_SIZE)
    plot_utils.finalize(ax)
        
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=plot_utils.LEGEND_SIZE, title="Jump\nProbability, $q$", scatterpoints=1, frameon=False)
    plt.ylim(ylim)
    plt.savefig('results/size-results-of-ALL-SI-random-hops.eps', bbox_inches='tight', format='eps', dpi=1000)

# Epidemic size versus infection probability for all institutions
def plot_size_infection_probability(cache_dirs, threshold=0.00, bins=range(0, 100, 10)):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.0), sharey=True)

    (title, cache_dir) = cache_dirs
    cache = pickle.load(open(cache_dir, 'rb'))
    meta = meta_of_dir(cache_dir)
    graph = graph_of_dir(cache_dir)
    results_size = defaultdict(list)

    for p in cache["size"].keys():
        for node, sizes in cache["size"][p].items():
            if node is bad_node_of_dir(cache_dir):
                continue

            pi = meta[node]["pi"]
            avg = np.average(sizes)
            if not np.isnan(avg) and not np.isinf(avg):
                result = (p, avg)
                results_size[pi].append(result)

    # Remove data below a threshold
    for pi, data in results_size.copy().items():
        trend = [size for _, size in data]
        if max(trend) <= threshold:
            del results_size[pi]
        else:
            results_size[pi] = sorted(data, key=lambda x: x[0])

    # Bin the remaining data
    if bins != None:
        left_endpoint = bins[0]
        percentiles = np.percentile(results_size.keys(), bins[1:])
        bin_means = defaultdict(list)
        for i, bin_edge in enumerate(percentiles):
            bin_values = []
            for pi in results_size.keys():
                if left_endpoint < pi <= bin_edge:
                    bin_values.extend(results_size[pi])
                    #break
            
            bin_means[(i+1)] = average_across_infection_probability(bin_values)
            left_endpoint = bin_edge
        results_size = bin_means

    length_of_results = len(results_size.keys())

    colors = iter(cm.rainbow(np.linspace(0, 1, length_of_results)))
    for pi, data in sorted(results_size.items(), key=lambda x: x[0]):
        data = sorted(data, key=lambda x: x[0])
        c = next(colors)

        ax1.scatter(*zip(*data), color=c, label='{0}'.format(int(pi*10)), edgecolor='w', clip_on=False, zorder=1, s=28)

        # Fit a logistic curve to this
        x = [p for (p, size) in data if not np.isnan(size) and not np.isinf(size)]
        y = [size for (p, size) in data if not np.isnan(size) and not np.isinf(size)]
        popt, pcov = curve_fit(curve, np.array(x), np.array(y), bounds=([0., -150., -5.], [1., 0., 5.]))
        x_fine = np.arange(0.0, 1.01, 0.01)
        y = curve(x_fine, *popt)
        ax1.plot(x_fine, y, color=c)

        r = -2.7; k = 0.91;
        def scale_x(x, d): return (1.0*x) / (-1.0*math.log(1.0-d))
        x = []; y = [];
        for x_i, y_i in data:
            if scale_x(x_i, pi*(1.0/10.0)) > 0:
                x.append(scale_x(x_i, pi*(1.0/10.0)))
                y.append(y_i)

        if pi in [1]:
            ax2.scatter(x, y, color=c, label='{0}st Decile'.format(int(pi)), edgecolor='w', clip_on=False, zorder=1, s=28)
        elif pi in [2]:
            ax2.scatter(x, y, color=c, label='{0}nd Decile'.format(int(pi)), edgecolor='w', clip_on=False, zorder=1, s=28)
        elif pi in [3]:
            ax2.scatter(x, y, color=c, label='{0}rd Decile'.format(int(pi)), edgecolor='w', clip_on=False, zorder=1, s=28)
        elif pi in [4, 5, 6, 7, 8, 9]:
            ax2.scatter(x, y, color=c, label='{0}th Decile'.format(int(pi)), edgecolor='w', clip_on=False, zorder=1, s=28)

    # Fit a curve to the whole thing!
    def scale_y(scaled_x): return (1.0 / (1.0 + math.exp(r*(k + math.log(scaled_x)))))
    x_total = np.arange(0.01, 10.01, 0.01)
    ax2.plot(x_total, [scale_y(i) for i in x_total], color='black', label="Generic")
    
    ax1.tick_params(labelsize=12)
    ax2.tick_params(labelsize=12)
    ax1.set_ylim(0, 1.)
    ax2.set_ylim(0, 1.)
    ax2.set_xscale("log")
    ax2.set_xlim(0.04, 10)
    ax1.set_xlim(0, 1)
    
    ax1.set_xlabel(r'Transmission Probability, $p$', fontsize=plot_utils.LABEL_SIZE)
    ax2.set_xlabel(r'Effective Transmission Probability, $p^{*}$', fontsize=plot_utils.LABEL_SIZE)
    ax1.set_ylabel(r'Epidemic Size, $\frac{Y}{N}$', fontsize=plot_utils.LABEL_SIZE)
    
    plot_utils.finalize(ax1)
    plot_utils.finalize(ax2)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=plot_utils.LEGEND_SIZE, scatterpoints=1, frameon=False)
    plt.savefig('results/infectious-size-results-of-ALL-SI.eps', bbox_inches='tight', format='eps', dpi=1000)

if __name__ == "__main__":
    plot_centrality()

    plot_grouped_adjacency()

    plot_si_prestige_size(all_departments_SI[1])
    plot_si_prestige_length(all_departments_SI[1], ylim=(0,5))

    plot_random_hop_size(all_departments_SI_random_jump[1], ylim=(0,1))
    plot_size_infection_probability(all_departments_SI[1])
