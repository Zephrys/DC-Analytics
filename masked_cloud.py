#!/usr/bin/env python
"""
Masked wordcloud
================
Using a mask you can generate wordclouds in arbitrary shapes.
"""

from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from wordcloud import WordCloud
from scipy.misc import imread


d = path.dirname(__file__)

# # Read the whole text.
# text = open(path.join(d, 'alice.txt')).read()

# # read the mask image
# # taken from
# # http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg

stop = stopwords.words("english")
stop.append("boss")
stop.append("bang")
stop.append("big")
stop.append("theory")

def make(category, img_link):
    
    with open('clog.csv') as clog:
        
        words = ""

        for line in clog:
            try:
                line_cat = int(line.split(",")[-2])
                if line_cat == category:
                    word = line.split(",")[-3].split(":")[-1]
                    words += word + " "
            except:
                pass

    mask = imread(img_link, flatten=True)

    wc = WordCloud(background_color="white", max_words=1000, mask=mask, stopwords=stop)

    # generate word cloud
    wc.generate(words)

    # store to file
    wc.to_file(path.join(d, "explicit_wc.png"))

    # show
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    make(1, "./silhouette.jpg")
