import os, json
from bs4 import BeautifulSoup

all_dataset_dir = '../Dataset/'

article_data_types = ['FullText', 'Abstract', 'Authors', 'Citedby', 'Footnotes', 'InfoSection',
                      'Keywords', 'LeftPanelInfo', 'RecommendedArticles', 'References']

all_dataset = {}

for sub_dir in os.listdir(all_dataset_dir):
    dataset_dir = all_dataset_dir + sub_dir
    
    if os.path.isdir(dataset_dir):
        dataset_dir += '/'
        
        # get all article IDs
        article_IDs = []
         
        for file_name in os.listdir(dataset_dir):
            if file_name.endswith('.xml'):
                article_IDs.append(file_name[:7])
        
        # # manually set article IDs
        # article_IDs = ['5995308', '5995309']
        
        # read all articles full text and data
        all_article_data = {}
        
        # read full text and other data
        for article_ID in article_IDs:
            article_data = {}
            # read full text
            full_text = {}
            try:
                with open(dataset_dir + article_ID + '_full_text.xml') as f:
                    html_doc = f.read()
                    soup = BeautifulSoup(html_doc, 'html.parser')
                    ## extract article
                    article = soup.find(id = 'article')
                    ## extract section title and content
                    for sec in article.find_all('div', class_ = 'section'):
                        # kicker = sec.find(class_ = 'kicker').string
                        if 'sec' not in str(sec['id']):
                            pass
        #                 section_name = sec.find(class_ = 'kicker').string
        #                 section_content = sec.p.text
                        else:
                            if sec.h2 is not None:
                                section_name = sec.h2.text
                            elif sec.h3 is not None:
                                section_name = sec.h3.text
                            else:
                                section_name = sec.h4.text
                            section_content = ''
                            for paragraph in sec.find_all('p'):
                                section_content += paragraph.text
                        full_text[section_name] = section_content
                f.close()
                
                article_data['FullText'] = full_text
            except AttributeError, error:
                print article_ID, 'Error'
                article_data['FullText'] = None
            # read article abstract
            with open(dataset_dir + article_ID + '_' + 'Abstract' + '.json') as f:
                article_abstract = json.loads(json.load(f))
                abstract = article_abstract["response"]["abstract"]["p"][0]      
            f.close()
            
            article_data['Abstract'] = abstract
            article_data['Title'] = article_abstract['response']['doc-title']
            
            # read article authors
            with open(dataset_dir + article_ID + '_' + 'Authors' + '.json') as f:
                article_authors = json.loads(json.load(f))
                if 'author' in article_authors['response']:
                    authors = article_authors["response"]['author']
                else:
                    authors = []     
            f.close()
            
            article_data['Authors'] = authors
            
            # read article citations
            with open(dataset_dir + article_ID + '_' + 'Citedby' + '.json') as f:
                article_citedby = json.loads(json.load(f))
                citedby = article_citedby["response"]["citations"]
                if citedby == "":
                    citedby = []
            f.close()
            
            article_data['Citedby'] = citedby
            
            # read article footnotes
            with open(dataset_dir + article_ID + '_' + 'Footnotes' + '.json') as f:
                article_footnotes = json.loads(json.load(f))
                if 'footnote' in article_footnotes['response']:
                    footnotes = article_footnotes["response"]['footnote']
                else:
                    footnotes= []
            f.close()
            
            article_data['Footnotes'] = footnotes
            
            # read article info section
            with open(dataset_dir + article_ID + '_' + 'InfoSection' + '.json') as f:
                article_infosection = json.loads(json.load(f))
                infosection = article_infosection['response']['sections']
            f.close()
            
            article_data['InfoSection'] = infosection
            
            # read keywords 
            with open(dataset_dir + article_ID + '_' + 'Keywords' + '.json') as f:
                article_keywords = json.loads(json.load(f))
                keywords = article_keywords['response']['kwd-group']
            f.close()
            
            article_data['Keywords'] = keywords
            
        #     # read left panel info
        #     with open(dataset_dir + article_ID + '_' + 'LeftPanelInfo' + '.json') as f:
        #         article_left_panel_info = json.loads(json.load(f))
        #         left_panel_info = article_left_panel_info['response']['kwd-group']
        #     f.close()
        #     
        #     article_data['LeftPanelInfo'] = left_panel_info
            
            # read recommended article
            with open(dataset_dir + article_ID + '_' + 'RecommendedArticles' + '.json') as f:
                try:
                    article_recommend_articles = json.loads(json.load(f))
                    recommend_articles = article_recommend_articles
                    article_data['RecommendedArticles'] = recommend_articles
                except  ValueError, error:
                    print article_ID, 'Error'
                    article_data['RecommendedArticles'] = ''
            f.close()
                
            # read references
            with open(dataset_dir + article_ID + '_' + 'References' + '.json') as f:
                article_references = json.loads(json.load(f))
                if 'reference' in article_references['response']:
                    references = article_references['response']['reference']
                else:
                    references = []
            f.close()
            
            article_data['References'] = references
            
            print article_ID
            ## add all article data
            all_article_data[article_ID] = article_data
            all_dataset[sub_dir] = all_article_data
# write to file
with open('CVPR.json', 'w') as f:
    json.dump(all_dataset, f)
f.close()