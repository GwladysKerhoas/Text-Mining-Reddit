#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:10:45 2021

@author: gwladyskerhoas
"""


################################## Création du Corpus ##################################

import praw
import urllib.request
import xmltodict 
import datetime as dt 
import Module_classe as md 
import Fonctions_support as fs
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


# Création des deux sources de données à comparer sur le même sujet d'étude
corpus_reddit = md.Corpus("Corona")
corpus_arxiv = md.Corpus("Corona")


# Source 1 : Document Reddit
reddit = praw.Reddit(client_id='0AlqCfHuOc5Hkg', client_secret='80PspjYMdTvF91ti9qZeWzAS2BU', user_agent='Reddit Irambique')
hot_posts = reddit.subreddit('Coronavirus').hot(limit=100)
for post in hot_posts:
    datet = dt.datetime.fromtimestamp(post.created)
    txt = post.title + ". "+ post.selftext
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = md.Document(datet,
                   post.title,
                   post.author_fullname,
                   txt,
                   post.url)
    corpus_reddit.add_doc(doc)
    
print("Création du corpus Reddit, %d documents et %d auteurs" % (corpus_reddit.ndoc,corpus_reddit.naut))


# Source 2 : Document Arxiv
url = 'http://export.arxiv.org/api/query?search_query=all:covid&start=0&max_results=100'
data =  urllib.request.urlopen(url).read().decode()
docs = xmltodict.parse(data)['feed']['entry']

for i in docs:
    datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
    try:
        author = [aut['name'] for aut in i['author']][0]
    except:
        author = i['author']['name']
    txt = i['title']+ ". " + i['summary']
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = md.Document(datet,
                   i['title'],
                   author,
                   txt,
                   i['id']
                   )
    corpus_arxiv.add_doc(doc)


print("Création du corpus Arxiv, %d documents et %d auteurs" % (corpus_arxiv.ndoc,corpus_arxiv.naut))




####################### Etude comparative de la fréquence des mots #############################


# Etape 1 : Analyse des fréquences de mots contenus dans les corpus
print("Reddit : Matrice des fréquences des termes les plus utilisés") 
corpus_reddit.stats()

print("Arxiv : Matrice des fréquences des termes les plus utilisés")
corpus_arxiv.stats()


# Etape 2 : Etude de l'importance des mots dans les corpus
print("Reddit : Méthode TF-IDF avec sklearn")
New_Reddit = corpus_reddit.tokenize() # Récupération des mots sans les stopwords
vectorizer = TfidfVectorizer()
X_Reddit = vectorizer.fit_transform(New_Reddit)
#print(vectorizer.get_feature_names())
print(X_Reddit.shape)
print(X_Reddit)

print("Arxiv : Méthode TF-IDF avec sklearn")
New_Arxiv = corpus_arxiv.tokenize() # Récupération des mots sans les stopwords
vectorizer = TfidfVectorizer()
X_Arxiv = vectorizer.fit_transform(New_Arxiv)
#print(vectorizer.get_feature_names())
print(X_Arxiv.shape)
print(X_Arxiv)



# Etape 3 : Nuage des mots des deux corpus
fs.show_wordcloud(New_Reddit) # Appel de la fonction show_wordcloud()
fs.show_wordcloud(New_Arxiv)



# Enregistrement de nos corpus
print("Enregistrement du corpus sur le disque...")
corpus_reddit.save("Corona_Reddit.crp")
corpus_arxiv.save("Corona_Arxiv.crp")









