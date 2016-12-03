from bs4 import BeautifulSoup
html_doc = open('../Dataset/CVPR 2011/5995308_full_text.xml', 'rb')
soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.prettify())

# print soup.title
# print soup.title.string

## extract article
article = soup.find(id = 'article')

## extract all sections
sections_list = []
for sec in article.find_all('div', class_ = 'section'):
    sections_list.append(sec)
print sections_list[0]
## extract section title and content
for sec in sections_list:
    kicker = sec.find(class_ = 'kicker').string
    
    title = sec.h2.text
    print title
#     title = ''
#     for sub_title in sec.h2.contents:
#         title += sub_title.string
    
#     # remove all a tags from section
#     for a in sec.find_all('a'):
#         a.decompose()
    
    content = ''
    for paragraph in sec.find_all('p'):
        content += paragraph.text
    print content
#     if sec == sections_list[len(sections_list) - 1]:
#         # extract acknowledgement
#         if sec.next_sibling:
#             acknowledgement = sec.next_sibling.string
#         print acknowledgement


## extract related articles
related_articles = soup.find(id = 'related-articles')



## extract article information
article_information = soup.find(id = 'left-panel')



## extract article information
article_data = soup.find(id = 'article-data')
# footnotes
# foot_notes_tag = article_data.find(id = 'footnotes')
# if foot_notes_tag is not None:
#     foot_notes = []
#     for foot_note in foot_notes_tag.find_all('p'):
#         foot_notes.append(foot_note.text)
    
#     print foot_notes

# references
# references_tag = article_data.find(id = 'references')
# if references_tag is not None:
#     references = []
#     for reference in references_tag.find_all(class_ = 'ref'):
#         references.append(reference.select_one('.body').text)

#     for refrence in references:
#         print refrence

# authors
# authors_tag = article_data.find(id = 'authors')
# if authors_tag is not None:
#     authors = []
#     for author in authors_tag.find_all(class_ = 'author'):
#         author_image = author.find('img')['src']
#         author_link = author.find('a')['href']
#         author_bio = author.select_one('.bio').text
#         authors.append({'image' : author_image,
#                         'link' : author_link,
#                         'bio' : author_bio
#                         })
# #     print authors
# 
# # citedby
# citedby_tag = article_data.find(id = 'citedby')
# if citedby_tag is not None:
#     citedby = []
#     for cityby_i in citedby_tag.find_all(class_ = 'ref ieee'):
#         pass
# 
# # keywords
# keywords_tag = article_data.find(id = 'keywords')
# if keywords_tag is not None:
#     keywords = []
#     for keywords_i in keywords_tag.find_all(class_ = 'block'):
#         keyword_type = keywords_i.h3.text
#         print keyword_type
#         _keywords = []
#         for keyword_link in keywords_i.find_all('a'):
#             _keywords.append(keyword_link.text)
#         keywords.append({keyword_type: _keywords})
#     print keywords
# else:
#     print None
        
# for para in soup.find(id='sec1').find_all('p'):
#     para.a.extract()

# for para in soup.find(id='sec1').find_all('p'):
#     print para