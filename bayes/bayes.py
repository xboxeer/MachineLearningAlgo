from numpy import *
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

#数据集中每个句子中包含的单词构成vocabList
#然后vocabList和sentance映射 
#比如sentance=['I','Love','you']
#vocabList=['I','U','Love','This','Is']
#得出映射结果就是[1,1,1,0,0]
def setOfWords2Vec(vocabList,sentance):
    #returnValue=[0]*len(vocabList)
    #for word in sentance:
    #    if word in vocabList:
    #        returnValue[vocabList.index(word)]=1
    #print(returnValue)
    returnValue=[(1 if sentance.count(example)>0 else 0) for example in vocabList]
    return returnValue
vec=setOfWords2Vec(vocabList,dataSet[1])

#trainMatrix是已经通过setOfWords2Vec数值化了的句子
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)
    numWords=len(trainMatrix[0])#其实整个数据集里面包含的不同的单词
    #此处因为trainCategory里面侮辱性语句标识为1，
    #因此sum(trainCategory)可以得到侮辱性语句总数，
    #除以文档总数就可以得到侮辱性语句的概率pAbusive
    #1-pAbusive就是非侮辱性语句的概率
    pAbusive=sum(trainCategory)/float(numTrainDocs)
    #p0num=zeros(numWords)#初始矩阵 意思是没有单词在普通语句里面出现过
    p0num=ones(numWords)#用1代替0来初始化矩阵
    #p1num=zeros(numWords)#初始矩阵 意思是没有单词在侮辱性语句里面出现过
    p1num=ones(numWords)#用1代替0来初始化矩阵
    p0Denom=2.0#英文初始化p0num矩阵用了1，用2代替0来初始化普通语句中单词总数量
    p1Denom=2.0#英文初始化p1num矩阵用了1，用2代替0来初始化侮辱性语句中单词总数量
    for i in range(numTrainDocs):
        if trainCategory[i]==1:#当前句子为侮辱性语句
            p1num+=trainMatrix[i]#句子矩阵相加（增加某词汇在侮辱性语句里出现次数）
            p1Denom+=sum(trainMatrix[i])#计算侮辱性语句里单词的总数
        else:
            p0num+=trainMatrix[i]#当前句子为普通语句，句子矩阵相加（增加某词汇在普通语句里出现的次数）
            p0Denom+=sum(trainMatrix[i])#计算普通语句里单词的总数
    p1vect=log(p1num/p1Denom)
    #侮辱性语句集合中词汇计数矩阵/总共有多少词出现在侮辱性语句中=[p(w|c1)],
    # 也就是每个词汇出现在侮辱性语句中的概率的集合
    #取自然对数，防止最后结果相乘时候太小导致四舍五入为0
    p0vect=log(p0num/p0Denom)
    #普通语句集合中词汇计数矩阵/总共有多少词出现在普通语句中=[p(w|c0)],
    #也就是每个词汇出现在普通语句中的概率的集合
    #取自然对数，防止最后结果相乘时候太小导致四舍五入为0
    return p0vect,p1vect,pAbusive

trainMatrix=[setOfWords2Vec(vocabList,example) for example in dataSet]
p0vect,p1vect,pAbusive=trainNB0(trainMatrix,classVec)

print(p0vect)
print(p1vect)
print(pAbusive)
def classifyNB(vec2Classify,p0vect,p1vect,pClass1):
    #p(c1|w1,w2,w3...)=(p(w1|c1)*p(w2|c1)*p(w3|c1)...p(c1))/p(w1,w2,w3....)
    #此处忽略p(w1,w2,w3....)因为对于p0,p1,这个值都一样
    #log(p(c1|w1,w2,w3...))=log(p(w1|c1))+log(p(w2|c1))+log(p(w3|c1))+...+log(p(c1))
    #这里vec2Classify*p1vect意思是
    #比如p0vect=[-2.56494936 -3.25809654 -2.56494936 -2.56494936 -3.25809654 -2.56494936
    #-3.25809654 -3.25809654 -3.25809654 -2.56494936 -2.56494936 -2.56494936
    #-3.25809654 -2.56494936 -2.56494936 -2.56494936 -1.87180218 -3.25809654
    #-2.56494936 -2.56494936 -2.15948425 -2.56494936 -3.25809654 -2.56494936
    #-3.25809654 -2.56494936 -2.56494936 -3.25809654 -3.25809654 -2.56494936
    #-2.56494936 -2.56494936]=[log(p(w1|c0)),log(p(w2|c0)),log(p(w3|c0)),log(p(w4|c0)),.....log(p(w21|c0))]
    #我的输入值语句矩阵vec2Classify是
    #[0,1,0,1,0.....1](输入语句包含词汇组里面的第2,4...最后一个词汇)
    #这样就可以得到一个简单的只包含输入矩阵中每个词汇在整体词汇表的概率的log的集合
    #简化了相当多计算
    p1=sum(vec2Classify*p1vect)+log(pClass1)
    p0=sum(vec2Classify*p0vect)+log(1-pClass1)
    return 1 if p1>p0 else 0

testSentence='this is worthless'.split()
testVec=setOfWords2Vec(vocabList,testSentence)
result=classifyNB(testVec,p0vect,p1vect,pAbusive)
print(result)

