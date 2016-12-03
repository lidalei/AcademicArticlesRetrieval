import cookielib, urllib2, os, time
from bs4 import BeautifulSoup

article_net_address_prefix = 'http://ieeexplore.ieee.org/xpls/icp.jsp?arnumber='

# acquire all IDs
root_dir = '../Resources/Request Again/'

article_IDs = []

for filename in os.listdir(root_dir):
    if filename.endswith('.xml'):
        article_IDs.append(filename[:7])
# with open(root_dir + '500_full_text.txt', 'r') as f:
#     for line in f:
#         if(line != ''):
#             article_IDs.append(line[:7])
#         else:
#             break
#         
# f.close()

if article_IDs is not None:
    # create Cookie
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    try:
        request_net_address = 'http://ieeexplore.ieee.org/xpls/icp.jsp?arnumber=6909894'
        full_text_response = opener.open(request_net_address, timeout = 5000)
    except urllib2.HTTPError, error:
        print 'Create Cookie Error:', error.code
    # Crawl data
    for article_ID in article_IDs:
        # request Full Text
        try:
            request_net_address = article_net_address_prefix + str(article_ID)
            full_text_response = opener.open(request_net_address, timeout = 10000)
            with open(str(article_ID) + '_full_text.xml', 'w') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\r\n')
                html_doc = full_text_response.read()
                soup = BeautifulSoup(html_doc, 'html.parser')
                # extract article
                article_tag = soup.find(id = 'article')
                f.write(str(article_tag))
            f.close()
        except urllib2.HTTPError, error:
            print str(article_ID) + '_full_text: ', error.code
        time.sleep(5)