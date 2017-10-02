import nltk
from nltk.corpus import conll2000
print(conll2000.chunked_sents('train.txt')[99])