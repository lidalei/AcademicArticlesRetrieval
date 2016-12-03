'''
Created on Oct 15, 2015

@author: Dalei
'''
import os, sys, json
from bs4 import BeautifulSoup

def extract_figures(dataset_folder_name = '../Dataset/', figures_name = 'figures.json'):
    # extract figures
    
    figures_network_addr_prefix = {'CVPR 2007': 'ielx5/4269955/4269956/',
                                   'CVPR 2008': 'ielx5/4558014/4587335/',
                                   'CVPR 2009': 'ielx5/5191365/5206488/',
                                   'CVPR 2010': 'ielx5/5521876/5539770/',
                                   'CVPR 2011': 'ielx5/5968010/5995307/',
                                   'CVPR 2012': 'ielx5/6235193/6247647/',
                                   'CVPR 2013': 'ielx7/6596161/6618844/',
                                   'CVPR 2014': 'ielx7/6909096/6909393/'
                                   }
    #  + article_ID
        
    all_figures = {}
    with open(dataset_folder_name + figures_name, 'w') as f:
        for sub_folder_name in os.listdir(dataset_folder_name):
            if os.path.isdir(dataset_folder_name + sub_folder_name):
                figures_folder = dataset_folder_name + sub_folder_name + '/Figures/'
                figures_files_list = os.listdir(figures_folder)
                
                figures_dict = {}
                for figure_file in figures_files_list:
                    if figure_file.endswith('.json'):
                        # get figures for an article
                        figures = {}
                        with open(figures_folder + figure_file) as figure_f:
                            figure_info = json.loads(json.load(figure_f))['response']
                            article_ID = figure_info['amsid']
                            print article_ID
                            figures['Title'] = figure_info['doc-title']
                            figures['fig'] = []
                            if 'fig' in figure_info:
                                for index, fig in zip(range(len(figure_info['fig'])), figure_info['fig']):
                                    if 'id' in fig and 'fig' in fig['id']:
                                        figure_label = fig['label'][:-1]
                                        figure_src = figures_network_addr_prefix[sub_folder_name] + article_ID + '/html/img/' + article_ID + '-fig-' + str(index + 1) + '-large.gif'
                                        figure_caption = BeautifulSoup(fig['caption'], 'html.parser').text
                                        figures['fig'].append({'label': figure_label, 'src': figure_src, 'caption': figure_caption})
                            else:
                                # get data from html file
                                with open(figures_folder + article_ID + '_figures.html', 'r') as html_f:
                                    soup = BeautifulSoup(html_f.read(), 'html.parser')
                                    for figure_section in soup.find_all('div', class_ = 'section'):
                                        if 'fig' in figure_section['id']:
                                            figure_label = figure_section.find(class_ = 'header').text
                                            figure_src = figure_section.find(class_ = 'img-wrap').img['src'][1:]
                                            figure_caption = figure_section.find(class_ = 'figcaption').text
                                        figures['fig'].append({'label': figure_label, 'src': figure_src, 'caption': figure_caption})
                                html_f.close()
                            figures_dict[article_ID] = figures
                        figure_f.close()
                
                all_figures[sub_folder_name] = figures_dict
                
        json.dump(all_figures, f)
        
    f.close()
    
    
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        extract_figures()
    elif len(sys.argv) <= 2:
        extract_figures(sys.argv[1])
    else:
        extract_figures(sys.argv[1], sys.argv[2])