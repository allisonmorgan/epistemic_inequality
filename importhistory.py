import networkx
import numpy as np

# Import vertex attributes
with open("data/HIS_vertexlist.txt") as f:
    lines = f.readlines()

# Create a map of node number to attributes
rows = [line.strip().split('\t') for i, line in enumerate(lines) if i > 0]
school_metadata = {}
vertex_names = {}
for row in rows:
    pi, USN2010, NRC95, region, institution = float(row[1]), row[2], row[3], row[4].strip(), row[5]
    try:
        USN2010 = float(USN2010)
    except:
        USN2010 = np.nan

    try:
        NRC95 = float(NRC95)
    except:
        NRC95 = np.nan

    vertex_names[row[5]] = int(row[0])
    attributes = {"pi": pi, "USN2010": USN2010, "NRC95": NRC95, "region": region, "institution": institution}
    school_metadata[int(row[0])] = attributes

# Import edge list
with open("data/HIS_edgelist.txt") as f:
    lines = f.readlines()

# Create list of edges
edgelist = [line.strip().split("\t") for i, line in enumerate(lines) if i > 0]
edges = []
for edge in edgelist:
    if int(edge[0]) == 145 or int(edge[1]) == 145:
        continue
    edges.append((int(edge[0]), int(edge[1])))

# Create an empty directed graph and add all edges
faculty_graph = networkx.MultiDiGraph()
faculty_graph.add_edges_from(edges)

# Multi-edge, directed, weighted graph
faculty_graph_weighted = networkx.MultiDiGraph()
for (u, v) in faculty_graph.edges():
    faculty_graph_weighted.add_edge(u, v, weight = 1.0)

for u in faculty_graph.nodes():
   for v in faculty_graph.nodes():
           faculty_graph_weighted.add_edge(u, v, weight = 0.0)
