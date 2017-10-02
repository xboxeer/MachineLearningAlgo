import nltk
from nltk.corpus import movie_reviews
all_words=nltk.FreqDist(w.lower for w in movie_reviews.words())
word_features=all_words.keys()[0:2000]
def document_features(document):
    for word in word_features:
        features['contains(%s)'%word]=(word in do)