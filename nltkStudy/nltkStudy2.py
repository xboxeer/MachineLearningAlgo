import nltk
my_train_set=[
    ({'feature1':'a'},'1'),
    ({'feature1':'a'},'1'),
    ({'feature1':'a'},'1'),
    ({'feature1':'a'},'3'),
    ({'feature1':'b'},'2'),
    ({'feature1':'b'},'2'),
    ({'feature1':'b'},'2'),
    ({'feature1':'b'},'2'),
    ({'feature1':'b'},'2'),
    ({'feature1':'b'},'2'),
]
classifier=nltk.NaiveBayesClassifier.train(my_train_set)
print(classifier.classify({'feature1':'a'}))
print(classifier.classify({'feature1':'b'}))