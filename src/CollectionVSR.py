import json, pickle
from sklearn.feature_extraction.text import TfidfVectorizer

class CollectionVSR:
    '''
    classdocs
    '''
    
    def __init__(self, pre_process_type = 'StemmingStopwords'):
        '''
        Constructor
        pre_process_type:
        
        'StemmingStopwords': stemming and removing stop words
        
        'Stemming': stemming only
        
        'Stopwords': removing stop words only
        
        'NonNon': neither stemming nor removing stop words
        
        '''
        
        if pre_process_type not in ['StemmingStopwords', 'Stemming', 'Stopwords', 'NonNon']:
            raise ValueError('No corresponding type')
        
        if pre_process_type == 'StemmingStopwords':
            pre_process_type = ''
        else:
            pre_process_type = '/'
        
        collection_url = '../Dataset/Collection/' + pre_process_type + 'collection.json'
        collection_vectorizer_url = '../Dataset/Collection/' + pre_process_type + 'collection_vectorizer.pkl'
        collection_tfidf_url = '../Dataset/Collection/' + pre_process_type + 'collection_tfidf.pkl'
        
        # load figures information
        with open(collection_url, 'r') as f:
            self.collection = json.load(f)
        f.close()
        
        
        # load vectorizer
        with open(collection_vectorizer_url, 'r') as f:
            self.collection_vectorizer = pickle.load(f)
            self.collection_terms = self.collection_vectorizer.get_feature_names()
        f.close()
        
        
        # load tf-idf matrix
        with open(collection_tfidf_url, 'r' ) as f:
            self.collection_tfidf = pickle.load(f)
        f.close()
        
    def query_process(self, query = 'information retrieval'):
        return self.collection_vectorizer.transform([query])