'''
Created on 28 okt. 2015

@author: s152037
'''
import json, nltk, string, time

configuration = {'stop words' :True,
                 'stop words set': 'english',
                 'stemming' :True,
                 'stemming type': 'Lancaster' # Porter
                 }

def self_stemmer(stemmer_type = 'Lancaster'):
    if stemmer_type == 'Lancaster':
        return nltk.stem.lancaster.LancasterStemmer()
    elif stemmer_type == 'Porter':
        return nltk.stem.lancaster.LancasterStemmer()
    return nltk.stem.lancaster.LancasterStemmer()

def intersect(a, b):
    return list(set(a) & set(b))

if configuration['stemming'] is True:
                    stemmer = self_stemmer(configuration['stemming type'])


class BooleanQuery:

    def __init__(self):
        '''
        Constructor
        '''
        with open('BooleanIR/inverted_index_title.json') as f:
            self.inverted_index_title = json.load(f)
        f.close()

        with open('BooleanIR/inverted_index_fulltext.json') as f:
            self.inverted_index_fulltext = json.load(f)
        f.close()

        with open('BooleanIR/inverted_index_abstract.json') as f:
            self.inverted_index_abstract = json.load(f)
        f.close()
    
    
    def query_boolean(self, query):
        t0 = time.time()
        list1=[]
        list2=[]
        qresult=[]
#       term = raw_input('Please input the term to be queried: ')
        term= query
        terms = nltk.word_tokenize(term, 'english')
        lenterms = len(terms)
        if int(lenterms)==3:
            term1= terms[0]
            term2= terms[2] 
            print term1,term2
            if (string.lower(terms[1]) =='and') or (string.lower(terms[1]) =='or'):
                if term1 != '':
                    term1=stemmer.stem(term1)
                    if term1 in self.inverted_index_fulltext: 
                        list1=self.inverted_index_fulltext[term1]
                    if term1 in self.inverted_index_title:
                        list1=list1+self.inverted_index_title[term1]
                    if term1 in self.inverted_index_abstract:
                        list1=list1+self.inverted_index_abstract[term1]
                            
                if term2 != '':
                    term2=stemmer.stem(term2)
                    if term2 in self.inverted_index_fulltext:  
                        list2=self.inverted_index_fulltext[term2] 
                    if term2 in self.inverted_index_title:
                        list2=list2+self.inverted_index_title[term2]
                    if term2 in self.inverted_index_abstract:
                        list2=list2+self.inverted_index_abstract[term2]
                if string.lower(terms[1]) =='and':
                    qresult= intersect(list1,list2)
                if string.lower(terms[1]) =='or':
                    qresult= list1+list2
            else:
                return None        
        else:                 
            return None
            
        t1 = time.time()
        
        result = {}
        result['time'] = t1 - t0
        result['length'] = len(qresult)
        
        if len(qresult) > 20:
            result['articles'] = qresult[:20]
        else:
            result['articles'] = qresult
        
        return result