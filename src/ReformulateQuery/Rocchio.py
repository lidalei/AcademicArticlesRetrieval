'''
Created on Oct 20, 2015

@author: student number:0984028
'''

import json
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

class Rocchio(object):
        
    def __init__(self):
        with open("ReformulateQuery/Title_term.json",'r') as d:
            self.dict = json.load(d)
        d.close()
        
#         with open("tfdf.json",'r') as f:
#             self.tfdf = json.load(f)
#         f.close()
        
        with open("ReformulateQuery/stopwords.json",'r') as f:
            self.list=json.load(f)
        f.close()
        
        self.a=2
        self.b=1
        self.r=-1
        
    def ChangeCoe(self,a,b,r):
        self.a=a
        self.b=b
        self.r=r        
     
#     def getQueryTF_IDF(self,document,query):
#         queryTerm=[]
#         queryTerm.extend(word_tokenize(str(query)))
#         documentTF_IDF=0
#         for term in queryTerm:
#             documentTF_IDF+=TF_IDF().getTF_IDF(document,term)
#         return documentTF_IDF
#     
#     def sortArticle(self,query):
#         query=str(query).lower()
#         
#         newDict={}
#         for document in self.tfdf["doc"]:
#             tf_idf = self.getQueryTF_IDF(document,query)
#             newDict[document] = tf_idf
#         
#         newDict= sorted(newDict.iteritems(), key=lambda d:d[1], reverse = True)
#         
#         dicLen=len(newDict)      
#         for i in range(0,dicLen-10):
#             newDict.pop()  
#         firstQueryList=[]
#         for i in range(0,10):
#             firstQueryList.append(str(newDict[i][0]))
#         print "The relevant articles are as follows:"
#         j=1
#         for i in firstQueryList:
#             print j,i
#             j+=1
#     
#         return firstQueryList
#     
#     def InputCheck(self,relevant):
#         relevantList=[]
#         relevantList.extend(word_tokenize(relevant))
#         for item in relevantList:
#             if not item.isdigit():
#                 return False
#             elif int(item)>10 or int(item)<1:
#                 return False        
#         return True
    
    def unionTitleTerm(self,sentimentSet):        
        titleTerm=[]
        titleTerm_new=[]
#         print sentimentSet
        for number in self.dict:
            if number in sentimentSet:
                tokenizer = RegexpTokenizer(r'\w+')
                titleTerm.extend(tokenizer.tokenize(str(self.dict[number])))
                wnl = WordNetLemmatizer()
                for term in titleTerm:
                    titleTerm_new.append(wnl.lemmatize(term.lower()))
                for word in titleTerm_new:
                    if word in self.list: 
                        titleTerm_new.remove(word)
        return titleTerm_new
                        
    def Rocchio(self,feedbackDictionary):
        likeList=feedbackDictionary["relevant"]
        unlikeList=feedbackDictionary["irrelevant"]

#         relevantList.extend(word_tokenize(relevant))
#         for i in relevantList:
#             likeList.append(firstQueryList[int(i)-1])
#         for i in relevantList:
#             unlikeList.remove(firstQueryList[int(i)-1])
            
        likeTerm=self.unionTitleTerm(likeList)
        unlikeTerm=self.unionTitleTerm(unlikeList)
#         print likeTerm
#         print unlikeTerm
        
        FinalDict={}
        likeSet = set(likeTerm)
        for item in likeSet:
            FinalDict[item] =  likeTerm.count(item)*self.b
            
        unlikeSet = set(unlikeTerm)
        for item in unlikeSet:
            FinalDict[item] =  unlikeTerm.count(item)*self.r
        
        queryTerm=[]
        queryTerm.extend(word_tokenize(str(feedbackDictionary["query"])))
        for term in queryTerm:
            if FinalDict.has_key(term):
                FinalDict[term] =  FinalDict[term]+self.a
            else:
                FinalDict[term] =  self.a
        FinalDict= sorted(FinalDict.iteritems(), key=lambda d:d[1], reverse = True)
                 
        SecondQuery = []
        for i in range(0,3):
            SecondQuery.append(FinalDict[i][0])
            
        return SecondQuery