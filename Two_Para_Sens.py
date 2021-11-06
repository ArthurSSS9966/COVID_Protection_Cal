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


#===================== INPUT PARAMETERS ==========================
inputFile = 'ang_dis_vel_600000_part.txt'
inputmesh = 'halfGeometry2.obj'
show3D = True
export3Dmesh = False
filename = ''+str(date.today().isoformat())+'Sensitive_Analysis'
# Column names for the txt file
myIndex = np.array(['x', 'y', 'z','size', 'cone_angle','insertion_dis','velocity'])
# myIndex = np.array(['x', 'y', 'z','size'])
# #===================== END INPUT PARAMETERS ==========================


raw_data = pandas.read_csv(inputFile, delim_whitespace=True, comment='%', header=0)
raw_data = raw_data.fillna(0)
raw_data = raw_data.to_numpy()
Npara = len(myIndex)
NumofSit = int((np.shape(raw_data)[1] - 1)/Npara)
s = (NumofSit,NumofSit)
Percent = np.zeros(s)
tep = raw_data[:,1+Npara*0:Npara*(0+1)+1]
tep2 = raw_data[:,1+Npara*(0+1):Npara*(0+2)+1]
newtep = np.vstack([tep,tep2])
MaxD = pandas.DataFrame(data=newtep, columns=myIndex)
Max = total_area_Data(inputmesh, MaxD, myIndex, False, False)
my_data = np.hstack([tep[0,Npara-3:Npara],tep2[0,Npara-3:Npara], Max])
for n in range (1,NumofSit - 1):
    for k in range(n+1,NumofSit):
        tep = raw_data[:,1+Npara*n:Npara*(n+1)+1]
        tep2 = raw_data[:,1+Npara*(k):Npara*(k+1)+1]
        newtep = np.vstack([tep,tep2])
        tepD = pandas.DataFrame(data=newtep, columns= myIndex)
        Percent = total_area_Data(inputmesh, tepD, myIndex, False, False)
        Para = np.hstack([tep[0,Npara-3:Npara],tep2[0,Npara-3:Npara],Percent])
        if Percent > Max:
            Max = Percent
            MaxD = tepD
            MaxN = np.hstack([tep[0,Npara-3:Npara],tep2[0,Npara-3:Npara]])
        my_data = np.vstack([Para, my_data])
Max = total_area_Data(inputmesh, MaxD, myIndex, show3D, export3Dmesh)
MaxD = MaxD[['cone_angle','insertion_dis','velocity']].head(1)

clean_data = pandas.DataFrame(data=my_data,  columns=['cone_angle','insertion_dis','velocity',
'cone_angle','insertion_dis','velocity','Percent'])
clean_data.to_csv(filename + '.csv')
print(Max, MaxN, MaxD)




