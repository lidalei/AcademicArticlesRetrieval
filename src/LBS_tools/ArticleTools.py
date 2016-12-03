'''
Created on Oct 26, 2015

@author: s151898
'''

import Collection,json


class ArticleTools(object):
    def __init__(self):
        with open("../../Dataset/metadata.json",'r') as d:
            self.dict = json.load(d)
        d.close()
        
        with open("../../Dataset/LBS/doc_labels.json",'r') as d:
            self.doc_labels = json.load(d)
        d.close()
        

    def getLabels(self,number):
        
        return self.doc_labels[number]                      #return a string list of labels
    
    def getTitle(self,number):
        for year in self.dict:
            if number in self.dict[year]:
                return self.dict[year][number]["title"] #return a string
    
    def getAbstract(self,number):
        for year in self.dict:
            if number in self.dict[year]:
                return self.dict[year][number]["abstract"] #return a string 

    def getArticlesByLabel(self,label):
        numbers = []
        for number in self.doc_labels:
            for in_label in self.doc_labels[number]:
                if in_label == label:
                    numbers.append(number)
        return  numbers[0:10]                                      #return a string list of numbers, which belong to this label
                
# print ArticleTools().getAbstract("5995313")
# print ArticleTools().getTitle("5995313")
# print ArticleTools().getLabels("6909404")
# print ArticleTools().getArticlesByLabel("computational geometry")