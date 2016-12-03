import json, nltk, string, time, pickle

from src import Utils_Dalei

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans

configuration = {'stop words' :True,
                 'stop words set': 'english',
                 'stemming' :True,
                 'stemming type': 'Lancaster', # Porter
                 'minibatch': True,
                 'verbose': False
                 }

## begin getting tfidf

# stop words
stop_words_set = None
if configuration['stop words'] is True:
    stop_words_set = set(nltk.corpus.stopwords.words(configuration['stop words set']))

# vectorizer
vectorizer = TfidfVectorizer(tokenizer = Utils_Dalei.tokenizer, stop_words = stop_words_set, norm = 'l2')


# extract all figure captions and pre-process them

all_figure_captions = []

with open('../Dataset/Figures/figures.json') as figures_f:
    # get all figures
    figures = json.load(figures_f)
    # get all articles of each year
    for year in figures:
        one_year_figures = figures[year]
        # deal with figures each article respectively
        for article_ID in one_year_figures:
            article =  one_year_figures[article_ID]
            article_title = article['Title']
            article_figures = article['fig']
            for figure_index, figure in zip(range(len(article_figures)), article_figures):
                figure_caption = figure['caption']
                
                # remove equations
                figure_caption = Utils_Dalei.remove_equations(figure_caption)
                
                # transfer to lower case
                figure_caption = string.lower(figure_caption)

                # remove punctuation
                figure_caption = Utils_Dalei.remove_punctuation(figure_caption)
                
                all_figure_captions.append({'article_ID': article_ID, 'figure_index': figure_index, 'figure_caption' :figure_caption})
                  
figures_f.close()

# save collection of figures and captions
with open('../Dataset/Figures/figures_captions.json', 'w') as f:
    json.dump(all_figure_captions, f)
f.close()

#     term1 term2 term3 ...
# doc1  0.2  0.8   0.2
# doc2  0.5  0.5   0.5
tfidf = vectorizer.fit_transform([figure['figure_caption'] for figure in all_figure_captions])

# save vectorizer
with open('../Dataset/Figures/figures_vectorizer.pkl', 'w') as f:
    pickle.dump(vectorizer, f)
f.close()

# save terms
with open('../Dataset/Figures/figures_terms.json', 'w') as f:
    json.dump(vectorizer.get_feature_names(), f)    
f.close()    

# save tf-idf matrix
with open("../Dataset/Figures/figures_tfidf.pkl", 'w') as f:
    pickle.dump(tfidf, f)
f.close()
# 
## end getting tfidf

## do clustering - k-means
# true_k = 300
# 
# if configuration['minibatch']:
#     km = MiniBatchKMeans(n_clusters = true_k, init = 'k-means++', n_init = 1, init_size = 1000, batch_size = 1000, verbose = configuration['verbose'])
# else:
#     km = KMeans(n_clusters = true_k, init = 'k-means++', max_iter = 100, n_init = 1, verbose = configuration['verbose'])
# 
# print 'Clustering sparse data with {}'.format(km)
# 
# t0 = time.time()
# 
# km.fit(tfidf)
# 
# print 'done in {}s'.format((time.time() - t0))