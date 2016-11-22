import re
import nltk
import pickle

from nltk.corpus import stopwords
stop = set(stopwords.words('english'))

from langdetect import detect

import enchant
english_dict = enchant.Dict("en_US")

with open("pornstars.pickle", "rb") as f:
    stars = pickle.load(f)

with open("genres.pickle", "rb") as f:
    genres = pickle.load(f)
        

with open("extra_terms.pickle", "rb") as f:
    extra_terms = pickle.load(f)


with open("tvshows.pickle", "rb") as f:
    tvshows = pickle.load(f)

with open("english_movies.pickle", "rb") as f:
    english_movies = pickle.load(f)


with open("softwares.pickle", "rb") as f:
    softwares = pickle.load(f)

with open("games.pickle", "rb") as f:
    games = pickle.load(f)

nsfw = stars + genres + extra_terms 

nsfw.remove("with")
nsfw.remove("rock")

indiantv_content = []
tvshow_content = []
explicit_content = []
englishmovie_content = []
indianmovie_content = []
games_content = []
software_content = []
hindi_query = 0
english_query = 0

# def extract_entities(text):
#     for sent in nltk.sent_tokenize(text):
#         return nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)))

def is_explicit(word):
    if word in nsfw and word not in stop:
        return True
    else:
        return False

def is_tvshow(word):

    if word in tvshows and word not in stop:
        return True
    else:
        return False


def is_englishmovie(word) :

    if word in english_movies and word not in stop:
        return True
    else:
        return False



def is_software(word) :

    if word in softwares and word not in stop:
        return True
    else:
        return False

def is_game(word) :

    if word in games and word not in stop:
        return True
    else:
        return False

def is_indiantv(word):

    if word in ["bigg", "boss", "koffee", "kofee", "karan", "kapil", "sharma", "bachao", "comedy", "mahabharat"]:
       return True
    else:        
        return False

def is_indianmovie(word):
    
    if word in ["shivaay", "shivay", "rock", "force", "dil", "mushkil", "rockstar", "hindi", "bollywood"]:
       return True
    else:        
        return False

with open('log.csv') as log:
    
    for line in log:
        search_query = line[line.rfind(":")+1:].lower().rstrip()
        
        for i in search_query.split(" "):    
            if is_explicit(i):
                explicit_content.append(search_query)
                break
        else:
          
            for i in search_query.split(" "):    
                if is_indiantv(i):
                    indiantv_content.append(search_query)
                    break
            else:
                
                for i in search_query.split(" "):    
                    if is_indianmovie(i):
                        indianmovie_content.append(search_query)
                        break
                else:
                    search_query_tv = re.sub(r"s(\d{1,2})e(\d{1,2})", "", search_query)
                    search_query_tv = re.sub(r"s(\d{1,2})", "", search_query_tv)
                    search_query_tv = re.sub(r"e(\d{1,2})", "", search_query_tv)
                    search_query_tv = search_query_tv.rstrip()
                    for i in search_query_tv.split(" "):
                        if is_tvshow(i):
                            tvshow_content.append(search_query)
                            break
                    else:

                        for i in search_query.split(" "):
                            if is_englishmovie(i):
                                englishmovie_content.append(search_query)
                                break
                        else:
                            
                            for i in search_query.split(" "):
                                if is_software(i):
                                    software_content.append(search_query)
                                    break
                            else:

                                for i in search_query.split(" "):
                                    if is_game(i):
                                        games_content.append(search_query)
                                        break
                                else:
                                    for i in search_query.split(" "):
                                        if english_dict.check(i):# or detect(i) == "en":
                                            english_query += 1
                                            break
                                    else:
                                        hindi_query += 1
print 
print "Explicit:", len(explicit_content)
print "Indian TV:", len(indiantv_content)
print "Indian movies:",  len(indianmovie_content)
print "English TV:",  len(tvshow_content)
print "English movies:",  len(englishmovie_content)
print "Games:",  len(games_content)
print "Software:",  len(software_content)
print "Hindi:",  hindi_query
print "English:",  english_query
print
#padhai
#songs
#hindi