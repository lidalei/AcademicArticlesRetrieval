from flask import Flask, render_template, request, Markup, jsonify

from CoAuthor.GetRelevantAuthors import GetRelevantAuthors
from CoAuthor.GetArticlesByAuthor import GetArticlesByAuthor

from LBS_tools.ProbabilisticSearch import ProbabilisticSearch

from BooleanIR.BooleanQuery import BooleanQuery

from QueryExpansion.QueryExpansion import QueryExpansion

from ReformulateQuery.Rocchio import Rocchio

import CollectionVSR_Query
import json, time

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/getArticlesByAuthor/<author_name>')
def get_articles_by_author(author_name = 'Xiaoou Tang'):

    response = get_articles_by_author_handler.get_articles_by_author(author_name)
    
    nearest_author = response['nearest_author']
    article_IDs = response['articles']
    
    articles_info = get_article_info_by_ID(article_IDs)
    
    articles_html = '<tbody><tr><th>ID</th><th>Title</th></tr>'
    for article_ID, article_info in zip(article_IDs, articles_info):
        a_tag_title = '<a target="_blank" href="' + IEEE_prefix + article_ID + '">'  + article_info['title'] + '</a>'
        articles_html += '<tr><td>' + article_ID + '</td><td>' + a_tag_title + '</td></tr>'
        articles_html += '<tr><td>Abstract</td><td>' + article_info['abstract'] + '</td></tr>'
    articles_html += '</tbody>'
    
    relevant_authors = relevant_authors_handler.get_relevant_authors(author_name)
    
    relevant_authors_html = '<ul class="list-unstyled"><li>Co-authors</li>'
    
    for relevant_author in relevant_authors:
        relevant_authors_html += '<li><a target = "_self" href="' + '/getArticlesByAuthor/' + relevant_author[0] + '">' + relevant_author[0] + '</a></li>'
    
    relevant_authors_html += '</ul>'
    
    
    return render_template('articles.html', author_name = nearest_author, articles = Markup(articles_html), relevant_authors = Markup(relevant_authors_html))



@app.route('/getRelevantAuthors/<author_name>')
def get_relevant_authors(author_name):
    return json.dumps(relevant_authors_handler.get_relevant_authors(author_name))

@app.route('/collectionVSR/<query>', methods = ['GET', 'POST'])
def collection_VSR(query):
    response = CollectionVSR_Query.get_relevant_articles(metadata, query)
    relevant_articles = response['articles']
    
    article_IDs = [relevant_article['article_ID'] for relevant_article in relevant_articles]
    articles_info = get_article_info_by_ID(article_IDs)
    
    articles_html = '<tbody id="query_' + query + '"><tr><th>ID</th><th>Title</th></tr>'
    for article, article_info in zip(relevant_articles, articles_info):
        a_tag_ID = feedback_dropdown_tag(article['article_ID'])
        a_tag_title = '<a target="_blank" href="' + IEEE_prefix + article['article_ID'] + '">'  + article['article_title'] + '</a>'
        articles_html += '<tr><td>' + a_tag_ID + '</td><td>' + a_tag_title + '</td></tr>'
        articles_html += '<tr><td>Abstract</td><td>' + article_info['abstract'] + '</td></tr>'
    articles_html += '</tbody>'
    return json.dumps({'query': query, 'time': response['time'], 'length': response['length'], 'articles': articles_html})


@app.route('/probabilisticSearch/<query>', methods = ['GET', 'POST'])
def probabilistic_search(query):
    t0 = time.time()
    response = probabilistic_search_handler.probabilisticSearch(query)
    t1 = time.time()
    article_IDs = [relevant_article['document'] for relevant_article in response]
    
    articles_info = get_article_info_by_ID(article_IDs)
    
    articles_html = '<tbody id="query_' + query + '"><tr><th>ID</th><th>Title</th></tr>'
    for article_ID, article_info in zip(article_IDs, articles_info):
        a_tag_ID = feedback_dropdown_tag(article_ID)
        a_tag_title = '<a target="_blank" href="' + IEEE_prefix + article_ID + '">'  + article_info['title'] + '</a>'
        articles_html += '<tr><td>' + a_tag_ID + '</td><td>' + a_tag_title + '</td></tr>'
        articles_html += '<tr><td>Abstract</td><td>' + article_info['abstract'] + '</td></tr>'
    articles_html += '</tbody>'
    return json.dumps({'query': query, 'time':t1 - t0, 'length': len(response), 'articles': articles_html})

