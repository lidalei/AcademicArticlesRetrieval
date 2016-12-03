import json
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class QueryExpansion:

    def __init__(self):
        
        with open('QueryExpansion/stopwords.json','r') as f:
            self.list=json.load(f)
        f.close()
        
#         with open('CVPR.json','r') as d:
#             self.dict = json.load(d)
#         d.close()
        
        with open('QueryExpansion/Paper-keyword.json','r') as d:
            self.keywordDict = json.load(d)
        d.close()
        
        print "Please wait for data set preparation"
#         newDict=self.loadKeywords()
        dataSet=self.loadDataSet(self.keywordDict)              
        L,suppData=self.apriori(dataSet, 0.025)
        self.rules=self.generateRules(L, suppData, 0.6)

#     def loadKeywords(self):
#         newDict={}
#         for year in self.dict:
#             for number in self.dict[year]:
#                 newDict[number]=[] 
#                 for keyword_index in self.dict[year][number]["Keywords"]:
#                     list = keyword_index
#                     if(list['kwd-group-type']=='IEEE'):
#                         for keyword in list['kwd']:
#                             newDict[number].append(str(keyword))
#      
#         with open('Paper-keyword.json', 'w') as f:
#             json.dump(newDict, f)
#         f.close()
#     
#         return newDict
    
    def loadDataSet(self,newDict):
        dataSet=[]
        for number in newDict:
            dataSet.append(newDict[number])
        return dataSet 
    
    def createC1(self,dataSet):
        C1 = []
        for transaction in dataSet:
            for item in transaction:
                if not [item] in C1:
                    C1.append([item])
                    
        C1.sort()
        return map(frozenset, C1)#use frozen set so we
                                #can use it as a key in a dict    
    
    
    def scanD(self,D, Ck, minSupport):
        ssCnt = {}
        for tid in D:
            for can in Ck:
                if can.issubset(tid):
                    if not ssCnt.has_key(can): ssCnt[can]=1
                    else: ssCnt[can] += 1
        numItems = float(len(D))
        retList = []
        supportData = {}
        for key in ssCnt:
            support = ssCnt[key]/numItems
            if support >= minSupport:
                retList.insert(0,key)
            supportData[key] = support
        return retList, supportData
    
    def aprioriGen(self,Lk, k): #creates Ck
        retList = []
        lenLk = len(Lk)
        for i in range(lenLk):
            for j in range(i+1, lenLk): 
                L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
                L1.sort(); L2.sort()
                if L1==L2: #if first k-2 elements are equal
                    retList.append(Lk[i] | Lk[j]) #set union
        return retList
    
    def apriori(self,dataSet, minSupport):
        C1 = self.createC1(dataSet)
        D = map(set, dataSet)
        L1, supportData = self.scanD(D, C1, minSupport)
        L = [L1]
        k = 2
        while (len(L[k-2]) > 0):
            Ck = self.aprioriGen(L[k-2], k)
            Lk, supK = self.scanD(D, Ck, minSupport)#scan DB to get Lk
            supportData.update(supK)
            L.append(Lk)
            k += 1
        return L, supportData
    
    def generateRules(self,L, supportData, minConf):  #supportData is a dict coming from scanD
        bigRuleList = []
        for i in range(1, len(L)):#only get the sets with two or more items
            for freqSet in L[i]:#begin two items set
                H1 = [frozenset([item]) for item in freqSet]
                if (i > 1):
                    self.rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
                else:
                    self.calcConf(freqSet, H1, supportData, bigRuleList, minConf)
        return bigRuleList         
    
    def calcConf(self,freqSet, H, supportData, brl, minConf):
        prunedH = [] #create new list to return
        for conseq in H:
            conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence
            if conf >= minConf: 
    #             print freqSet-conseq,'-->',conseq,'conf:',conf
                brl.append((freqSet-conseq, conseq, conf))
                prunedH.append(conseq)
        return prunedH
    
    def rulesFromConseq(self,freqSet, H, supportData, brl, minConf):
        m = len(H[0])
        if (len(freqSet) > (m + 1)): #try further merging
            Hmp1 = self.aprioriGen(H, m+1)#create Hm+1 new candidates
            Hmp1 = self.calcConf(freqSet, Hmp1, supportData, brl, minConf)
            if (len(Hmp1) > 1):    #need at least two sets to merge
                self.rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
    
    def delExceptQuery(self,query,rules):
        leftSide_new=[]
        wnl = WordNetLemmatizer()
        leftSide=word_tokenize(str(query))
        for term_a in leftSide:
            leftSide_new.append(wnl.lemmatize(str(term_a).lower()))
        leftSide_newnew=set(leftSide_new)
        newRule=[]
        for eachrule in rules:
            rightSide=[]
            rightSide_new=[]
            for term in eachrule[0]:
                for term_b in word_tokenize(term):
                    rightSide.append(term_b)
            for term_new in rightSide:
                rightSide_new.append(wnl.lemmatize(str(term_new).lower()))
            for word in rightSide_new:
                if word in self.list: 
                    rightSide_new.remove(word)
            rightSide_newnew=set(rightSide_new)
            if  leftSide_newnew==rightSide_newnew:
                newRule.append(eachrule)
        newRule = sorted(newRule, key=lambda rule : rule[2])          
            
        querySide=[]
        querySide_new=[]
        expandQuery=[]
        for eachrule_a in newRule:
            for term_c in eachrule_a[1]:
                for term_d in word_tokenize(term_c):
                    querySide.append(term_d)
                for term_e in querySide:
                    querySide_new.append(wnl.lemmatize(str(term_e).lower()))
                    for word in querySide_new:
                        if word in self.list: 
                            querySide_new.remove(word)
            querySide_newnew=set(querySide_new)
            expandQuery.append(querySide_newnew)
            
        return expandQuery

    def expand_query(self, query):
        expandQuery = self.delExceptQuery(query, self.rules)
        expand_new = []
        for eachNewQuery in expandQuery:
            a=str(query+" ")
            for eachTerm in eachNewQuery:
                a+=eachTerm+" "
            expand_new.append(a)
        expand_new=set(expand_new)
        
        return expand_new