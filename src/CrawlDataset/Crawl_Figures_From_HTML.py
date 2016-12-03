import os, json, cookielib, urllib2, time
# crawl missing figures from HTML

figures_network_addr_prefix = 'http://ieeexplore.ieee.org/xpls/icp.jsp?arnumber='
# article_ID
figures_netword_addr_suffix = '&pgName=figures'

dataset_folder_name = '../Dataset/'
figures_name = 'figures.json'
    
# all_figures = {}

# create Cookie
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
try:
    request_net_address = 'http://ieeexplore.ieee.org/xpls/icp.jsp?arnumber=6909894'
    full_text_response = opener.open(request_net_address, timeout = 5000)
except urllib2.HTTPError, error:
    print 'Create Cookie Error:', error.code

with open(dataset_folder_name + figures_name, 'w') as f:
    for sub_folder_name in os.listdir(dataset_folder_name):
        if os.path.isdir(dataset_folder_name + sub_folder_name):
            figures_folder = dataset_folder_name + sub_folder_name + '/Figures/'
            figures_files_list = os.listdir(figures_folder)
            # get all IDs
            article_IDs = []
            for figure_file in figures_files_list:
                if figure_file.endswith('.json'):
                    with open(figures_folder + figure_file) as figure_f:
                        figure_info = json.loads(json.load(figure_f))['response']
                        if 'fig' not in figure_info:
                            article_IDs.append(figure_info['amsid'])
                    figure_f.close()
            # download html files
            for article_ID in article_IDs:
                # request the html file
                try:
                    request_net_address = figures_network_addr_prefix + str(article_ID) + figures_netword_addr_suffix
                    html_response = opener.open(request_net_address, timeout = 10000)
                    with open(figures_folder + str(article_ID) + '_figures.html', 'w') as html_f:
                        html_f.write(html_response.read())
                    html_f.close()
                except urllib2.HTTPError, error:
                    print str(article_ID) + '_figures: ', error.code
                print article_ID
                time.sleep(2)
f.close()