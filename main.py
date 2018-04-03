import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
        QPushButton, QToolTip,QMessageBox,QHBoxLayout,QVBoxLayout,QLabel)
from PyQt5.QtGui import QIcon,QFont,QPixmap,QPainter,QImage
from PyQt5.QtCore import QCoreApplication,QRect
from PIL import Image,ImageDraw
import numpy as np
import math

class Example(QWidget):
    OrinX = 30
    OrinY = 30
    OrinX2 = 560
    OrinY2 = 30
    PHEIGHT = 400
    PWIDTH = 500 
    MyColor = (0,255,0)
    MatrixIn = []
    MatrixOut = []
    ListIn =[]
    ListOut = []
    flag = 1

    def __init__(self):
        super(Example,self).__init__()
        
        self.initUI()


    def initUI(self):
 
        QToolTip.setFont(QFont('SansSerif',10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        self.MatrixIn = np.full((self.PHEIGHT,self.PWIDTH),255,dtype = 'int32')
        self.MatrixOut = np.full((self.PHEIGHT,self.PWIDTH),255,dtype = 'int32')

        Img = Image.open("test.jpg")
        Img = Img.resize((self.PWIDTH,self.PHEIGHT))
        Img.save("res0.jpg")
        Img.save("res.jpg")

        btn = QPushButton('选中物体', self)
        btn.setToolTip('请点击 <b>物体内</b> 点')
        btn.clicked.connect(self.chooseColorG)
        btn.move(50, 500)

        btn2 = QPushButton('选中背景', self)
        btn2.setToolTip('请点击 <b>背景中</b> 点')
        btn2.clicked.connect(self.chooseColorR)
        btn2.move(200, 500)

       # lbl.move(20,20)
        
        self.setGeometry(300, 300, 1100, 600)
        self.setWindowTitle('Deep Interactive Object Selection in the Video Flow')
        self.setWindowIcon(QIcon('icon.ico'))    

        self.show()

    def chooseColorR(self,event):
        self.MyColor = (255,0,0)
        self.flag = 0
    def chooseColorG(self,event):
        self.MyColor = (0,255,0)   
        self.flag = 1

    def paintEvent(self,event):
        painter = QPainter()
        img = QImage("res0.jpg")
        pix = QPixmap.fromImage(img)

        imgres = QImage("res.jpg")
        #print imgres.size()
        pixres = QPixmap.fromImage(imgres)

        painter.begin(self)
        painter.drawPixmap(QRect(self.OrinX,self.OrinY,self.PWIDTH,self.PHEIGHT),
                        pix
                        #,QRect(0,0,self.PWIDTH,self.PHEIGHT)
                        )
        painter.drawPixmap(QRect(self.OrinX2,self.OrinY2,self.PWIDTH,self.PHEIGHT),
                        pixres
                        #,QRect(0,0,self.PWIDTH,self.PHEIGHT)
                        )
        painter.end()

    def mousePressEvent(self,event):

        #print self.OrinX  
        xx = event.x()-self.OrinX
        yy = event.y()-self.OrinY
        print xx,yy
        
        resImage = Image.open("res.jpg")
        draw = ImageDraw.Draw(resImage)
        draw.ellipse((xx,yy,xx+20,yy+20),fill =self.MyColor)
        resImage.save("res.jpg")

        if self.flag == 1:
            self.ListIn.append([xx,yy])
            for i in range(self.PHEIGHT):
                for j in range(self.PWIDTH):     
                    dis = math.sqrt((i-yy)**2+(j-xx)**2)
                    if dis<self.MatrixIn[i,j]:
                        self.MatrixIn[i,j] = dis
            im = Image.fromarray(self.MatrixIn)
            im = im.convert("L") 
            im.save("in.bmp")
        else:
            self.ListOut.append([xx,yy])
            for i in range(self.PHEIGHT):
                for j in range(self.PWIDTH):     
                    dis = math.sqrt((i-yy)**2+(j-xx)**2)
                    if dis<self.MatrixOut[i,j]:
                        self.MatrixOut[i,j] = dis
            im2 = Image.fromarray(self.MatrixOut)
            im2 = im2.convert("L") 
            im2.save("out.bmp")
        self.update()



    def buttonClicked(self):
        pass

    def closeEvent(self,event):

        reply = QMessageBox.question(self, 'Message',"Are you sure to quit？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()




if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())   