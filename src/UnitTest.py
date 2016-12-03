'''import json, pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# load terms
with open('../Dataset/Collection/Stopwords/collection_terms.json', 'r') as f:
    collection_terms = json.load(f)
f.close()
 
# load tf-idf matrix
with open('../Dataset/Collection/Stopwords/collection_tfidf.pkl', 'r' ) as f:
    collection_tfidf = pickle.load(f)
f.close()
 
print 'Stopwords'
 
print len(collection_terms), collection_tfidf.getnnz()
 
# load terms
with open('../Dataset/Collection/NonNon/collection_terms.json', 'r') as f:
    collection_terms = json.load(f)
f.close()

# load tf-idf matrix
with open('../Dataset/Collection/NonNon/collection_tfidf.pkl', 'r' ) as f:
    collection_tfidf = pickle.load(f)
f.close()
 
print 'NonNon'
 
print len(collection_terms), collection_tfidf.getnnz()

# load terms
with open('../Dataset/Collection/Stemming/collection_terms.json', 'r') as f:
    collection_terms = json.load(f)
f.close()
 
# load tf-idf matrix
with open('../Dataset/Collection/Stemming/collection_tfidf.pkl', 'r' ) as f:
    collection_tfidf = pickle.load(f)
f.close()
 
print 'Stemming'

print len(collection_terms), collection_tfidf.getnnz()


# load terms
with open('../Dataset/Collection/collection_terms.json', 'r') as f:
    collection_terms = json.load(f)
f.close()
 
# load tf-idf matrix
with open('../Dataset/Collection/collection_tfidf.pkl', 'r' ) as f:
    collection_tfidf = pickle.load(f)
f.close()
 
print 'StemmingStopwords'

print len(collection_terms), collection_tfidf.getnnz()
'''
'''
import json, string

def remove_equations(text):
    result_text = ''
    
    non_equation_start_index = 0
    while True:
        equation_start_index = string.find(text, '\\$', non_equation_start_index)
        if equation_start_index != -1:
            # extract the non-equation content
            result_text += text[non_equation_start_index: equation_start_index]
            # deal with next equation mark
            equation_end_index = string.find(text, '\\$', equation_start_index + 2)
            if equation_end_index != -1:
                non_equation_start_index = equation_end_index + 3
                if non_equation_start_index == len(text):
                    break
            else:
                break
        else:
            result_text += text[non_equation_start_index:]
            break
    
    text = result_text
    
    result_text = ''
    
    non_equation_start_index = 0
    while True:
        equation_start_index = string.find(text, '$$', non_equation_start_index)
        if equation_start_index != -1:
            # extract the non-equation content
            result_text += text[non_equation_start_index: equation_start_index]
            # deal with next equation mark
            equation_end_index = string.find(text, '$$', equation_start_index + 2)
            
            
            if equation_end_index != -1:
                
                equation = text[equation_start_index + 2: equation_end_index]
                        
                text = string.replace(text, equation, '')
                non_equation_start_index = non_equation_start_index + 4
                if non_equation_start_index == len(text):
                    break
            else:
                break
        else:
            result_text += text[non_equation_start_index:]
            break
        
    
    return result_text



with open('../Dataset/CVPR_sample.json') as f:    
    all_articles = json.load(f)
f.close()


for year in all_articles:
    one_year_articles = all_articles[year]
    for article_ID in one_year_articles:
        article = one_year_articles[article_ID]
        if article['FullText'] is not None:
            for section in article['FullText']:
                section_content = article['FullText'][section]
                section_content = remove_equations(section_content)
                all_articles[year][article_ID]['FullText'][section] = section_content
            
            
            
with open('CVPR_sample_new.json', 'w') as f:
    
    json.dump(all_articles, f)

f.close()
'''