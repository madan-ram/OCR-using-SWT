import numpy as np
cimport numpy as np
import cython as cy
from sklearn import cluster
import random
import cv2

cdef class componentDetails:
    cdef:
        double mean
        double variance
        int centerX
        int centerY
        double colorAverageB
        double colorAverageG
        double colorAverageR
    def __cinit__(self,double mean,double variance,int centerX,int centerY,int colorAverageB,int colorAverageG,int colorAverageR):
        self.mean=mean
        self.variance=variance
        self.centerX=centerX
        self.centerY=centerY
        self.colorAverageB=colorAverageB
        self.colorAverageG=colorAverageG
        self.colorAverageR=colorAverageR

cdef class Boundbox:
    cdef:
        int minx,miny,maxx,maxy
    def __cinit__(self,minx,miny,maxx,maxy):
        self.minx=minx
        self.miny=miny
        self.maxx=maxx
        self.maxy=maxy

def getComponentsDetails(np.ndarray image,np.ndarray SWTImage,np.ndarray row_loc,components):
    cdef:
        double mean
        double variance
        int centerX,centerY,row,col
        int width,height,count,minx,miny,maxx,maxy
        double colorAverageB
        double colorAverageG
        double colorAverageR
        int vertex
        np.ndarray componentsDetailsList=np.zeros((len(components),6))
    width=SWTImage.shape[1]
    height=SWTImage.shape[0]
    boundbox=[]

    for i in xrange(len(components)):
        component=components[i]
        mean=0.0
        variance=0.0
        centerX=0
        centerY=0
        colorAverage=0.0
        countNumberPixel=0
        minx=99999
        maxx=-99999
        miny=99999
        maxy=-99999
        for vertex in component:
            row=row_loc[vertex]
            col=int(vertex-row*width)
            if(minx>=col):
                minx=col
            if(miny>=row):
                miny=row
            if(maxx<col):
                maxx=col
            if(maxy<row):
                maxy=row
            #calculating mean
            mean+=SWTImage.item((row,col))
            colorAverageB+=image.item(row,col,0)
            colorAverageG+=image.item(row,col,1)
            colorAverageR+=image.item(row,col,2)

        #dimTuple=((maxy-miny),(maxx-minx))
        boundbox.append((minx,miny,maxx,maxy))
        mean=mean/len(component)
        colorAverageB=colorAverageB/len(component)
        colorAverageG=colorAverageG/len(component)
        colorAverageR=colorAverageR/len(component)
        #calculating variance
        for vertex in component:
            row=row_loc.item(vertex)
            col=vertex-row*width
            variance+=(mean-SWTImage.item((row,col)))*(mean-SWTImage.item((row,col)))
        variance=variance/len(component)

        centerX=(minx+maxx)/2
        centerY=(miny+maxy)/2

        componentsDetailsList[i]=np.array([variance,centerX,centerY,colorAverageB,colorAverageG,colorAverageR])
    dbscan = cluster.DBSCAN(eps=100,min_samples=2)
    X=componentsDetailsList
    predict=dbscan.fit_predict(X)

    boundboxTextLine=[]
    validChar=[0]*len(components)

    prev=0
    b=int(random.random()*255)
    g=int(random.random()*255)
    r=int(random.random()*255)
    newImg=np.copy(image)
    for x in dbscan.core_sample_indices_:
        minx,miny,maxx,maxy=boundbox[x]
        if predict[x]!=prev:
            b=int(random.random()*255)
            g=int(random.random()*255)
            r=int(random.random()*255)
            cv2.rectangle(newImg,(maxx,maxy),(minx,miny),cv2.cv.RGB(r,g,b),thickness=2)
            prev=predict[x]
        else:
            cv2.rectangle(newImg,(maxx,maxy),(minx,miny),cv2.cv.RGB(r,g,b),thickness=2)
    return validChar
    #print dbscan.labels_
    #for i in xrange(len(predict)):
    #    if predict[i]!=-1:
    #    	if predict[i]<len(boundboxTextLine)-1:
    #    		boundboxTextLine.append()