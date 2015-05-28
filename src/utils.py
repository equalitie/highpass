import re, sys, math, random, csv, types, networkx as nx
from collections import defaultdict

def parse(filename, isDirected):
    reader = csv.reader(open(filename, 'r'), delimiter=',')
    data = [row for row in reader]

    print "Reading and parsing the data into memory..."
    if isDirected:
        return parse_josh(data)
        #return parse_directed(data)
    else:
        return parse_undirected(data)

def parse_undirected(data):
    G = nx.Graph()
    nodes = set([row[0] for row in data])
    edges = [(row[0], row[2]) for row in data]

    num_nodes = len(nodes)
    rank = 1/float(num_nodes)
    G.add_nodes_from(nodes, rank=rank)
    G.add_edges_from(edges)

    return G

def parse_directed(data):
    DG = nx.DiGraph()

    for i, row in enumerate(data):

        node_a = format_key(row[0])
        node_b = format_key(row[2])
        val_a = digits(row[1])
        val_b = digits(row[3])

        DG.add_edge(node_a, node_b)
        if val_a >= val_b:
            DG.add_path([node_a, node_b])
        else:
            DG.add_path([node_b, node_a])

    return DG

def parse_josh(data):

    violation_latt = 47.991266 #47.140580
    violation_long = 37.792420 #37.564110
    distance_value_coeff = 0#100

    DG = nx.DiGraph()
    content = {}
    init_ranks = {}

    for i, row in enumerate(data[1:]): #skipping header
        node_a = format_key(row[0])
        node_b = format_key(row[1])
        val_a = digits(row[5])
        val_b = 0 #digits(row[3])

        from math import sqrt, cos
        import pdb

        distance_score = 1;
        try:
            int_latt = float(row[9])
            int_long = float(row[10])

            #pdb.set_trace()
            cos2_theta = cos((int_latt + violation_latt)/2)**2
            distance_score =1/(sqrt(int_latt - violation_latt)**2 + cos2_theta*(int_long- violation_long)**2)
            distance_score *= distance_value_coeff
            distance_score += 1

            val_a *= distance_score

        except ValueError:
            pass

        DG.add_edge(node_a, node_b)
        #if val_a >= val_b:
        DG.add_path([node_a, node_b])
        # else:
        #     DG.add_path([node_b, node_a])

        unicoded_content = unicode(row[15], 'utf-8').encode('utf8')
        if node_b in content:
            content[node_b].append(unicoded_content)
            init_ranks[node_b] += val_a
        else:
            content[node_b] = [unicoded_content]
            init_ranks[node_b] = val_a

    return (DG, init_ranks, content)

def digits(val):
    return int(re.sub("\D", "", val))

def format_key(key):
    key = key.strip()
    if key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
    return key


def print_results(f, method, results):
    print method