@app.route('/relevanceFeedback/', methods = ['POST'])
def relevance_feedback():
    feedback = request.get_json(force=True)    
    
    feedback_dictionary = {'query': feedback['query'][6:],'relevant':feedback['relevant'],'irrelevant':feedback['non_relevant']}
    reformulated_query = ' '.join(str(term) for term in reformulate_query_handler.Rocchio(feedback_dictionary))
    
    return collection_VSR(reformulated_query)

@app.route('/booleanIR/<query>', methods = ['GET', 'POST'])
def boolean_IR(query):
    response = boolean_IR_handler.query_boolean(query)
    if response is None:
        return json.dumps({'time': 0, 'length': 0, 'articles':''})
    else:
        article_IDs =  [str(article_ID) for article_ID in response['articles']]        
        
        articles_info = get_article_info_by_ID(article_IDs)
        
        print articles_info
        
        articles_html = '<tbody><tr><th>ID</th><th>Title</th></tr>'
        for article_ID, article_info in zip(article_IDs, articles_info):
            a_tag_title = '<a target="_blank" href="' + IEEE_prefix + article_ID + '">'  + article_info['title'] + '</a>'
            articles_html += '<tr><td>' + article_ID + '</td><td>' + a_tag_title + '</td></tr>'
            articles_html += '<tr><td>Abstract</td><td>' + article_info['abstract'] + '</td></tr>'
        articles_html += '</tbody>'
        
        print articles_html
        
        return json.dumps({'time': response['time'], 'length':response['length'], 'articles': articles_html})

@app.route('/queryExpansion/<query>')
def query_expansion(query):
    t0 = time.time()
    response = query_expansion_handler.expand_query(query)
    t1 = time.time()
    if len(response) == 0:
        return json.dumps({'time': t1 - t0, 'length': 0, 'queries':[]})
    
    return json.dumps({'time': t1 - t0, 'length': len(response), 'queries':[expanded_query for expanded_query in response]})

def get_article_info_by_ID(article_IDs):
    
    articles_info = []
    
    if not isinstance(article_IDs, list):
        article_IDs = [article_IDs]
        
    for article_ID in article_IDs:
        for year in metadata:
            if article_ID in metadata[year]:
                articles_info.append({'title':metadata[year][article_ID]['title'],
                                      'abstract':metadata[year][article_ID]['abstract'],                                               
                                    })
                break

    return articles_info

def feedback_dropdown_tag(article_ID):
    tag_html = '<div class="dropdown" id="' + article_ID + '">'
    tag_html += '<button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
    tag_html += 'Feedback<span class="caret"></span></button>'
    tag_html += '<ul class="dropdown-menu">'
    tag_html += '<li><a href="#">Relevant</a></li>'
    tag_html += '<li><a href="#">Non relevant</a></li></ul></div>'
    return tag_html
    
if __name__ == '__main__':
    with open('../Dataset/metadata.json') as f:
        metadata = json.load(f)
    f.close()
    get_articles_by_author_handler = GetArticlesByAuthor()
    relevant_authors_handler = GetRelevantAuthors()
    IEEE_prefix = 'http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber='
    
    probabilistic_search_handler = ProbabilisticSearch()
    
    boolean_IR_handler = BooleanQuery()
    
    query_expansion_handler  = QueryExpansion()
    
    reformulate_query_handler = Rocchio()
    
    app.run(debug = True)