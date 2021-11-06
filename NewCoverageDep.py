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
inputFile = '120000_part_viral.txt'
inputmesh = 'halfGeometry2.obj'
show3D = False
export3Dmesh = False
filename = ''+str(date.today().isoformat())+inputFile
# Column names for the txt file
# myIndex = np.array(['x', 'y', 'z','size', 'cone_angle','air_vel','spray_vel'])
# myIndex = np.array(['x', 'y', 'z','size','inhale_speed'])
myIndex = np.array(['x', 'y', 'z','size'])
swabpercent = 1 #Coverage Percentage of using Swab 1 being 100%
swabpos = 1/3 # Swab coverage location in y axis, fraction of anterior coverage
Numsitcom = 3 #Number of situation to compare
# #===================== END INPUT PARAMETERS ==========================

raw_data = pandas.read_csv(inputFile, delim_whitespace=True, comment='%', header=0)
raw_data = raw_data.dropna()
raw_data = raw_data.to_numpy()
Npara = len(myIndex)

MaxD = pandas.DataFrame(data=raw_data[:,1:Npara+1], columns=myIndex)
sortdata = MaxD.sort_values(['size'])
coveragelen = min(sortdata['y']) + (max(sortdata['y']) - min(sortdata['y']))*swabpos
NumofSit = int((np.shape(raw_data)[1] - 1)/Npara)
sortdata['size'] = (sortdata['size'] * 1000).astype(int)
size = np.array(sortdata['size'].unique())
Numofsize = len(size)

Max = total_area_Data(inputmesh, sortdata, myIndex, show3D, export3Dmesh)
depos = np.zeros(Numofsize)
deposswab = np.zeros(Numofsize)
for i in range(0,Numofsize):
    tepdata = sortdata.loc[sortdata['size'] == size[i]]
    depos[i] = total_area_Data(inputmesh, tepdata,myIndex, False, False)

swabsort = sortdata[sortdata['y'] < coveragelen]
Maxswab = total_area_Data(inputmesh, swabsort, myIndex, show3D, export3Dmesh)
for i in range(0,Numofsize):
    tepdata = swabsort.loc[swabsort['size'] == size[i]]
    deposswab[i] = total_area_Data(inputmesh, tepdata,myIndex, False, False)


deposnew = np.zeros(Numofsize)
deposswabnew = np.zeros(Numofsize)
partnew = sortdata.loc[sortdata['size'] == size[0]]
deposnew[0] = total_area_Data(inputmesh, partnew, myIndex, False, False)
for i in range(1,Numofsize):
    if size[i] < 6:
        tepdata = sortdata.loc[sortdata['size'] == size[i]]
        deposnew[i] = total_area_Data(inputmesh, tepdata, myIndex, False, False)
        partnew = np.vstack((partnew,tepdata))
    else:
        tepdata = sortdata.loc[sortdata['size'] == size[i]]
        dropsize = int((size[i] - 5)/(max(size) - 5) * 0.65 * tepdata.shape[0])
        drop_indices = np.random.choice(tepdata.index, dropsize, replace=False)
        tepdata = tepdata.drop(drop_indices)
        deposnew[i] = total_area_Data(inputmesh, tepdata, myIndex, False, False)
        partnew = np.vstack((partnew,tepdata))
partnew = pandas.DataFrame(data=partnew, columns=myIndex)
Min = total_area_Data(inputmesh, partnew, myIndex, show3D, export3Dmesh)
swabpartnew = partnew[partnew['y'] < coveragelen]
Minswab = total_area_Data(inputmesh, swabpartnew, myIndex, show3D, export3Dmesh)
for i in range(0,Numofsize):
    tepdata = swabpartnew.loc[swabpartnew['size'] == size[i]]
    deposswabnew[i] = total_area_Data(inputmesh, tepdata,myIndex, False, False)




# hist = sortdata['size'].hist(bins = 10)
# hist2 = partnew['size'].hist(bins = 10)
# hist.set_xlabel('Size of Particle(um)')
# hist.set_ylabel('Number of Particles')

