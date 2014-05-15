import TextDetection as text
import cv2
import matplotlib.pyplot as plt
import time
import numpy as np
import sys, getopt
import random
import os

def startFeatch(directory):
    f=open("feature.txt","a")
    swt=text.SWT()
    for file in next(os.walk(directory))[2]:
        if file[-4:] in [".PNG",".png",".jpg",".JPG"]:
            print directory+"/"+file
            image=cv2.imread(directory+"/"+file)
            os.remove(directory+"/"+file)
            height,width,_=image.shape
            if (width>=1000):
                image=cv2.resize(image,(1000,int((height*1000)/width)))
                print "resize done"
            Fstart=time.time()

            for t in [True,False]:
                start=time.time()
                print "please wait"
                SWTImage,rays=swt.getSWT(image,t,optimizeSpeed=True,medianFilterEnable=False)
                end=time.time()
                res=(end-start)
                print res

                start=time.time()
                components,row_loc=swt.connected_components(SWTImage)
                end=time.time()
                res=(end-start)
                print res

                start=time.time()
                count=0
                countZeros=0
                width=image.shape[1]
                boundbox,validChar=swt.connected_Filter(SWTImage,row_loc,components)

                componentImage=np.zeros(image.shape,dtype="uint8")
                componentImage.fill(255)
                for component in components:
                    g=int(random.random()*255)
                    b=int(random.random()*255)
                    r=int(random.random()*255)
                    for v in component:
                        row=row_loc[v]
                        col=v-row*width
                        componentImage.itemset((row,col,0),g)
                        componentImage.itemset((row,col,1),b)
                        componentImage.itemset((row,col,2),r)


                #cv2.imshow("display",componentImage)
                #cv2.waitKey(0)

                #swt.slidingWindowFull(componentImage,boundbox,validChar,size=(20,20))

                #newImage=image.copy()
                #if t==True:
                #    newImage=255-newImage
                newImage=np.zeros(SWTImage.shape)
                newImage[SWTImage==0]=255
                #newImage[SWTImage>0]=0
                #swt.slidingWindowFull(newImage,boundbox,validChar,size=(32,20))
                #cv2.imshow("display",newImage)
                #cv2.waitKey(2000)
                cv2.imwrite(directory+"/"+str(int(random.random()*100))+".png",newImage)
                end=time.time()
                res=(end-start)
                #print res

                Fend=time.time()
                res=(Fend-Fstart)
                #print res

try:
    opts, args = getopt.getopt(sys.argv[1:],"hd")
except getopt.GetoptError:
    print 'test.py -d <directory path of images>'
    sys.exit(2)
for opt, arg in opts:
    if opt=="-h":
        print 'test.py -d <directory path of images>'
    elif opt=="-d":
        if args!=[]:
            PATH=args[0]
            if os.path.isdir(PATH) and os.access(PATH, os.R_OK):
                startFeatch(PATH)
            else:
                print "directory does not exist"
        else:
            print "please input the <directory path of images>"
