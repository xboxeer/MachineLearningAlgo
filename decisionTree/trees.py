from math import log
import operator
def calcShannonEnt(dataSet):
    itemCount=len(dataSet)
    labelCount={}
    for featVic in dataSet:
        currentLabel=featVic[-1]
        if currentLabel not in labelCount.keys():
            labelCount[currentLabel]=0
        labelCount[currentLabel]+=1
    shannonEnt=0.0
    for key in labelCount:
        prob=float(labelCount[key])/itemCount
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def createDataSet():
    dataSet=[[1,1,'Yes'],
             [1,1,'Yes'],
             [1,0,'No'],
             [0,1,'No'],
             [0,1,'No']]
    labels=['no surfacing','flippers']
    return dataSet,labels

def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]== value:
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

#根据哪个特征信息熵减少的最多来决定如何划分数据集
def chooseBestFeatureToSplit(dataSet):
    featureCount=len(dataSet[0])-1#获取总特征数，-1 是因为最后一列是数据标签
    baseEntropy=calcShannonEnt(dataSet)#获取最原始的数据信息熵
    baseInfoGain=0.0;bestFeature=-1
    for i in range(featureCount):
        featureList=[example[i] for example in dataSet]
        uniqueVals=set(featureList)#获取该特征的唯一值集合
        newEntropy=0.0
        for value in uniqueVals:
            subDataSet=splitDataSet(dataSet,i,value)#针对该特征的不同值划分整个数据集
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannonEnt(subDataSet)#计算划分后的数据集的熵
        infoGain=baseEntropy-newEntropy
        if(infoGain>baseInfoGain):
            baseInfoGain=infoGain
            bestFeature=i
    return bestFeature

#获取classList列表中出现次数最多的项
def majorityCount(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount:classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.iterable,key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]#获取样本数据集最后一列的所有值（本例中是数据最终的标签）
    if classList.count(classList[0])==len(classList):
        return classList[0]#如果没有不同的标签了 就返回标签值
    if len(dataSet[0])==1:#试用完了所有特征（数据集里面的column都被用掉了）
        return majorityCount(classList)#返回出现次数最多的特征值
    bestFeature=chooseBestFeatureToSplit(dataSet)#找到最能降低信息熵的特征项划分数据集
    bestFeatureLable=labels[bestFeature]#得到特征项的label（其实就是数据集的column header)
    mytree={bestFeatureLable:{}}#为该特征建立一棵树，树的跟节点就是被上一行找到的特征label
    del(labels[bestFeature])#从特征label字典中删除刚刚找到的特征label
    featValues=[example[bestFeature] for example in dataSet]#得到该特征在数据集中的所有值（有重复）
    uniqueVals=set(featValues)#去除重复值，得到用于分割的特征的所有值（无重复）
    for value in uniqueVals:
        subLabels=label[:]
        mytree[bestFeatureLable][value]=createTree(splitDataSet(dataSet,bestFeature,value),subLabels)
        #splitDataSet(dataSet,bestFeature,value) 在已有的数据集上，筛选特征值bestFeature=value的子集，供下一次建立子树使用
    return mytree
        
def classify(input,featLabels,testVec):
    firstStr=list(input.keys())[0]
    secondDict=input[firstStr]
    featIndex=featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex]==key:
            if type(secondDict[key]) is dict:
                classLabel=classify(secondDict[key],featLabels,testVec)
            else:
                classLabel=secondDict[key]
    return classLabel

def storeTree(inputTree,fileName):
    import pickle
    fw=open(fileName,'wb+')
    pickle.dump(input,fw,protocol=pickle.HIGHEST_PROTOCOL)
    fw.close()
def grapTree(fileName):
    import pickle
    fr=open(fileName,'rb+')
    tree= pickle.load(fr)
    return tree;
    

dataSet,label=createDataSet()
shannonEnt=calcShannonEnt(dataSet)
tree=createTree(dataSet,label)
print(tree)
storeTree(tree,'myTree.txt')
myTree=grapTree('myTree.txt')
print(myTree)
myClass=[1,0]
dataSet,label=createDataSet()
print(classify(myTree,label,myClass))