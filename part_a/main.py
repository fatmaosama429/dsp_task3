from imageclass import image_class 
from PyQt5 import QtWidgets, QtCore, uic, QtGui, QtPrintSupport
from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg
from pyqtgraph import ImageView
from pyqtgraph import PlotWidget, plot
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *   
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QApplication, QMainWindow,QVBoxLayout,QAction,QFileDialog, QPushButton, QLabel, QCheckBox
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
import matplotlib 
import logging 
import os
from os import path
from os.path import dirname, realpath,join
import math
from cv2 import cv2
import cv2 as cv
import qdarkgraystyle

logging.basicConfig(filename="logging.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

logger=logging.getLogger() 
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 


scriptDir=dirname(realpath(__file__))
From_Main,_= loadUiType(join(dirname(__file__),"main.ui"))


class MainApp(QtWidgets.QMainWindow,From_Main):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        self.msg = QMessageBox() 
        self.mode="real&imaginary"
        self.gain1=1
        self.gain2=1

        logger.info("the window opened successfully")

         # list of everything
        self.images=[None,None]
        self.modes=["real&imaginary","imaginary&real","magnitude&uniform_phase","magnitude&phase",\
            "uniform_magnitude&phase", "uniform_magnitude&uniform_phase", "phase&magnitude", \
                "phase&uniform_magnitude","uniform_phase&magnitude","uniform_phase&uniform_magnitude"]
        self.img_views=[self.imageView,self.imageView_2,self.imageView_1_edit,self.imageView_2_edit,self.output_1,self.output_2]
        self.combos=[self.image1_FT_component,self.image2_FT_component,self.mixer_viewer,\
            self.mixer_image1,self.mixer_image2,self.mixer_comp1,self.mixer_comp2]
         # hide
        for i in range(len(self.img_views)):
            self.img_views[i].ui.histogram.hide()
            self.img_views[i].ui.roiBtn.hide()
            self.img_views[i].ui.menuBtn.hide()
            self.img_views[i].ui.roiPlot.hide()
        logger.info("all viewers are hiden")
        self.connect_func()

    def connect_func(self):
        self.mixer_comp1.setCurrentText("Real")
        self.mixer_comp2.setCurrentText("Imaginary")
        self.actionNew_Window.triggered.connect(self.newwindow)
        
        self.actionImage1.triggered.connect(lambda: self.browse(0))
        self.actionImage2.triggered.connect(lambda: self.browse(1))
        logger.info("open buttons are connected to the function browse successfully")

        self.image1_FT_component.currentTextChanged.connect(lambda: self.choose_FT(0))
        self.image2_FT_component.currentTextChanged.connect(lambda: self.choose_FT(1))
        logger.info("combobox for choosing ft components are connected to the functions choose_ft successfully")
        
        self.mixer_viewer.currentTextChanged.connect(lambda: self.mixer())
        logger.info("mixer viewer combobox connected with mixer function successfully")

        
        self.mixer_comp1.currentTextChanged.connect(lambda: self.update_mode())
        self.mixer_comp2.currentTextChanged.connect(lambda: self.update_mode())
        

        logger.info("combobox for choosing ft components for mixer are connected to the function update mode")

        self.mixer_image1.currentTextChanged.connect(lambda: self.mixer())
        self.mixer_image2.currentTextChanged.connect(lambda: self.mixer())
        logger.info("comboboxes for choosing images in mixer are connected to their functions successfully")

        self.FT_slider_1.valueChanged.connect(lambda:self.sliderupdate())
        self.FT_slider_2.valueChanged.connect(lambda:self.sliderupdate())

        logger.info("sliders are connected to their functions successfully")
    
    def browse(self,id):
        self.file,_ = QtGui.QFileDialog.getOpenFileName(self, 'choose the image', os.getenv('HOME') ,"Images (*.png *.xpm *.jpg)" )    
        if self.file == "":
            logger.info("no file has been chosen to be open")
            pass
        #error when upload img1 before img2
        #set the second argument in imread is flages = 0 to draw in grayscale
        if id == 0:
            self.images[id] = image_class(self.file)
            self.current_size= np.array(self.images[id].image_data).shape[:2]
            logger.info("the file opend successfully the path is"+ self.file)
            self.draw_img(id,self.images[id].image_data)
            # self.choose_FT(0)
        elif id == 1:
            self.images[id] = image_class(self.file)
            # self.choose_FT(1)
            if  np.array(self.images[id].image_data).shape[:2] != self.current_size:
                self.msg.setWindowTitle("Error in Image Size")
                self.msg.setText("The images must have the same size")
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()
                return
            else:
                # self.image_models[idx]=ImageModel(self.file)
                logger.info("the file opend successfully the path is"+ self.file)
                self.draw_img(id,self.images[id].image_data)
        logger.info("the image is shown in the image viewer")

    def draw_img(self,id,image):
        logger.info("image viewer no. "+str(id)+" is chosen to show the image")
        self.img_views[id].setImage(image)
        logger.info("image uploaded successfuly")
        
    def choose_FT(self,id):
        selected_combo = self.combos[id].currentText()
        if selected_combo == "FT Magnitude":
            self.draw_img(id+2,self.images[id].magnitude_shift)
        elif selected_combo == "FT Phase":
            self.draw_img(id+2,self.images[id].phase_shift)
        elif selected_combo == "FT Real Component":
            self.draw_img(id+2,self.images[id].real_shift)
        elif selected_combo == "FT Imaginary Component":
            self.draw_img(id+2,self.images[id].imaginary_shift)
        logger.info(selected_combo +"component have chosen to be showed in image viewer")

    def sliderupdate(self):
        self.gain1= self.FT_slider_1.value() / 100.0
        self.gain2 = self.FT_slider_2.value() / 100.0
        self.label_8.setText(str(self.gain1))
        self.label_9.setText(str(self.gain2))
        logger.info("FT_slider1 value changed to"+str(self.gain1))
        logger.info("FT_slider2 value changed to"+str(self.gain2))
        self.mixer()
  
    def update_mode(self): 
        selected_combo = self.combos[5].currentText()
        selected_combo1 = self.combos[6].currentText()

        if selected_combo == "Real" and selected_combo1 =="Imaginary" :
            logger.info("mode changed from "+ self.mode +" to real&imaginary")
            self.mode = "real&imaginary"
        elif selected_combo == "Imaginary" and selected_combo1 == "Real"  :
            logger.info("mode changed from "+ self.mode +" to imaginary&real")
            self.mode = "imaginary&real"
        
        elif selected_combo == "Magnitude" and selected_combo1 =="Phase"  : 
            logger.info("mode changed from "+ self.mode +" to magnitude&phase")
            self.mode = "magnitude&phase"  
        elif selected_combo == "Magnitude" and selected_combo1 =="Uniform Phase"  : 
            logger.info("mode changed from "+ self.mode +" to magnitude&uniform_phase")
            self.mode = "magnitude&uniform_phase"

        elif selected_combo == "Uniform Magnitude" and selected_combo1 =="Phase"  : 
            logger.info("mode changed from "+ self.mode +" to uniform_magnitude&phase")
            self.mode = "uniform_magnitude&phase"  
        elif selected_combo == "Uniform Magnitude" and selected_combo1 =="Uniform Phase"  : 
            logger.info("mode changed from "+ self.mode +" to uniform_magnitude&uniform_phase")
            self.mode = "uniform_magnitude&uniform_phase"

        elif selected_combo == "Phase" and selected_combo1 =="Magnitude"  : 
            logger.info("mode changed from "+ self.mode +" to phase&magnitude")
            self.mode = "phase&magnitude"  
        elif selected_combo == "Phase" and selected_combo1 =="Uniform Magnitude"  : 
            logger.info("mode changed from "+ self.mode +" to phase&uniform_magnitude")
            self.mode = "phase&uniform_magnitude"

        elif selected_combo == "Uniform Phase" and selected_combo1 =="Magnitude"  : 
            logger.info("mode changed from "+ self.mode +" to uniform_phase&magnitude")
            self.mode = "uniform_phase&magnitude"  
        elif selected_combo == "Uniform Phase" and selected_combo1 =="Uniform Magnitude"  : 
            logger.info("mode changed from "+ self.mode +" to uniform_phase&uniform_magnitude")
            self.mode = "uniform_phase&uniform_magnitude"
        else : self.mode="None"
        logger.info("the mode chosen is "+str(self.mode))
        self.mixer()
            
    def mixer (self): 
        logger.info("the mode used in mixing the images is "+str(self.mode)+" for component "\
            +str(self.mixer_comp1.currentText()) +" for " + str(self.mixer_image1.currentText())+\
                 " and component "+str(self.mixer_comp2.currentText())+" for "+str(self.mixer_image2.currentText()) )
        print(self.mode)
        if self.mode in self.modes:
            self.imag1=self.images[self.mixer_image1.currentIndex()]
            self.imag2=self.images[self.mixer_image2.currentIndex()]
            data=self.imag1.mix(self.imag2,self.gain1,self.gain2,self.mode)
            self.draw_img(self.mixer_viewer.currentIndex()+4,data)
            logger.info("the mixer worked successfully")
        else: 
            logger.info("the mixer did not work please choose the components properly")    
            self.msg.setWindowTitle("Error")
            self.msg.setText("error: please choose the component properly")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()
        
    def newwindow(self):
        new= MainApp()
        new.show()
        new.setWindowTitle("Mixer")
        
    
      
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
