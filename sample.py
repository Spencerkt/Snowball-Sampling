import sys
import networkx as nx
import pandas as pd
import numpy as np
from snowballsampling import randomseed 
from snowballsampling import snowballsampling 
from snowballsampling import surroundings 


def show_graph_stats(df):
    print '\ndataset stats:'
    print 'num movies = {}'.format(df.movie_id.unique().shape[0])
    print 'num users = {}'.format(df.user_id.unique().shape[0])
    print 'num ratings = {}'.format(df.shape[0])
    avg = df[['user_id', 'movie_id']].groupby('user_id').count().mean().values[0]
    print 'avg num ratings per user = {}\n'.format(avg)
    return 


def build_graph(path):
    graph_df = pd.read_csv(path, sep='\t', header=None)
    graph_df.columns = ['user_id', 'movie_id', 'rating', 'timestamp']
    show_graph_stats(graph_df)

    G = nx.Graph()

    users = ['user_{}'.format(i) for i in graph_df.user_id.tolist()]
    movies = ['movie_{}'.format(i) for i in graph_df.movie_id.tolist()]
    links = [(r.user_id, r.movie_id) for _, r in graph_df.iterrows()]

    G.add_nodes_from(users)
    G.add_nodes_from(movies)
    G.add_edges_from(links)

    print 'graph has {} nodes.'.format(G.number_of_nodes())
    print 'graph has {} edges.'.format(G.number_of_edges())

    return G


if __name__ == "__main__":

    dataset_path = sys.argv[1]
    print 'reading graph from ' + dataset_path

    graph = build_graph(dataset_path)

    num_users = 10
    samples = []    

    print '\nsampling for {} users'.format(num_users)

    for i in range(num_users):
        rand_node = randomseed(graph)
        subgraph = snowballsampling(graph, rand_node, maxsize=50)
        samples.append(subgraph)
        print '\tdone with {}th sample'.format(i + 1)

    sampled_nodes = np.unique([s.nodes() for s in samples])
    print '\nsample results:'
    print sampled_nodes.shape
    print sampled_nodes





    












