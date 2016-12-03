import string

import FiguresVSR

from src import Utils_Dalei

query_handler = FiguresVSR.FiguresVSR()

while True:
    
    query = raw_input('Please input a query: ')
    
    if query == 'EOF':
        print 'Thanks'
        break
    query_result = query_handler.query_process(Utils_Dalei.remove_punctuation(string.lower(query)))
    
    query_term_indices = [term_index for term_index in query_result.nonzero()[1]]
    
    query_tfidf = [query_result[0, term_index] for term_index in  query_term_indices]
    
    relevant_figures = []
    
    for figure_index, figure in zip(range(len(query_handler.figures_captions)), query_handler.figures_captions):
        
        figure_tfidf = [query_handler.figures_tfidf[figure_index, term_index] for term_index in query_term_indices]
        
        similarity = Utils_Dalei.cosine_similarity(query_tfidf, figure_tfidf)
        
        if similarity is not False and similarity != 0:
            relevant_figures.append({'article_ID': figure['article_ID'], 'figure_index': figure['figure_index'], 'similarity': similarity})
    
    ranked_relevant_figures = sorted(relevant_figures, key = lambda relevant_figure: relevant_figure['similarity'], reverse = True)
    for relevant_figure in ranked_relevant_figures:
        print relevant_figure      
        