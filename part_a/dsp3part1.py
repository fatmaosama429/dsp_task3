from PyQt5 import QtWidgets, QtCore, uic, QtGui, QtPrintSupport
from PyQt5.QtWidgets import QMessageBox  
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *   
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import path
import numpy as np
import sys
import os
import math
from pyqtgraph import ImageView
from cv2 import cv2
import cv2 as cv
import numpy as np
import sys
import os
import qdarkgraystyle
import logging
#from imageModel import ImageModel   #lsa maga4

MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"main.ui"))

class MainApp(QtWidgets.QMainWindow,MAIN_WINDOW):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        self.msg = QMessageBox() 

# list of everything
        self.images=[None,None]
        self.image_models=[None,None]
        self.img_views=[self.imageView,self.imageView_2,self.imageView_1_edit,self.imageView_2_edit,self.output_1,self.output_2]
        self.combos=[self.comboBox,self.comboBox_2,self.comboBox_3,self.comboBox_4,self.comboBox_5,self.comboBox_6,self.comboBox_7]
# hide
        for i in range(len(self.img_views)):
            self.img_views[i].ui.histogram.hide()
            self.img_views[i].ui.roiBtn.hide()
            self.img_views[i].ui.menuBtn.hide()
            self.img_views[i].ui.roiPlot.hide()

        self.connect_func()

    def connect_func(self):
        self.actionImage1.triggered.connect(lambda: self.browse(0))
        self.actionImage2.triggered.connect(lambda: self.browse(1))

        self.comboBox.currentTextChanged.connect(lambda: self.img_components(0))
        self.comboBox_2.currentTextChanged.connect(lambda: self.img_components(1))

    def browse(self,idx):
        self.file,_ = QtGui.QFileDialog.getOpenFileName(self, 'choose the image', os.getenv('HOME') ,"Images (*.png *.xpm *.jpg)" )
        if self.file == "":
            pass
        #error when upload img1 before img2
        #set the second argument in imread is flages = 0 to draw in grayscale
        if idx == 0:
            image = self.images[idx] = cv.imread(self.file,0).T
            self.current_size = image.shape[:2]
            # self.image_models[idx]=ImageModel(self.file)
            self.draw_img(idx,image)

        elif idx == 1:
            image = self.images[idx] = cv.imread(self.file,0).T
            if image.shape[:2] != self.current_size:
                self.msg.setWindowTitle("Error in Image Size")
                self.msg.setText("The images must have the same size")
                self.msg.setIcon(QMessageBox.Warning)
                x = self.msg.exec_()
                return
            else:
                # self.image_models[idx]=ImageModel(self.file)
                self.draw_img(idx,image)

    def draw_img(self,idx,image):
        self.img_views[idx].setImage(image)


    def img_components(self,idx):
        self.dft = np.fft.fft2(self.images[idx])
        self.dft_shift = np.fft.fftshift(self.dft)
        self.magnitude_shift = 20*np.log(np.abs(self.dft_shift))
        self.phase_shift = np.angle(self.dft_shift)
        self.real_shift = 20*np.log(np.real(self.dft_shift))
        self.imaginary_shift = np.imag(self.dft_shift)
        
        self.check_combo(idx)

    def check_combo(self,idx):
        selected_combo = self.combos[idx].currentText()
        if selected_combo == "FT Magnitude":
            self.draw_img(idx+2,self.magnitude_shift)
        elif selected_combo == "FT Phase":
            self.draw_img(idx+2,self.phase_shift)
        elif selected_combo == "FT Real Component":
            self.draw_img(idx+2,self.real_shift)
        elif selected_combo == "FT Imaginary Component":
            self.draw_img(idx+2,self.imaginary_shift)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
