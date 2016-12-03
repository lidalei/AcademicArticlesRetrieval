'''
Created on Oct 16, 2015

@author: s151898
'''
import json,math
import Collection

class TF_IDF(object):
    
    def __init__(self):
        self.doc_term_url = Collection.doc_term_url
        self.term_doc_url = Collection.term_doc_url
        self. idf_url = Collection.idf_url
        self.info_table_url = Collection.info_table_url
        
        with open(self.term_doc_url,'r') as f:
            self.term_doc = json.load(f)
        f.close()
         
        with open(self.idf_url,'r') as f:
            self.idf = json.load(f)
        f.close()
         
        with open(self.info_table_url,'r') as f:
            self.info_table = json.load(f)
        f.close()
        
    def getTF(self,document,term):
        tf=0.0
        if term in self.term_doc:  
            if document in self.term_doc[term]:
                tf =self.term_doc[term][document]
        return tf
        
    def getIDF(self,term):
        df=0.0
        if term in self.idf:
                df=self.idf[term] 
        if df == 0.0:
            pass
#             print "term","\"",term,"\"","isn't in this collection"
        else:
            N=float(self.info_table["doc_sum"])
            idf=math.log10(N/df)
            return idf
        
    def getTF_IDF(self,document,term):
        t=TF_IDF()
        tf=t.getTF(document, term)
        idf=t.getIDF(term)
        if tf != 0 and idf!=0:
            x =float(tf*idf)
            return x
        else:
            return 0
 
# s=TF_IDF()
# s.getTF("6247988","allanalyz")