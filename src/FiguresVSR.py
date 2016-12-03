import json, pickle
from sklearn.feature_extraction.text import TfidfVectorizer

class FiguresVSR:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        # load figures information
        with open('../Dataset/Figures/figures_captions.json', 'r') as f:
            self.figures_captions = json.load(f)
        f.close()
        
        
        # load vectorizer
        with open('../Dataset/Figures/figures_vectorizer.pkl', 'r') as f:
            self.figures_vectorizer = pickle.load(f)
        f.close()
        
        # load terms
        with open('../Dataset/Figures/figures_terms.json', 'r') as f:
            self.figures_terms = json.load(f)
        f.close()
        
        # load tf-idf matrix
        with open('../Dataset/Figures/figures_tfidf.pkl', 'r' ) as f:
            self.figures_tfidf = pickle.load(f)
        f.close()
        
    def query_process(self, query = 'information retrieval'):
        return self.figures_vectorizer.transform([query])