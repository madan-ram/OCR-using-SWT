from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import cv2
import numpy as np
from PyQt4 import uic
from threading import Thread
from time import sleep
import os
from PyQt4.QtCore import SIGNAL, QObject
import TextDetection as text
import time
#import Algorithm as algo
import tesseract
import random
import groupingLetter as grl

def numpytoQimage(img,sizeWidth=1000):

    if len(img.shape)==2:
        img=np.uint8(img)
        img=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    height, width, bytesPerComponent = img.shape
    if (width>=sizeWidth):
        img=cv2.resize(img,(sizeWidth,int((height*sizeWidth)/width)))
    height, width, bytesPerComponent = img.shape
    bytesPerLine = bytesPerComponent * width
    img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    image = QImage(img.data,width,height,bytesPerLine,QImage.Format_RGB888)
    return image

def setImageLabel(widget,img):
    imageLabel=QLabel(widget)
    img=numpytoQimage(img)
    imageLabel.setPixmap(QPixmap.fromImage(img))
    return imageLabel

class MultiWindows(QMainWindow):

    def __init__(self, param):
        self.__windows = []

    def addwindow(self, window):
        self.__windows.append(window)

    def show():
        for current_child_window in self.__windows:
             current_child_window.exec_() # probably show will do the same trick

class Application():
    window=None
    notebook=None

    def createTab(self,string):
        self.notebook.tabBar().setTabsClosable(True)
        self.notebook.tabCloseRequested.connect(self.close_handler)
        self.window.setCentralWidget(self.notebook)
        tabApp = QWidget()
        self.notebook.addTab(tabApp,string)
        return tabApp

    def __init__(self):
        myWindow = MyWindowClass(None)
        path=myWindow.path
        self.notebook = QTabWidget()
        self.window = QMainWindow()
        #myWindow = MyDialogClass(None)
        #myWindow.start()
        path=path.toLocal8Bit().data()
        img=cv2.imread(path)
        height,width,nchannel=img.shape
        setHeigth=1000
        if height>=setHeigth and width>=setHeigth:
            img=cv2.resize(img,(setHeigth,int((height*setHeigth)/width)))
        tabApp=self.createTab("original image")
        setImageLabel(tabApp,img)
        for t in [False,True]:
            swt=text.SWT()
            Fstart=time.time()
            start=time.time()
            SWTImage,rays=swt.getSWT(img,t,optimizeSpeed=True)

            end=time.time()
            res=(end-start)
            #print res

            start=time.time()
            components,row_loc=swt.connected_components(SWTImage)
            end=time.time()
            res=(end-start)
            #print res
            SWTImage=np.uint8(SWTImage)
            SWTImageNew=cv2.cvtColor(SWTImage,cv2.COLOR_GRAY2BGR)
            tabApp=self.createTab("stroke width transform")
            setImageLabel(tabApp,SWTImageNew)

            Fend=time.time()
            res=(Fend-Fstart)
            #print res

            start=time.time()
            boundbox,validChar=swt.connected_Filter(SWTImage,row_loc,components)
            swt.boundboxFilter(boundbox)
            end=time.time()
            res=(end-start)
            #print res

            Fend=time.time()
            res=(Fend-Fstart)
            print res
            #imgNew=img.copy()
            width=img.shape[1]
            componentImage=np.zeros((SWTImage.shape[0],SWTImage.shape[1],3))
            for component in components:
                g=int(random.random()*255)
                b=int(random.random()*255)
                r=int(random.random()*255)
                for v in component:
                    row=row_loc[v]
                    col=v-row*width
                    #print row,col,row_loc.item(v),v
                    componentImage.itemset((row,col,0),g)
                    componentImage.itemset((row,col,1),b)
                    componentImage.itemset((row,col,2),r)

            #componentImage=np.uint8(componentImage)
            #if True==t:
            #	imgNew=255-imgNew
            imgNew=np.zeros((SWTImage.shape[0],SWTImage.shape[1]),dtype="uint8")
            imgNew[SWTImage<=0]=255

            api = tesseract.TessBaseAPI()
            api.Init(".","eng",tesseract.OEM_DEFAULT)
            api.SetPageSegMode(tesseract.PSM_AUTO)
            #as suggested by zdenko podobny <zdenop@gmail.com>,
            #using PSM_SINGLE_BLOCK will be more reliable for ocr-ing a line of word.
            #api.SetPageSegMode(tesseract.PSM_SINGLE_BLOCK)
            #image1=cv2.cvtColor(imgNew,cv2.COLOR_BGR2GRAY)
            image = numpytoQimage(imgNew)
            tesseract.SetCvImage(image,api)
            textData=api.GetUTF8Text()
            conf=api.MeanTextConf()
            image=None
            print "..............."
            print "Ocred Text: %s"%textData
            print "Cofidence Level: %d %%"%conf

            #print componentImage.dtype
            #cv2.imshow("win",componentImage)
            #cv2.waitKey(0)
            tabApp=self.createTab("connected component")
            setImageLabel(tabApp,imgNew)
            
            #validChar=grl.getComponentsDetails(img,SWTImage,row_loc,components)

            count=0
            width=img.shape[1]
            imgNew=img.copy()
            for i in xrange(len(components)):
                if validChar[count]==1:
                    g=255
                    b=0
                    r=0
                elif validChar[count]==0:
                    g=0
                    b=0
                    r=255
                else:
                    g=0
                    b=255
                    r=0
                minx,miny,maxx,maxy=boundbox[count]
                cv2.rectangle(imgNew,(maxx,maxy),(minx,miny),cv2.cv.RGB(r,g,b),thickness=2)
                count=count+1
            imgNew=np.uint8(imgNew)
            tabApp=self.createTab("boundedbox")
            setImageLabel(tabApp,imgNew)

        self.window.resize(img.shape[1],img.shape[0])
        self.window.show()

    def close_handler(self, index):
        print "close_handler called, index = %s" % index
        self.notebook.removeTab(index)



form_class = uic.loadUiType("ui/fi.ui")[0]
class MyWindowClass(QDialog, form_class):

    path=None
    def selectFile(self):
        self.lineEdit.setText(QFileDialog.getOpenFileName())


    def ok(self):
        self.path=self.lineEdit.displayText()
        self.close()
        #QCoreApplication.instance().setActiveWindow(appNew.window)
        #QCoreApplication.instance().quit

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.selectFile)
        self.okpushButton.clicked.connect(self.ok)
        self.cancelpushButton.clicked.connect(QCoreApplication.instance().quit)
        self.show()
        self.exec_()


class myClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        a = [1,2,3,4,5,6,67,78]
        for i in a:
            print i
            sleep(1)


form_class = uic.loadUiType("ui/load.ui")[0]
class MyDialogClass(QThread):
    dialog=None
    form=None
    def run(self):
        for i in xrange(10):
            print i
            sleep(1)

    def __init__(self, parent=None):
        QThread.__init__(self)
        self.dialog=QMainWindow(parent)
        self.form=form_class()
        self.form.setupUi(self.dialog)
        imageLabel=self.form.label
        movie=QMovie("loading.gif")
        imageLabel.setMovie(movie)
        movie.start()
        self.dialog.show()
        #self.dialog.exec_()


app = QApplication(sys.argv)
appNew = Application()
app.exec_()
