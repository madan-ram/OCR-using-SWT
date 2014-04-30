import TextDetection as text
import cv2
import matplotlib.pyplot as plt
import time
import numpy as np 
import sys, getopt
import os

def connected_Boxing(SWTImage,row_loc,components):
	varianceList=[]
	meanList=[]
	boundbox=[]
	countList=[]
	dimList=[]
	width=SWTImage.shape[1]
	for component in components:
		mean=0.0
		variance=0.0
		count=0
		minx=99999
		maxx=-99999
		miny=99999
		maxy=-99999
		#calculating mean
		for v in component:
			row=int(row_loc.item(v))
			col=int(v-row*width)
			if(minx>col):
				minx=col
			if(miny>row):
				miny=row
			if(maxx<col):
				maxx=col
			if(maxy<row):
				maxy=row
			mean+=SWTImage.item((row,col))
			count=count+1
		dimList.append([(maxy-miny),(maxx-minx)])
		boundbox.append([minx,miny,maxx,maxy])
		mean=mean/count
		#calculating variance
		for v in component:
			row=row_loc.item(v)
			col=v-row*width
			variance+=(mean-SWTImage.item((row,col)))*(mean-SWTImage.item((row,col)))
		variance=variance/count
		countList.append(count)
		varianceList.append(variance)
		meanList.append(mean)
	return boundbox,meanList,varianceList,countList,dimList

def startFeatch(directory):
	f=open("feature.txt","a")
	swt=text.SWT()
	for file in next(os.walk(directory))[2]:
		if file[-4:] in [".PNG",".png",".jpg",".JPG"]:
			print directory+"/"+file
			image=cv2.imread(directory+"/"+file)
			if (image.shape[0]>=800 and image.shape[1]>=800):
				image=cv2.resize(image,(int(image.shape[0]*0.75),int(image.shape[1]*0.75)))
				print "resize done"
			Fstart=time.time()

			for i in [True,False]:
				start=time.time()
				print "please wait"
				SWTImage,rays=swt.getSWT(image,i,optimizeSpeed=False,medianFilterEnable=False)
				end=time.time()
				res=(end-start)
				#print res
				
				start=time.time()
				components,row_loc=swt.connected_components(SWTImage)
				end=time.time()
				res=(end-start)
				#print res

				start=time.time()
				boundbox,meanList,varianceList,countList,dimList=connected_Boxing(SWTImage,row_loc,components)
				end=time.time()
				res=(end-start)
				#print res

				Fend=time.time()
				res=(Fend-Fstart)
				#print res

				count=0
				countZeros=0
				width=image.shape[1]
				newImage=image.copy()
				for i in xrange(len(components)):
					image=newImage.copy()
					minx,miny,maxx,maxy=boundbox[count]
					print meanList[count],varianceList[count],countList[count],dimList[count][0],dimList[count][1]
					cv2.rectangle(image,(maxx,maxy),(minx,miny),cv2.cv.RGB(255,0,0),thickness=5)
					image=cv2.resize(image,(500,500))
					cv2.imshow("figure",image)
					cv2.waitKey(13)
					label=input()
					if label==0:
						countZeros+=1
					else:
						countZeros=0
					print >>f,label,meanList[count],varianceList[count],countList[count],dimList[count][0],dimList[count][1]
					count=count+1
					if countZeros==10:
						break

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
