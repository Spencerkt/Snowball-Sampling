import sys
import networkx as nx
import pandas as pd
import numpy as np
import file_writer as fw
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
    links = [('user_{}'.format(r.user_id), 'movie_{}'.format(r.movie_id))
                    for _, r in graph_df.iterrows()]

    G.add_nodes_from(users)
    G.add_nodes_from(movies)
    G.add_edges_from(links)

    print 'graph has {} nodes.'.format(G.number_of_nodes())
    print 'graph has {} edges.'.format(G.number_of_edges())

    return G


if __name__ == "__main__":
    """
    For movielens dataset, we need the following files.
    """
    rating_path = './data/movielens/ratings_filtered.txt'
    movie_path = './data/movielens/movies_filtered.txt'
    users_path = './data/movielens/users_filtered.txt'
    user_sim_path = './data/movielens/users_similarity.txt'
    movie_sim_path = './data/movielens/movies_similarity.txt'

    print 'reading graph from ' + rating_path
    graph = build_graph(rating_path)

    starting_points = 1   # 5 seems to be about the right size.
    samples = []

    print '\nsampling for {} users'.format(starting_points)

    for i in range(starting_points):
        rand_node = randomseed(graph)
        subgraph = snowballsampling(graph, rand_node, maxsize=200)
        samples.append(subgraph)
        print '\tdone with {}th sample'.format(i + 1)

    sampled_nodes = list(np.unique(samples))
    print '\n\nsampled nodes => {}'.format(len(sampled_nodes))

    users = []
    movies  = []

    for n in sampled_nodes:
        if 'user_' in str(n):
            users.append(n)
        else:
            movies.append(n)

    print 'users => {}'.format(len(users))
    print 'movies => {}\n\n'.format(len(movies))

    users = [int(u.replace('user_', '')) for u in users]
    movies = [int(m.replace('movie_', '')) for m in movies]

    print 'writing data files.'
    fw.write_movies(movie_path, movies)
    fw.write_users(users_path, users)
    fw.write_ratings(rating_path, users, movies)
    fw.write_user_sim(user_sim_path, users)
    fw.write_movie_sim(movie_sim_path, movies)
    print 'done!'


















