# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:56:07 2020
Revised on Nov. 19
This file plots the particle deposition depending on the size of the particles in a loop.
Parameters:
    Details can be found in the INPUT PARAMETERS section

Notes:
    - the particle diameter is specified in mm in the txt file. Here we use microns
    - Figure saved as SVG
    - help on plotting found here https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.bar.html
    - rev 04:
        - title and figure labels are defined in the parameters section
        - axisOfInterest added (more flexible). Values: x is sagittal - y is rostrocaudal - z is height

@author: jmbouteiller

"""
#from numpy import genfromtxt
import pandas
import numpy as np
import matplotlib.pyplot as plt
from Coverage_Functions import total_area_Data
from datetime import date
import tkinter as tk
from tkinter import Tk
import tkinter.filedialog as fd


#===================== INPUT PARAMETERS ==========================
Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
root = tk.Tk()
inputFile = fd.askopenfilenames(parent=root, title='Choose a file')
# inputFile = 'diffuser deposition_para.txt'
inputmesh = 'halfGeometry2.obj'
show3D = False
export3Dmesh = False
filename = ''+str(date.today().isoformat())+inputFile
# Column names for the txt file
# myIndex = np.array(['x', 'y', 'z','size', 'cone_angle','insertion_depth','spray_vel'])
myIndex = np.array(['x', 'y', 'z','size','cone_angle','spray_vel'])
# myIndex = np.array(['x', 'y', 'z','size'])
# #===================== END INPUT PARAMETERS ==========================

raw_data = pandas.read_csv(inputFile, delim_whitespace=True, comment='%', header=0)
raw_data = raw_data.fillna(0)
raw_data = raw_data.to_numpy()
Npara = len(myIndex)
NumofSit = int((np.shape(raw_data)[1] - 1)/Npara)
Percent = np.zeros(NumofSit)
MaxD = pandas.DataFrame(data=raw_data[:,1:Npara+1], columns=myIndex)
Max = total_area_Data(inputmesh, MaxD, myIndex, False, False)
my_data = np.hstack([raw_data[0,Npara-2:Npara+1], Max])
for n in range (1,NumofSit):
    tep = raw_data[:,1+Npara*n:Npara*(n+1)+1]
    tepD = pandas.DataFrame(data=tep, columns= myIndex)
    Percent[n] = total_area_Data(inputmesh, tepD, myIndex, False, False)
    Para = np.hstack([tep[0,Npara-3:Npara],Percent[n]])
    if Percent[n] > Max:
        Max = Percent[n]
        MaxD = tepD
        MaxN = n
    my_data = np.vstack([Para, my_data])
Max = total_area_Data(inputmesh, MaxD, myIndex, show3D, export3Dmesh)
MaxD = MaxD[['cone_angle','inhale_speed']].head(1)

clean_data = pandas.DataFrame(data=my_data,  columns=['cone_angle','inhale_speed','Percent'])
clean_data.to_csv(filename + '.csv')
print(Max, MaxN, MaxD)




