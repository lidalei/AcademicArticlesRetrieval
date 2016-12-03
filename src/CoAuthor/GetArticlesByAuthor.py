import json
from nltk.metrics import edit_distance

# read the Graph
class GetArticlesByAuthor:
    
    def __init__(self):
        with open('CoAuthor/authors_graph.json', 'r') as f:
            self.authors_graph  = json.load(f)
        f.close()
        with open('CoAuthor/articles_authors.json', 'r') as f:
            self.articles_authors = json.load(f)
        f.close()
        
    def get_articles_by_author(self, author_name):
        
        author_name = author_name.lower()
        
        name_distances = [(author, edit_distance(author.lower(), author_name)) for author in self.authors_graph]
        min_distance = name_distances[0][1]
        nearest_author = name_distances[0][0]
        for name_distance in name_distances:
            if name_distance[1] < min_distance:
                min_distance = name_distance[1]
                nearest_author = name_distance[0]
        
        articles = []
                
        for article_ID in self.articles_authors:
            if nearest_author in self.articles_authors[article_ID]:
                articles.append(article_ID)
                
        sorted_articles = sorted(articles, reverse = True)
        
        return {'nearest_author': nearest_author, 'articles': sorted_articles}