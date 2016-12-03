'''
Created on Oct 18, 2015

@author: s151898
'''
from TF_IDF import TF_IDF
from nltk.stem  import SnowballStemmer
import nltk, json
from Rank import rank_list

class ProbabilisticSearch:
    
    def __init__(self):
        
        term_doc_url = "../Dataset/LBS/term_doc.json"
        info_table_url = "../Dataset/LBS/info_table.json"
        
        with open(term_doc_url,'r') as f:
            self.term_doc = json.load(f)
        f.close()
        
        with open(info_table_url,'r') as f:
            self.info_table = json.load(f)
        f.close()
        
    def probabilisticSearch(self, query):
        x = 0.5
        ti=TF_IDF()
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        
        terms_before=nltk.word_tokenize(query)
        terms= []
        for term_befor in terms_before:
            terms.append(stemmer.stem(term_befor))
    #     print  terms
        
        to_rank_prob = []
        
        collection=set()
        for term in terms:
            if term in self.term_doc:
                for number in self.term_doc[term]:
                    collection.add(number)
    
        for document in collection:
            p_Qd = 1    
            for term in terms:
                p_td = 0
                p_tMd = 0
                p_tMc = 0
                term_sum = 0
                tf=0
                tf = ti.getTF(document,term)
                dl=self.info_table["doc"][document]["term_indoc_all"]
                p_tMd=(float(tf)/float(dl))
    
                if term in self.info_table["term"]:
                    term_sum =self.info_table["term"][term]
                    term_sum_all = self.info_table["term_sum_all"]
                    p_tMc = (float(term_sum)/float(term_sum_all))
                    p_td = x*p_tMd + (1-x)*p_tMc
                    p_Qd = p_Qd*p_td
    #         prob_dict[document]=p_Qd
            to_rank_prob.append({'document': document, 'probability': p_Qd})
        ranked_prob = rank_list(to_rank_prob)
        return ranked_prob
