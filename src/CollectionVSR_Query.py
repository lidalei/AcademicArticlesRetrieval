import string, json, time

import CollectionVSR

import Utils_Dalei

# select pre-procesing methods
query_handler = CollectionVSR.CollectionVSR('StemmingStopwords')

def get_relevant_articles(metadata, query):
    
    if query == 'EOF':
        print 'Thanks'
    
    t0 = time.time()
    
    query_result = query_handler.query_process(Utils_Dalei.remove_punctuation(string.lower(query)))
           
    query_term_indices = [term_index for term_index in query_result.nonzero()[1]]
    
#     for term_index in query_term_indices:
#         print query_handler.collection_terms[term_index]
    
    query_tfidf = [query_result[0, term_index] for term_index in query_term_indices]
    
    relevant_articles = []
    
    for article_index, article in zip(range(len(query_handler.collection)), query_handler.collection):
        
        collection_tfidf = [query_handler.collection_tfidf[article_index, term_index] for term_index in query_term_indices]
        
        similarity = Utils_Dalei.cosine_similarity(query_tfidf, collection_tfidf)
        
        if similarity is not False and similarity != 0:
            for year in metadata:
                if article['article_ID'] in metadata[year]:
                    article_title = metadata[year][article['article_ID']]['title']
            
            relevant_articles.append({'article_ID': article['article_ID'], 'article_title': article_title, 'similarity': similarity})
    
    ranked_relevant_articles = sorted(relevant_articles, key = lambda relevant_article: relevant_article['similarity'], reverse = True)
    
    t1 = time.time()
    
    response = {}
    
    response['time'] = t1 - t0
    response['length'] = len(ranked_relevant_articles)
    if len(ranked_relevant_articles) > 20:
        response['articles'] = ranked_relevant_articles[:20]
    else:
        response['articles'] = ranked_relevant_articles
    return response

# print get_relevant_articles('image classification')