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
from Coverage_Functions import filter_Spray
from Coverage_Functions import total_area_filterData
from datetime import date
import tkinter as tk
from tkinter import Tk
import tkinter.filedialog as fd


#===================== INPUT PARAMETERS ==========================
Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
root = tk.Tk()
sprayFile = fd.askopenfilenames(parent=root, title='Choose a file')
inputFile = 'ang_dis_vel_1200000_part_viral_wide.txt'
# sprayFile = 'diffuser deposition_para.txt'
inputmesh = 'halfGeometry2.obj'
show3D = False
export3Dmesh = False
filename = ''+str(date.today().isoformat())+inputFile
# Column names for the txt file
SprayIndex = np.array(['x', 'y', 'z','size', 'cone_angle','air_vel','spray_vel'])
# myIndex = np.array(['x', 'y', 'z','size','inhale_speed'])
myIndex = np.array(['x', 'y', 'z','size'])
swabpercent = 1 #Coverage Percentage of using Swab 1 being 100%
swabpos = 1/3 # Swab coverage location in y axis, fraction of anterior coverage
Numsitcom = 7 #Number of situation to compare
Numofcol = 6
fileName = ''+str(date.today().isoformat())+'_protection_rate_along_y_axis'+'_for_'+'swab_spray_and_mask'
# #===================== END INPUT PARAMETERS ==========================

raw_data = pandas.read_csv(inputFile, delim_whitespace=True, comment='%', header=0)
raw_data = raw_data.dropna()
raw_data = raw_data.to_numpy()
spray_data = pandas.read_csv(sprayFile, delim_whitespace=True, comment='%', header=0)
spray_data = spray_data.dropna()
spray_data = spray_data.to_numpy()

Npara = len(myIndex)
Npara2 = len(SprayIndex)

MaxD = pandas.DataFrame(data=raw_data[:,1:Npara+1], columns=myIndex)
Spray = pandas.DataFrame(data = spray_data[:,1:Npara+1], columns = myIndex)

SpID = filter_Spray(inputmesh,Spray)

sortdata = MaxD.sort_values(['size'])
len = np.linspace(min(sortdata['y']),max(sortdata['y']),Numofcol+1)
coveragelen = min(sortdata['y']) + (max(sortdata['y']) - min(sortdata['y']))*swabpos
NumofSit = int((np.shape(raw_data)[1] - 1)/Npara)
sortdata['size'] = (sortdata['size'] * 1000).astype(int)
size = np.array(sortdata['size'].unique())
sizenum = size.shape[0]
Numofsize = len.shape[0] - 1

##No Mask Analysis

depos = np.zeros(Numofsize)

for i in range(0,Numofsize):
    tepdata = sortdata.loc[sortdata['y'] > len[i]]
    tepdata = tepdata.loc[tepdata['y'] < len[i+1]]
    depos[i] = total_area_Data(inputmesh, tepdata,myIndex, False, False)

#Spray Analysis

deposspray = np.zeros(Numofsize)

for i in range(0,Numofsize):
    tepdata = sortdata.loc[sortdata['y'] > len[i]]
    tepdata = tepdata.loc[tepdata['y'] < len[i+1]]
    deposspray[i] = total_area_filterData(inputmesh, SpID,tepdata, False, False)

##Swab Analysis

deposswab = np.zeros(Numofsize)
swabsort = sortdata[sortdata['y'] > coveragelen]

for i in range(0,Numofsize):
    tepdata = swabsort.loc[swabsort['y'] > len[i]]
    tepdata = tepdata.loc[tepdata['y'] < len[i+1]]
    deposswab[i] = total_area_Data(inputmesh, tepdata,myIndex, False, False)

#Swab+Spray Analysis


##Mask Analysis

deposnew = np.zeros(Numofsize)

partnew = sortdata.loc[sortdata['size'] == size[0]]
for i in range(1,sizenum):
    if size[i] < 6:
        tepdata = sortdata.loc[sortdata['size'] == size[i]]
        partnew = np.vstack((partnew,tepdata))
    else:
        tepdata = sortdata.loc[sortdata['size'] == size[i]]
        dropsize = int((size[i] - 5)/(max(size) - 5) * 0.65 * tepdata.shape[0])
        drop_indices = np.random.choice(tepdata.index, dropsize, replace=False)
        tepdata = tepdata.drop(drop_indices)
        partnew = np.vstack((partnew,tepdata))
partnew = pandas.DataFrame(data=partnew, columns=myIndex)

for i in range(0,Numofsize):
    tepdata = partnew.loc[partnew['y'] > len[i]]
    tepdata = tepdata.loc[tepdata['y'] < len[i+1]]
    deposnew[i] = total_area_Data(inputmesh, tepdata,myIndex, False, False)

##Mask + Swab Analysis
swabpartnew = partnew[partnew['y'] > coveragelen]
deposswabnew = np.zeros(Numofsize)

for i in range(0,Numofsize):
    tepdata = swabpartnew.loc[swabpartnew['y'] > len[i]]
    tepdata = tepdata.loc[tepdata['y'] < len[i+1]]
    deposswabnew[i] = total_area_Data(inputmesh, tepdata,myIndex, False, False)

#Mask + Swab + Spray Analysis

deposspraynew = np.zeros(Numofsize)

for i in range(0,Numofsize):
    tepdata = swabpartnew.loc[swabpartnew['y'] > len[i]]
    tepdata = tepdata.loc[tepdata['y'] < len[i+1]]
    deposspraynew[i] = total_area_filterData(inputmesh, SpID, tepdata, False, False)

