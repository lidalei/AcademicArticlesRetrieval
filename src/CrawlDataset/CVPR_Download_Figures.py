import os, time, urllib2, cookielib, json

root_network_address = 'http://ieeexplore.ieee.org/'

figures_network_address_prefix = root_network_address + 'rest/xpls/Figures/amsid/'

figures_network_address_prefix_dict = {'2007': 'ielx5/4269955/4269956/',
                                  '2008': 'ielx5/4558014/4587335/',
                                  '2009': 'ielx5/5191365/5206488/',
                                  '2010': 'ielx5/5521876/5539770/',
                                  '2011': 'ielx5/5968010/5995307/',
                                  '2012': 'ielx5/6235193/6247647/',
                                  '2013': 'ielx7/6596161/6618844/',
                                  '2014': 'ielx7/6909096/6909393/'
                                  }

for key in figures_network_address_prefix_dict.keys():
    dataset_dir = '../Dataset/CVPR ' + key + '/'
    # get all article IDs
    article_IDs = []
     
    for file_name in os.listdir(dataset_dir):
        if file_name.endswith('.xml'):
            if file_name[:7] > '6909872':
                article_IDs.append(file_name[:7])
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
            # request the json file explaning Figures
            try:
                request_net_address = figures_network_address_prefix + str(article_ID)
                figures_response = opener.open(request_net_address, timeout = 10000)
                with open(dataset_dir + 'Figures/' + str(article_ID) + '_figures.json', 'w') as f:
                    json.dump(figures_response.read(), f)
                f.close()
                # downloading figures
            except urllib2.HTTPError, error:
                print str(article_ID) + '_figures: ', error.code
            print article_ID
            time.sleep(5)