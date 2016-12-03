'''
Created on Oct 15, 2015

@author: Dalei
'''

import json, nltk
import networkx as nx
import matplotlib.pyplot as plt

# This module is used to extract co-authors of articles

## we only need authors information
# articles_authors = {}
#   
# with open('../Dataset/metadata.json') as f:
#     metadata = json.load(f)
#     for year in metadata:
#         one_year_articles = metadata[year]
#         for article_ID in one_year_articles:
#             # convert authors string to list
#             articles_authors[article_ID] = one_year_articles[article_ID]['authors'].split(';')
# f.close()
## end get authors information only

## begin get articles_authors
# with open('../../Dataset/Local/articles_authors.json', 'r') as f:
#     articles_authors = json.load(f)
# f.close()
## end get articles_authors

## begin get single authors from file
# with open('../../Dataset/Local/single_authors.json', 'r') as f:
#     authors = json.load(f)
# f.close()    
## end get single authors from file

## begin single authors
# how to get single authors from articles_authors
# 
# authors = {}
#      
# for article_ID in articles_authors:
#     for author in articles_authors[article_ID]:
#         if author not in authors:
#             authors[author] = 1
#         else:
#             authors[author] += 1
#              
# with open('../Dataset/Local/single_authors.json', 'w') as f:
#     json.dump(authors, f)
# f.close()
## end single authors

## begin building graph
# authors_graph = {}
#   
# for author in authors:
#     authors_graph[author] = {}
#          
#     for article_ID in articles_authors:
#              
#         article_authors = articles_authors[article_ID]
#             
#         # author exists in the article
#         if author in article_authors:
#             for author_ in article_authors:
#                 if author_ != author:
#                     if author_ not in authors_graph[author]:
#                         authors_graph[author][author_] = 1
#                     else:
#                         authors_graph[author][author_] += 1

# removing less relation
# notably_authors_graph = {}
# 
# for author in authors_graph:
#     notably_authors_graph[author] = {}
#     for adjacent_author in authors_graph[author]:
#         if authors_graph[author][adjacent_author] >= 2:
#             notably_authors_graph[author][adjacent_author] = authors_graph[author][adjacent_author]
#             
# for author in authors_graph:
#     if len(notably_authors_graph[author]) < 1:
#         del notably_authors_graph[author]
#             
#          
# with open('authors_graph.json', 'w') as f:
#     json.dump(authors_graph, f)
# f.close()
## end building graph

## begin building a visual graph from the graph file
with open('../../Dataset/Local/authors_graph.json', 'r') as f:
    authors_graph = json.load(f)
f.close()
      
coauthor_network = nx.Graph()
coauthor_network.add_nodes_from(authors_graph.keys())
weighted_edges = [(node, adjacent_node, {'weight':authors_graph[node][adjacent_node]}) for node in authors_graph for adjacent_node in authors_graph[node]]
coauthor_network.add_edges_from(weighted_edges)
nx.write_gml(coauthor_network, 'coauthor_network.graph')
 
edges = [(node, adjacent_node) for node in authors_graph for adjacent_node in authors_graph[node]]

position = nx.spring_layout(coauthor_network)

nx.draw_networkx_nodes(coauthor_network, position, node_size = 2)
nx.draw_networkx_edges(coauthor_network, position, edge_list = edges, edge_color = 'r')
# plt.show()
plt.savefig('authors_graph.png', dpi = 1200)

## end building a visual graph from the grapg file

# with open('single_authors.json', 'r') as f:
#     authors = json.load(f)
# f.close()
# 
# authors_support = []
# 
# for author_index, author in zip(range(len(authors)), authors):
#     authors_support.append([author, 0])
#     for article_ID in articles_authors:
#         for author_ in articles_authors[article_ID]:
#             if author == author_:
#                 authors_support[author_index][1] += 1
#                 break
# 
# authors_support = sorted(authors_support, reverse = True, key=lambda author: author[1])
# 
# with open('authors_support.json', 'w') as f:
#     json.dump(authors_support, f)
# f.close()
# associative rule mining



if __name__ == '__main__':
    pass