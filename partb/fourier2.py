import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np
import matplotlib.pylab as plt
import time 
from numpy import random
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


fourier = ctypes.CDLL('./fourier3.so')

ft = fourier.dft
fft=fourier.fft

ft.restype = None
ft.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),

                ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                ctypes.c_int]

fft.restype = None
fft.argtypes =[ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_int]

dft_time= []
fft_time= []
fourier_error=[]

N =[16,32,128,256,1024,2048,4096,8192]
Ts = 1/1024
t = np.arange(0,10+Ts,Ts) #(start,stop,step)
x = 1*np.cos(2*np.pi*500*t)
y = 0*np.sin(2*np.pi*3*t)
z = np.column_stack((x, y))
z1 = np.column_stack((x, y))

for i in N :

    before_dft= time.time()
    ft(z,z,i)
    after_dft= time.time()    
    dft_time.append(after_dft-before_dft)
    print ("when N =",i, "dft_time =", dft_time)
    before_fft= time.time()    
    fft(z1,i)
    after_fft= time.time()
    fft_time.append(after_fft-before_fft)
    print("when N =",i, "fft_time =",fft_time)
    mean_error= np.square(np.subtract(z,z1)).mean()
    fourier_error.append(mean_error)

# print (len(N))
# print(len(fft_time))
# print ( len(dft_time))
# print(len(fourier_error))


# plot 1:
plt.subplot(1, 2, 1)
plt.plot(N,dft_time,label="dft time")
plt.plot(N,fft_time,label="fft time")
plt.title("time of dft and fft")
plt.xlabel('size of signal')
plt.ylabel('time of dft and fft')
plt.legend()

#plot 2:

plt.subplot(1, 2, 2)
plt.plot(N,fourier_error)
plt.title("Error between fft and dft")
plt.xlabel('size of signal')
plt.ylabel('error')
plt.legend()

plt.show()