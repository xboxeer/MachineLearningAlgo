def CreateDataSet():
    sentances=['my dog has flea problems help please',
               'maybe not take him to dog park stupid',
               'my dalmation is so cute i love him',
               'stop posting stupid worthless garbage',
               'mr licks ate my steak how to stop him',
               'quit buying worthless dog food stupid']
    dataSet=[example.split() for example in sentances]
    classVec=[0,1,0,1,0,1]
    return dataSet,classVec
dataSet,classVec=CreateDataSet()

def CreateVocabList(dataSet):
    vocabList=set([])
    #return [vocabList|set(example) for example in dataSet]
    for doc in dataSet:
        vocabList=vocabList|set(doc)
    return list(vocabList)
vocabList=CreateVocabList(dataSet)

def setOfWords2Vec(vocabList,sentance):
    #returnValue=[0]*len(vocabList)
    #for word in sentance:
    #    if word in vocabList:
    #        returnValue[vocabList.index(word)]=1
    #print(returnValue)
    returnValue=[(1 if sentance.count(example)>0 else 0) for example in vocabList]
    return returnValue
vec=setOfWords2Vec(vocabList,dataSet[1])
pass