import networkx as nx
import Queue as que
import copy

from numpy.random import randint
from numpy.random import choice


def randomseed(g):
    """this function recturns a single node from g, it's chosen with uniform probability"""
    user_nodes = [n for n in g.nodes() if 'user_' in str(n)]
    rand = randint(0,len(user_nodes),1)
    return user_nodes[rand[0]]

def snowballsampling(g, seed, maxsize=50):
    """this function returns a set of nodes equal to maxsize from g that are 
    collected from around seed node via snownball sampling"""
    if g.number_of_nodes() < maxsize:
        return []
    q = que.Queue()
    q.put(seed)
    subgraph = [seed]
    while not q.empty():
        for node in g.neighbors(q.get()):
            if len(subgraph) < maxsize:
                q.put(node)
                subgraph.append(node)
            else :
                return subgraph
    return subgraph

def surroundings(g, subgraph):
    """this function returns the surrounding subgraph of input subgraph argument""" 
    surdngs = copy.copy(subgraph)
    for node in subgraph:
        for i in g.neighbors(node):
            if i not in surdngs:
                surdngs.append(i)
    return surdngs