ax = plt.subplot(2,1,1)
ax.bar(size+1.4, depos, width=0.4, color='b', align='center')
ax.bar(size+1.8, deposnew, width=0.4, color='g', align='center')
legen = {'Without Mask':'blue', 'With Mask':'green'}
labels = list(legen.keys())
handles = [plt.Rectangle((0,0),1,1, color=legen[label]) for label in labels]
ax.legend(handles,labels)
ax.set_title('Deposition rate for particles with different diameter in no mask vs. mask')
plt.xlabel('Particle diameter(um)')
plt.ylabel('Deposition Rate(%)')
ax1 = plt.subplot(2,1,2)
ax1.hist(sortdata['size']+1.4, 10, width = 0.4, color = 'b', align = 'mid')
ax1.hist(partnew['size']+1.8, 10, width = 0.4, color = 'g', align = 'mid')
legen = {'Without Mask':'blue', 'With Mask':'green'}
labels = list(legen.keys())
handles = [plt.Rectangle((0,0),1,1, color=legen[label]) for label in labels]
ax1.legend(handles,labels)
# ax1.set_title('PDF of particles in no mask vs. mask')
plt.xlabel('Particle diameter(um)')
plt.ylabel('Number of Particles')
plt.figure()
ax = plt.subplot(2,1,1)
ax.bar(size+1.4, deposswab, width=0.4, color='b', align='center')
ax.bar(size+1.8, deposswabnew, width=0.4, color='g', align='center')
legen = {'Without Mask':'blue', 'With Mask':'green'}
labels = list(legen.keys())
handles = [plt.Rectangle((0,0),1,1, color=legen[label]) for label in labels]
ax.legend(handles,labels)
ax.set_title('Deposition rate with swab in no mask vs. mask')
plt.xlabel('Particle diameter(um)')
plt.ylabel('Deposition Rate(%)')
ax1 = plt.subplot(2,1,2)
ax1.hist(swabsort['size']+1.4, 10, width = 0.4, color = 'b', align = 'mid')
ax1.hist(swabpartnew['size']+1.8, 10, width = 0.4, color = 'g', align = 'mid')
legen = {'Without Mask':'blue', 'With Mask':'green'}
labels = list(legen.keys())
handles = [plt.Rectangle((0,0),1,1, color=legen[label]) for label in labels]
ax1.legend(handles,labels)
# ax1.set_title('PDF of particles in no mask vs. mask')
plt.xlabel('Particle diameter(um)')
plt.ylabel('Number of Particles')
plt.figure()
ax = plt.subplot(2,1,1)
ax.bar(size+1.2, (depos - deposnew)/depos*100, width=0.2, color='b', align='center')
ax.bar(size+1.4, (depos - deposswabnew)/depos*100, width=0.2, color='g', align='center')
ax.bar(size+1.6, (depos - deposswab)/depos*100, width=0.2, color='y', align='center')
legen = {'Mask':'blue', 'Swab':'yellow' ,'Swab+Mask':'green'}
labels = list(legen.keys())
handles = [plt.Rectangle((0,0),1,1, color=legen[label]) for label in labels]
ax.legend(handles,labels)
ax.set_title('Protection rate with swab vs. mask')
plt.xlabel('Particle diameter(um)')
plt.ylabel('Protection Rate(%)')
xvalue = np.arange(Numsitcom)
yvalue = [(Max - Min)/Max*100,(Max - Maxswab)/Max*100,(Max - Minswab)/Max*100]
ax1 = plt.subplot(2,1,2)
ax1.bar(xvalue, yvalue, align = 'center')
xlabels = ['Mask', 'Swab', 'Swab+Mask']
plt.xticks(xvalue,xlabels)
ax.set_title('Protection rate between different situations')
plt.xlabel('Protection Method')
plt.ylabel('Protection Rate(%)')
plt.show()