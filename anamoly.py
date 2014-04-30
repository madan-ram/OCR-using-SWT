import numpy as np
import matplotlib.font_manager
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.externals import joblib

X=[]
labels=[]
count=0
f=open("feature.txt")
for x in f.read().split("\n"):
	temp=map(float,x.split())
	labels.append(int(temp[0]))
	count=count+1
	X.append(temp[1:])

trainX=X[:int(len(X)*0.50)]
trainlLabels=labels[:int(len(X)*0.50)]
test=X[int(len(X)*0.50):]
testLabels=labels[int(len(X)*0.50):]

trainX=np.array(trainX)
clf=svm.LinearSVC()
clf.fit(trainX,trainlLabels)
predictLabels=clf.predict(test)
#predictLabels=[]
#for y0,y1 in predictLabels_prob:
#	if y0>=.58:
#		predictLabels.append(0)
#	else:
#		predictLabels.append(1)

#print predictLabels
print(classification_report(testLabels, predictLabels))
joblib.dump(clf, "./model/model.svc")
#
#trainX=np.array(trainX)
#clf=svm.SVC(class_weight={1: 50})
#clf.fit(trainX,trainlLabels)
#predictLabels=clf.predict(test)
#
##print predictLabels
#print(classification_report(testLabels, predictLabels))