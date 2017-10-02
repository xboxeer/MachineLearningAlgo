from numpy import *
import operator
def CreateDataSet():
    groups=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=(['A','A','B','B'])
    return groups,labels
def Classify(inX,dataSet,label,k):
    dataSetSize=dataSet.shape[0]
    diffMatrix=tile(inX,(dataSetSize,1))-dataSet
    squMatrix=diffMatrix**2
    sumMatrix=squMatrix.sum(axis=1)
    distanceMatrix=sumMatrix**0.5
    sortedDistance=argsort(distanceMatrix)
    classCount={}
    for i in range(k):
        voteILabel=label[sortedDistance[i]]
        classCount[voteILabel]=classCount.get(voteILabel,0)+1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=False)
    return sortedClassCount[0][0]

group,label=CreateDataSet()
result=Classify([3,3],group,label,2)
print(result)
    