Max = total_area_Data(inputmesh, sortdata, myIndex, show3D, export3Dmesh) #Total depos No Mask as control
Maxspray = total_area_filterData(inputmesh, SpID, sortdata, show3D, export3Dmesh) #Spray
Maxswab = total_area_Data(inputmesh, swabsort, myIndex, show3D, export3Dmesh) #Swab
MedSS = total_area_filterData(inputmesh, SpID, swabsort, show3D, export3Dmesh) #Swab+Spray
MaxM = total_area_Data(inputmesh, partnew, myIndex, show3D, export3Dmesh) #Mask
MedSM = total_area_filterData(inputmesh, SpID, partnew, show3D, export3Dmesh) #Mask+Spray
Minswab = total_area_Data(inputmesh, swabpartnew, myIndex, show3D, export3Dmesh) #Swab+Mask
Min = total_area_filterData(inputmesh, SpID, swabpartnew, show3D, export3Dmesh) #Swab+Spray+Mask
##Spray Analysis








# hist = sortdata['size'].hist(bins = 10)
# hist2 = partnew['size'].hist(bins = 10)
# hist.set_xlabel('Size of Particle(um)')
# hist.set_ylabel('Number of Particles')

# ax = plt.subplot(2,1,1)
# ax.bar(size+1.4, depos, width=0.4, color='b', align='center')
# ax.bar(size+1.8, deposnew, width=0.4, color='g', align='center')
# legen = {'Without Mask':'blue', 'With Mask':'green'}
# labels = list(legen.keys())
# handles = [plt.Rectangle((0,0),1,1, color=legen[label]) for label in labels]
# ax.legend(handles,labels)
# ax.set_title('Deposition rate for particles with different diameter in no mask vs. mask')
# plt.xlabel('Particle diameter(um)')
# plt.ylabel('Deposition Rate(%)')
# ax1 = plt.subplot(2,1,2)
# ax1.hist(sortdata['size']+1.4, 10, width = 0.4, color = 'b', align = 'mid')
# ax1.hist(partnew['size']+1.8, 10, width = 0.4, color = 'g', align = 'mid')
# legen = {'Without Mask':'blue', 'With Mask':'green'}
# labels = list(legen.keys())
# handles = [plt.Rectangle((0,0),1,1, color=legen[label]) for label in labels]
# ax1.legend(handles,labels)
# # ax1.set_title('PDF of particles in no mask vs. mask')
# plt.xlabel('Particle diameter(um)')
# plt.ylabel('Number of Particles')
# plt.figure()
#
#
# ax = plt.subplot(2,1,1)
# ax.bar(size+1.4, deposswab, width=0.4, color='b', align='center')
# ax.bar(size+1.8, deposswabnew, width=0.4, color='g', align='center')
# legen = {'Without Mask':'blue', 'With Mask':'green'}
# labels = list(legen.keys())
# handles = [plt.Rectangle((0,0),1,1, color=legen[label]) for label in labels]
# ax.legend(handles,labels)
# ax.set_title('Deposition rate with swab in no mask vs. mask')
# plt.xlabel('Particle diameter(um)')
# plt.ylabel('Deposition Rate(%)')
# ax1 = plt.subplot(2,1,2)
# ax1.hist(swabsort['size']+1.4, 10, width = 0.4, color = 'b', align = 'mid')
# ax1.hist(swabpartnew['size']+1.8, 10, width = 0.4, color = 'g', align = 'mid')
# legen = {'Without Mask':'blue', 'With Mask':'green'}
# labels = list(legen.keys())
# handles = [plt.Rectangle((0,0),1,1, color=legen[label]) for label in labels]
# ax1.legend(handles,labels)
# # ax1.set_title('PDF of particles in no mask vs. mask')
# plt.xlabel('Particle diameter(um)')
# plt.ylabel('Number of Particles')
# plt.figure()

# fig = plt.subplot
ax = plt.subplot(2,1,1)
ax.bar(len[0:Numofcol]-2, (depos - deposnew)/depos*100, width=2, color = 'k', ec = 'k', align='center')
ax.bar(len[0:Numofcol], (depos - deposswab)/depos*100, width=2, color = 'darkgrey', ec = 'k', align='center')
ax.bar(len[0:Numofcol]+2, (depos - deposspray)/depos*100, width=2, color = 'w', ec = 'k', align='center')
legen = {'Mask':'k','Swab':'darkgrey', 'Spray':'w'}
labels = list(legen.keys())
handles = [plt.Rectangle((0,0),1,1, color=legen[label]) for label in labels]
ax.legend(handles,labels,prop = {"size":15})
ax.set_title('Protection rate with different situation of different size of particles',fontsize = 15)
plt.xlabel('y-axis position(mm)')
plt.ylabel('Protection Rate(%)')
xvalue = np.arange(Numsitcom)
yvalue = [(Max - MaxM)/Max*100,(Max - Maxswab)/Max*100,(Max - Minswab)/Max*100, (Max - Maxspray)/Max*100,
          (Max - MedSS)/Max*100, (Max - MedSM)/Max*100, (Max - Min)/Max*100]
ax1 = plt.subplot(2,1,2)
ax1.bar(xvalue, yvalue,color = 'lightgrey', ec = 'k', align = 'center')
for index, value in enumerate(yvalue):
    ax1.text(index-0.1, value+1, str(int(value))+'%')
xlabels = ['Mask', 'Swab', 'Swab+Mask', 'Spray', 'Spray+Swab', 'Spray+Mask', 'Spray+Swab+Mask']
plt.xticks(xvalue,xlabels)
ax.set_title('Protection rate along y-axis between different situations',fontsize = 15)
plt.xlabel('Protection Method')
plt.ylabel('Protection Rate(%)')
plt.show()
# fig.savefig( fileName+'.svg', dpi=150)