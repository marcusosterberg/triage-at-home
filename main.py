# http://www.nltk.org/api/nltk.stem.html
# http://snowball.tartarus.org/algorithms/swedish/stemmer.html

import nltk
from nltk.stem.snowball import SwedishStemmer
# nltk.download('stopwords')

swedish_stemmer = SwedishStemmer()	#(ignore_stopwords=False)
# print(swedish_stemmer.stem('snuvig'))

def remove_stopwords(s):
    stopwords = set(w.rstrip() for w in open('resources/stopwords_se.txt'))

    s = s.lower() # downcase
    tokens = nltk.tokenize.word_tokenize(s) # split string into words (tokens)
    tokens = [t for t in tokens if len(t) > 2] # remove short words, they're probably not useful
    # tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # put words into base form
    tokens = [t for t in tokens if t not in stopwords] # remove stopwords
    return tokens

s = "Haft hosta under den senaste tiden. Är rökare och har känt sig snuvig i faktiskt flera månader och har även misstanke om någon form av allergi"
s = remove_stopwords(s)

tags = nltk.pos_tag(s)
# print(tags)

print(nltk.ne_chunk(tags))

# nltk.stem.snowball.demo()

# print(remove_stopwords(s))