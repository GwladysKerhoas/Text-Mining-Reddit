#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 18:53:09 2021

@author: gwladyskerhoas
"""


################################## Déclaration des fonctions #############################


import unittest
import Module_classe as md 
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
stopwords = set(STOPWORDS)


# Représentation des termes les plus fréquents sous forme de nuage de points
def show_wordcloud(data, title = None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40, 
        scale=3,
        random_state=1 
    ).generate(str(data))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()



# Tests unitaires
class Tests(unittest.TestCase):
    
    # Test de la méthode nettoyer_texte()
    def test_nettoyer_texte(self):
        result = md.nettoyer_texte("Nettoyer ce TEXTE")
        self.assertEqual(result,"nettoyer ce texte")

if __name__ == '__main__':
    unittest.main()


