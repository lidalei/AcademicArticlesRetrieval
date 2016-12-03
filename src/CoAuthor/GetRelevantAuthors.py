import json
from nltk.metrics import edit_distance

# read the Graph
class GetRelevantAuthors:
    
    def __init__(self):
        with open('CoAuthor/authors_graph.json', 'r') as f:
            self.authors_graph  = json.load(f)
        f.close()
        
    def get_relevant_authors(self, author_name):
        
        author_name = author_name.lower()
        
        name_distances = [(author, edit_distance(author.lower(), author_name)) for author in self.authors_graph]
        
        min_distance = name_distances[0][1]
        nearest_author = name_distances[0][0]
        for name_distance in name_distances:
            if name_distance[1] < min_distance:
                min_distance = name_distance[1]
                nearest_author = name_distance[0]
                
        relevant_authors = []
                
        for relevant_author in self.authors_graph[nearest_author]:
                relevant_authors.append([relevant_author, self.authors_graph[nearest_author][relevant_author]])
                ranked_relevant_authors = sorted(relevant_authors, reverse = True, key = lambda relevant_author: relevant_author[1])
        
        return ranked_relevant_authors 