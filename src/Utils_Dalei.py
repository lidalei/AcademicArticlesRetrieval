import string, nltk

pre_process_configuration = {'stop words': True,
                             'stop words set': 'english',
                             'stemming': True,
                             'stemming type': 'Lancaster' # Porter
                             }

def stemmer():
    # construct a stemmer
    stemmer_type = pre_process_configuration['stemming type']
    if stemmer_type == 'Lancaster':
        return nltk.stem.lancaster.LancasterStemmer()
    elif stemmer_type == 'Porter':
        return nltk.stem.porter.PorterStemmer()
    return nltk.stem.lancaster.LancasterStemmer()

def tokenizer(text):
    
    # tokenization with / without stemming
    
    # first, tokenization, ignore length one tokens
    temp_tokens = [token for token in nltk.tokenize.word_tokenize(text, language='english') if string.find(token, '\\') == -1 and len(token) > 1]        
    
    tokens = []
    
    for token in temp_tokens:
        flag = True
        for ch in string.punctuation:
            if ch in token:
                flag = False
                break
        if flag is True:
            tokens.append(token)
        
    # second, stemming or not
    
    stemming = pre_process_configuration['stemming']
    
    if stemming is True:
        stemmer_ = stemmer()
        return [stemmer_.stem(token) for token in tokens]
    else:
        return tokens
    
def remove_equations(text):
    # remove equations
    
    result_text = ''
    
    non_equation_start_index = 0
    while True:
        equation_start_index = string.find(text, '\\$', non_equation_start_index)
        if equation_start_index != -1:
            # extract the non-equation content
            result_text += text[non_equation_start_index: equation_start_index]
            # deal with next equation mark
            equation_end_index = string.find(text, '\\$', equation_start_index + 2)
            if equation_end_index != -1:
                non_equation_start_index = equation_end_index + 3
                if non_equation_start_index == len(text):
                    break
            else:
                break
        else:
            result_text += text[non_equation_start_index:]
            break
    return result_text


def remove_punctuation(text):
    # remove punctuation
    result_text = ''
    self_punctuation = '+-*/1234567890^_$'
    
    for ch in text:
        if ch not in self_punctuation:
            result_text += ch
    return result_text


def cosine_similarity(vec1, vec2):
    # compute similarity between two normalized vectors
    
    if len(vec1) != len(vec2):
        return False
    similarity = 0
    for vec1_element, vec2_element in zip(vec1, vec2):
        similarity += vec1_element * vec2_element
    return similarity