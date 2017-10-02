import nltk
default_tag=nltk.DefaultTagger('NN')
raw='我 勒 个 去'
tokens=nltk.word_tokenize(raw)
tags=default_tag.tag(tokens)
print(tags)

partten=[(r'.*们$','PRO')]
tagger=nltk.RegexpTagger(partten)
print(tagger.tag(nltk.word_tokenize('我们 了 个 去 你们')))