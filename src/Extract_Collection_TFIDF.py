import json, nltk, string, pickle

from sklearn.feature_extraction.text import TfidfVectorizer

import Utils_Dalei

pre_process_configuration = Utils_Dalei.pre_process_configuration
## begin getting tfidf

# stop words
stop_words_set = None
if pre_process_configuration['stop words'] is True:
    stop_words_set = set(nltk.corpus.stopwords.words(pre_process_configuration['stop words set']))

# vectorizer
vectorizer = TfidfVectorizer(tokenizer = Utils_Dalei.tokenizer, stop_words = stop_words_set, norm = 'l2')


with open('../Dataset/CVPR.json','r') as f:
    all_articles = json.load(f)
f.close

collection = []

for year in all_articles:
    one_year_articles = all_articles[year]
    
    for article_ID in one_year_articles:
        
        content = one_year_articles[article_ID]['Abstract']
        
        full_text = one_year_articles[article_ID]['FullText']
        
        if full_text is not None:
            for section in full_text:
                content += full_text[section] + ' '
        
        content = Utils_Dalei.remove_equations(content)
        
        # transfer to lower case
        content = string.lower(content)
        
        content = Utils_Dalei.remove_equations(content)

        collection.append({'article_ID': article_ID, 'content': content})

# save collection of figures and captions
with open('../Dataset/Collection/collection.json', 'w') as cf:
    json.dump(collection, cf)
cf.close()
 
#     term1 term2 term3 ...
# doc1  0.2  0.8   0.2
# doc2  0.5  0.5   0.5
tfidf = vectorizer.fit_transform([article['content'] for article in collection])
 
# save vectorizer
with open('../Dataset/Collection/collection_vectorizer.pkl', 'w') as f:
    pickle.dump(vectorizer, f)
f.close()
 
# save terms
with open('../Dataset/Collection/collection_terms.json', 'w') as f:
    json.dump(vectorizer.get_feature_names(), f)    
f.close()    
 
# save tf-idf matrix
with open('../Dataset/Collection/collection_tfidf.pkl', 'w') as f:
    pickle.dump(tfidf, f)
f.close()
## end getting tfidf