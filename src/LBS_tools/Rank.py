'''
Created on Oct 18, 2015

@author: s151898
'''

def rank_list(to_rank_list,k=5):
    ranked_list = sorted(to_rank_list, key = lambda torank_list: torank_list['probability'], reverse = True)
    ranked_list = ranked_list[0:k]
    return ranked_list

def rank_list_similarity(to_rank_list,k=5):
    ranked_list = sorted(to_rank_list, key = lambda torank_list: torank_list['similarity'], reverse = True)
    ranked_list = ranked_list[0:k]
    return ranked_list

def rank_dict_label(to_rank_dict):
    ranked_list = sorted(to_rank_dict.items(), lambda x, y: cmp(x[1], y[1]),reverse=True)
    return ranked_list


# print rank_dict_label({"a":0,"b":3,"c":2})