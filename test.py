import TextDetection as text
import cv2
import matplotlib.pyplot as plt
import time
import numpy as np 
#import Algorithm as algo
import random
import cProfile,pstats
import pysam
from guppy import hpy
h = hpy()
h.setref()

image=cv2.imread("1.jpg")
height,width,nchannel=image.shape
if height>=800 and width>=800:
	image=cv2.resize(image,(800,int((height*800)/width)))
swt=text.SWT()
Fstart=time.time()
start=time.time()
#SWTImage,rays=swt.getSWT(image,True,optimizeSpeed=False,medianFilterEnable=False)

cProfile.runctx("swt.getSWT(image,True,optimizeSpeed=False,medianFilterEnable=False)", globals(), locals(), "Profile.prof")
print h.heap()
s = pstats.Stats("Profile.prof")
print s.strip_dirs().sort_stats("time").print_stats()
end=time.time()
res=(end-start)
print res

#start=time.time()
#components,row_loc=swt.connected_components(SWTImage)
#end=time.time()
#res=(end-start)
#print res
#Fend=time.time()
#res=(Fend-Fstart)
#print res
#
#start=time.time()
#boundbox,validChar=swt.connected_Filter(SWTImage,row_loc,components)
#end=time.time()
#res=(end-start)
#print res
#
#Fend=time.time()
#res=(Fend-Fstart)
#print res

#width=image.shape[1]
#componentImage=np.zeros((SWTImage.shape[0],SWTImage.shape[1],3))
#for component in components:
#	g=int(random.random()*255)
#	b=int(random.random()*255)
#	r=int(random.random()*255)
#	for v in component:
#		row=row_loc[v]
#		col=v-row*width
#		#print row,col,row_loc.item(v),v
#		componentImage.itemset((row,col,0),g)
#		componentImage.itemset((row,col,1),b)
#		componentImage.itemset((row,col,2),r)
#
#componentImage=np.uint8(componentImage)
#plt.imshow(componentImage)
#cv2.imshow("d",SWTImage)
##cv2.waitKey(0)
#plt.show()

#count=0
#width=image.shape[1]
#for i in xrange(len(components)):
#	if validChar[count]==1:
#		g=255
#		b=0
#		r=0
#	else:
#		g=0
#		b=0
#		r=255
#	minx,miny,maxx,maxy=boundbox[count]
#	cv2.rectangle(image,(maxx,maxy),(minx,miny),cv2.cv.RGB(r,g,b),thickness=2)
#	count=count+1
#	
#plt.imshow(image)
#plt.show()