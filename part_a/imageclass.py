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


class image_class():
    def __init__(self,path:str):
        self.path=path
        self.image_data= cv.imread(self.path,0).T
        self.size=self.image_data.shape

        self.image_fft = fftpack.fft2(self.image_data) 

        self.magnitude= np.abs(self.image_fft)
        self.phase =  np.angle(self.image_fft)
        self.real = np.real(self.image_fft)
        self.imaginary = 1j*np.imag(self.image_fft)
        
        self.dft = np.fft.fft2(self.image_data)
        self.dft_shift = np.fft.fftshift(self.dft)
        self.magnitude_shift = 20*np.log(np.abs(self.dft_shift))
        self.phase_shift = np.angle(self.dft_shift)
        self.real_shift = 20*np.log(np.real(self.dft_shift))
        self.imaginary_shift = np.imag(self.dft_shift)

        self.uniform_magnitude = np.ones(self.size)
        self.uniform_phase = np.zeros(self.size)

    def mix(self, image2:'image_class', gain1 , gain2 ,mode ):
       
        Modes={'magnitude&phase':[self.magnitude,image2.magnitude,self.phase,image2.phase],\
            'phase&magnitude':[self.phase,image2.phase,self.magnitude,image2.magnitude]\
                ,'real&imaginary':[self.real,image2.real,self.imaginary,image2.imaginary],\
                    'imaginary&real':[self.imaginary,image2.imaginary,self.real,image2.real],\
                        'uniform_magnitude&phase':[self.uniform_magnitude , image2.uniform_magnitude ,self.phase,image2.phase],\
                            'uniform_magnitude&uniform_phase':[self.uniform_magnitude , image2.uniform_magnitude ,self.uniform_phase,image2.uniform_phase],\
                                'magnitude&uniform_phase':[self.magnitude,image2.magnitude,self.uniform_phase,image2.uniform_phase],\
                                    'phase&uniform_magnitude':[self.phase,image2.phase,self.uniform_magnitude, image2.uniform_magnitude]\
                                        ,'uniform_phase&magnitude':[self.uniform_phase,image2.uniform_phase,self.magnitude,image2.magnitude]\
                                            ,'uniform_phase&uniform_magnitude':[self.uniform_phase,image2.uniform_phase,self.uniform_magnitude,image2.uniform_magnitude]}      
        mag_phase_list=['magnitude&phase','uniform_magnitude&phase','uniform_magnitude&uniform_phase','magnitude&uniform_phase']
        phase_mag_list=['phase&magnitude','phase&uniform_magnitude','uniform_phase&magnitude','uniform_phase&uniform_magnitude']
        real_imag_list=['real&imaginary','imaginary&real']
        compined_image = None
        
        if mode in Modes:
            mode_data= Modes.get(mode)
            data_comp1= (gain1*mode_data[0])+((1-gain1)*mode_data[1])
            data_comp2= ((1-gain2)*mode_data[2])+(gain2*mode_data[3])
            if (mode in mag_phase_list ):
                combined = np.multiply(data_comp1, np.exp(1j * data_comp2))
                logger.info("Mixing Magnitude and Phase")
            elif  (mode in real_imag_list):
                combined =  data_comp1 + data_comp2
                logger.info("Mixing Real And Imaginary")
            elif(mode in phase_mag_list):
                combined = np.multiply(data_comp2, np.exp(1j * data_comp1))
                logger.info("Mixing Magnitude and Phase")
            compined_image = np.real(np.fft.ifft2(combined)) 
             
        return(compined_image)
       
   
