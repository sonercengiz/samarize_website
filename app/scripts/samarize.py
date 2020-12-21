import pandas as pd
import re
import nltk
from nltk.corpus import stopwords;
from nltk.tokenize import sent_tokenize,word_tokenize
import numpy as np
import matplotlib.pyplot as plt
import json
import statistics

import json
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
#from sklearn.preprocessing import PolynomialFeatures
#from sklearn.linear_model import LinearRegression

with open("app/scripts/en-stopwords.json", encoding="utf8") as json_file:
    stopwords = json.load(json_file)

def remove_parantheses_sentences(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    ret = re.sub(r'\s+', ' ', ret)
    return ret

def remove_punct(text):
    new_words = []
    for word in text:
        w = re.sub(r'[^\w\s]',' ',word) #remove everything except words and space#how 
                                        #to remove underscore as well
        w = re.sub(r'\_',' ',w)
        w = re.sub(r'\s+', ' ', w)
        new_words.append(w)
    return "".join(new_words)

def find_frequencies(text):
    flist = text.split()
    frequencies = {}
    for f in flist:
        f = f.lower()
        if f not in stopwords:
            if f not in frequencies.keys():
                frequencies[f] = 1
            else:
                frequencies[f] += 1
    sort_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    return frequencies

def samarize(text):
    a_t = text
    formatted_article_text = remove_punct(remove_parantheses_sentences(a_t))
    sentence_list = nltk.sent_tokenize(a_t)
    
    word_frequencies = find_frequencies(a_t)
                
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        

    # counts = []
    # for i in range(len(sentence_list)):
    #     longest = wordCount(sentence_list[0])
    #     counts.append(wordCount(sentence_list[i]))
    #     if longest < wordCount(sentence_list[i]):
    #         longest = sentence_list[i]

    
    # limit = statistics.quantiles(counts)[2]
    
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():

                if len(sent.split(' ')) < 50:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
                        
    it = iter(sentence_scores.values())
    X = []
    Y = []
    for i in range(len(sentence_scores)):
        X.append(i)
        Y.append(next(it))
        
    lim = np.full((1, len(Y)), statistics.mean(Y))
    #lim = withPolyReg(X, Y)
        
    plt.scatter(X, Y)
    plt.scatter(X, lim)
    plt.show()
    
    art = []
    for (sent, score) in sentence_scores.items(): 
        if score>statistics.mean(Y):
            #0, 4, 5, 9, 10, 14, 15, 17
            art.append(remove_parantheses_sentences(sent))
    return " ".join(art)

def twodarray(serie):
    return np.array(list(serie)).reshape(-1,1)

def withPolyReg(X, Y): # it gives predict_y
    poly = PolynomialFeatures(degree = 1)
    x_poly = poly.fit_transform(twodarray(X))
    pilreg = LinearRegression()
    pilreg.fit(x_poly, twodarray(Y))
    return pilreg.predict(poly.fit_transform(twodarray(X)))