from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import cv2
import numpy as np
from PyQt4 import uic


def numpytoQimage(img):
    height, width, bytesPerComponent = img.shape
    if (width>=700):
    	img=cv2.resize(img,(700,int((height*700)/width)))
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
        self.notebook = QTabWidget()
        self.notebook.tabBar().setTabsClosable(True)
        self.notebook.tabCloseRequested.connect(self.close_handler)
        self.window.setCentralWidget(self.notebook)
        tabApp = QWidget()
        self.notebook.addTab(tabApp,string)
        return tabApp

    def __init__(self):
        myWindow = MyWindowClass(None)
        path=myWindow.path
        myWindow = MyDialogClass(None)
        

        string="canny"
    	path=path.toLocal8Bit().data()
    	img=cv2.imread(path)

        self.window = QMainWindow()

        tabApp=self.createTab(string)
        setImageLabel(tabApp,img)
        self.window.resize(img.shape[1],img.shape[0])
        self.window.show()

    def close_handler(self, index):
        print "close_handler called, index = %s" % index
        self.notebook.removeTab(index)



form_class = uic.loadUiType("fi.ui")[0]                 # Load the UI

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


form_class = uic.loadUiType("load.ui")[0]                 # Load the UI
class MyDialogClass(QDialog, form_class):
	
	
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setupUi(self)
		imageLabel=self.label

		movie=QMovie("loading.gif")
		imageLabel.setMovie(movie)
		movie.start()
		self.show()
		self.exec_()


app = QApplication(sys.argv)
appNew = Application()
app.exec_()