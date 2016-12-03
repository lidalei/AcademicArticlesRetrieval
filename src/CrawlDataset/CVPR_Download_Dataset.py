import cookielib, urllib2, json, time

article_net_address_prefix = 'http://ieeexplore.ieee.org/rest/xpls/'

article_full_text_prefix = article_net_address_prefix + 'Fulltext/amsid/'

article_data_types = ['InfoSection', 'Abstract', 'LeftPanelInfo', 'Footnotes', 'References',
                      'Authors', 'Citedby', 'Keywords', 'RecommendedArticles']

dataset_links_prefix = [
                 article_net_address_prefix + 'InfoSection/amsid/',
                 article_net_address_prefix + 'Abstract/amsid/',
                 article_net_address_prefix + 'LeftPanelInfo/amsid/',
                 article_net_address_prefix + 'Footnotes/amsid/',
                 article_net_address_prefix + 'References/amsid/',
                 article_net_address_prefix + 'Authors/amsid/',
                 article_net_address_prefix + 'Citedby/amsid/',
                 article_net_address_prefix + 'Keywords/amsid/',
                 'http://ieeexplore.ieee.org/xpl/getRecommendedArticlesAsJsonResponse?arnumber=']


# get the first article ID
article_first_ID = int(raw_input("Please input the ID of the first article:"))
print 'your input is {}'.format(str(article_first_ID))
# get the last article ID
article_last_ID = int(raw_input("Please input the ID of the last article:"))
print 'your input is {}'.format(str(article_last_ID))
if article_first_ID > article_last_ID:
    print 'Illegal input combination'
else:
    # collect data from network
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    try:
        request_net_address = 'http://ieeexplore.ieee.org/xpls/icp.jsp?arnumber=6909894'
        full_text_response = opener.open(request_net_address, timeout = 5000)
    except urllib2.HTTPError, error:
        print 'Create Cookie Error:', error.code
    for article_ID in range(article_first_ID, article_last_ID + 1):
        # request Full Text
        try:
            request_net_address = article_full_text_prefix + str(article_ID)
            full_text_response = opener.open(request_net_address, timeout = 5000)
            with open(str(article_ID) + '_full_text.xml', 'w') as f:
                f.write(full_text_response.read())
            f.close()
        except urllib2.HTTPError, error:
            print str(article_ID) + '_full_text: ', error.code
        # request article data
        for dataset_link_prefix, data_type in zip(dataset_links_prefix, article_data_types):
            try:
                related_data_response =  urllib2.urlopen(dataset_link_prefix + str(article_ID), timeout = 5000)
                with open(str(article_ID) + '_' + data_type + '.json', 'w') as f:
                    json.dump(related_data_response.read(), f)
                f.close()
            except urllib2.HTTPError, error:
                print str(article_ID) + '_' + data_type + ': ', error.code
        time.sleep(2)