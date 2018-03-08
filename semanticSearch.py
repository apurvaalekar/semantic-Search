# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#from _future_ import print_function
#from _future_ import print_function
import pysolr
import os
import sys
solr = pysolr.Solr('http://localhost:8983/solr/xyz/', timeout=10000)
path = sys.argv[1]

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
documents = []
totalWords=0
totalSentence=0
for filename in os.listdir(path):

    f = open(path+'/'+filename)
    raw = f.read()
    sentence = sent_tokenize(raw)
    
    sentId=1 
    for s in sentence:
        s = s.replace('\n', '')
        totalSentence+=1
        words = word_tokenize(s)
        totalWords+=len(words)
        id = str(filename) + "|" + str(sentId)
        doc = {
        "id": id,
        "sentence": s,
        "words":words
        }
        documents.append(doc)
        sentId+=1
    f.close()
   
print("total Sentence:",totalSentence)
print("total Words:",totalWords)
solr.add(documents)
                                                                                                                                                                                                         

#solr.search('food')
def input_query():
    input_sen = input("Enter Query String:")
   
    
    sent_words = word_tokenize(input_sen)
    
    query = "words:("+" ".join(sent_words)+")"
   
   
        
    print("The query is:"+query)
    results = solr.search(query+"&fl=*,score&sort=score desc")
    for result in results:
        print(result['id']+" "+result['sentence'][0]) 
        
input_query()