
import nltk
import pickle

with open("pornstars.pickle", "rb") as f:
    stars = pickle.load(f)

with open("genres.pickle", "rb") as f:
    genres = pickle.load(f)
        

with open("extra_terms.pickle", "rb") as f:
    extra_terms = pickle.load(f)

nsfw = stars + genres + extra_terms 

nsfw.remove("with")
nsfw.remove("rock")

bigg_boss_counter = 0
explicit_content = []

# def extract_entities(text):
#     for sent in nltk.sent_tokenize(text):
#         return nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)))

def is_explicit(word):
    if word.lower() in nsfw:
        explicit_content.append(word)
        return True
    else:
        return False

def is_bigg_boss(word):
    global bigg_boss_counter

    if word in ["bigg", "boss"]:
       bigg_boss_counter += 1 
       return True
    else:
        return False

with open('log.csv') as log:
    
    for line in log:

        search_query = line[line.rfind(":")+1:].rstrip()
        
        for i in search_query.split(" "):    
            if is_explicit(i):
                break

      
        for i in search_query.split(" "):    
            if is_bigg_boss(i):
                break

print len(explicit_content), bigg_boss_counter
