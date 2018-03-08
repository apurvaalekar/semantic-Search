# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 14:55:07 2017

@author: apurva
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pysolr
import os
import sys
solr = pysolr.Solr('http://localhost:8983/solr/task3/', timeout=10000)
import nltk
path = sys.argv[1]

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from rake_nltk import Rake
lemmatizer = WordNetLemmatizer()
st = LancasterStemmer()
r= Rake()
documents = []

totalWords = 0
totalSentence=0
for filename in os.listdir(path):

    f = open(path+'/'+filename)
    raw = f.read()
    sentence = sent_tokenize(raw)
    sentId=1 
    for sen in sentence:
        totalSentence+=1
        words = word_tokenize(sen)
        totalWords+=len(words)
        lemma = []
        stem = []
        hypernym = []
        holonym=[]
        meronym=[]
        hyponym=[]
        phrases=[]
        top6_phrases =[]
        pos=[]
        r.extract_keywords_from_text(sen)
        phrases=r.get_ranked_phrases()
        top6_phrases=phrases[0:6]
        for w in words:
             syn = wordnet.synsets(w)
            
             for s in syn:
                 hypo=[]
                 holo=[]
                 mero=[]
                 hyper=[]
                 
                 if len(s.hypernyms())>0:
                     for h in s.hypernyms():
                         hyper.append(h.name())
                     hypernym.extend(list(set(hyper)))
                 if len(s.member_holonyms())>0:
                     for h in s.member_holonyms():
                         holo.append(h.name())
                     holonym.extend(list(set(holo)))
                 if len(s.part_meronyms())>0:
                     for h in s.part_meronyms():
                         mero.append(h.name())
                     meronym.extend(list(set(mero)))
                 if len(s.hyponyms())>0:
                     for h in s.hyponyms():
                         hypo.append(h.name())
                     hyponym.extend(list(set(hypo)))
             lemma.append(lemmatizer.lemmatize(w))
             stem.append(st.stem(w))
        #headword =  StanfordDependencyParser.hea
        for tag in nltk.pos_tag(words):
            pos.append(tag[0]+"|"+tag[1])
        #pos.append(nltk.pos_tag(words)[])
        id = str(filename) + "|" + str(sentId)
        doc = {
        "id": id,
        "sentence": sen,
        "lemma":lemma,
        "stem":stem,
        "hypernyms":hypernym,
        "holonym":holonym,
        "meronym":meronym,
        "hyponym":hyponym,
        "pos":pos,
        "words":words,
        "phrases":top6_phrases
        }
        documents.append(doc)
        sentId+=1
    f.close()
    
print("total Words:",totalWords)
print("total Sentence:",totalSentence)
solr.add(documents)
input_sen=""

def query_input():
    input_sen = input("Enter Query String")
   
    sent_words = word_tokenize(input_sen)
    hypo=[]
    holo=[]
    mero=[]
    hyper=[]
    sent_lemma =[]
    sent_stem=[]
    sent_pos=[]
    r.extract_keywords_from_text(input_sen)
    sen_phrases=r.get_ranked_phrases()
    input_phrases=sen_phrases[0:6]
    for word in sent_words:
        syn = wordnet.synsets(word)
        for s in syn:
            if len(s.hypernyms())>0:
                for h in s.hypernyms():
                    hyper.append(h.name())
            if len(s.member_holonyms())>0:
                for h in s.member_holonyms():
                    holo.append(h.name())
                         
            if len(s.part_meronyms())>0:
                for h in s.part_meronyms():
                    mero.append(h.name())
                         
            if len(s.hyponyms())>0:
                for h in s.hyponyms():
                    hypo.append(h.name())
                         
        sent_lemma.append(lemmatizer.lemmatize(word))
        sent_stem.append(st.stem(word))
    for tag in nltk.pos_tag(sent_words):
            sent_pos.append(tag[0]+"|"+tag[1])    
    query=[]
    if(len(sent_words))>0:
        query1 = "words:" + " || words:".join(sent_words)
        query.append(query1)
    if(len(sent_lemma)>0):
        query2 = "lemma:" + " || lemma:".join(sent_lemma)
        query.append(query2)
    if(len(sent_stem)>0):
        query3 = "stem:" + " || stem:".join(sent_stem)
        query.append(query3)
    if(len(sent_pos)>0):
        query4 = "pos:" + " || pos:".join(sent_pos)
        query.append(query4)
    if(len(input_phrases)>0):
        query5 = "phrases:" + " || phrases:".join(input_phrases)
        query.append(query5)
    if(len(hyper)>0):
        query6 = "hypernyms:" + " || hypernyms:".join(hyper)
        query.append(query6)
    if(len(hypo)>0):
        query7 = "hyponym:" + " || hyponym:".join(hypo)
        query.append(query7)
    if(len(mero)>0):
        query8 = "meronym:" + " || meronym:".join(mero)
        query.append(query8)
    if len(holo)>0:
        query9 = "holonym:" + " || holonym:".join(holo)
        query.append(query9)
   
    joinedQuery = ' || '.join(item for item in query)
    print(joinedQuery)
    results = solr.search(joinedQuery)
    for result in results:
        print(result['id']+" "+result['sentence'][0]) 
        
query_input()