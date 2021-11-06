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
from datetime import date


#===================== INPUT PARAMETERS ==========================
# inputFile = ['para_velocity_0_dia_1_50.txt','para_velocity_3_dia_1_50.txt','para_velocity_6_dia_1_50.txt','para_velocity_10_dia_1_50.txt']
inputFile = ['ang_dis_vel_1200000_part_viral_wide.txt']
#Title of the figure generated
figTitle = "Y axis Profile (0um - 100um)"
figXlabel = 'Y axis'
figYlabel = 'ratio of particles deposited per location'
sizeOfInterest = 10  # Upper bound Size defined as microns
sizeOfInterest2 = 0 # Lower bound Sized defined as microns
# define axis of interest (x, y or z) 
axisOfInterest = 'y'
# Filename of figure
fileName = ''+str(date.today().isoformat())+'_deposition_profile_along_'+axisOfInterest+'_for_'+str(sizeOfInterest)

# Nb of columns in the txt file
nbOfColumns=4  
# Nb of bins in the histogram
nbOfBins = 12
# diameters to be separated (NOTE: the particle diameter is specified in mm in the txt file. Here we use microns)
diams = np.array([0.1, 1., 3., 4.,4.])*0.001
# diams = np.array([5.,10., 30., 50.,50.])*0.001
# diams = np.array([10., 20., 30., 40., 50, 80, 100])*0.001
# Velocity m/s
velo = np.array([0.,3.,6.,10.])
# Cone Angle (deg)
deg = np.array([0.,30.,45.,60.,90.])
# Display all particles independently from their size
displayCombined = False
# Do we want to normalize the deposition with the nb of particles of a specific size
normalized = True  
# Column names for the txt file
myIndex = ['x', 'y', 'z','size']
# myIndex = np.array(['x', 'y', 'z','size', 'cone_angle','air_vel','spray_vel'])
#===================== END INPUT PARAMETERS ==========================

my_data = pandas.read_csv(inputFile[0], delim_whitespace=True, comment='%', header=0, names=myIndex)
# my_data2 = pandas.read_csv(inputFile[1], delim_whitespace=True, comment='%', header=0, names=myIndex)
# my_data3 = pandas.read_csv(inputFile[2], delim_whitespace=True, comment='%', header=0, names=myIndex)
# my_data4 = pandas.read_csv(inputFile[3], delim_whitespace=True, comment='%', header=0, names=myIndex)
# my_data5 = pandas.read_csv(inputFile[4], delim_whitespace=True, comment='%', header=0, names=myIndex)
#print (my_data.head(30))

# REMOVE THE NaN from the data
clean_data = my_data.dropna()
clean_data = clean_data[clean_data['z'] > min(clean_data['z']+max(clean_data['size']))]
outdata = len(clean_data[clean_data['z'] < min(clean_data['z']+max(clean_data['size']))])
# clean_data2 = my_data2.dropna()
# clean_data3 = my_data3.dropna()
# clean_data4 = my_data4.dropna()
# clean_data5 = my_data5.dropna()
#print (clean_data.head(30))

# COMBINE SIZE OF INTEREST
# subset1 = clean_data[clean_data["size"] < sizeOfInterest*0.001]
# subset1 = subset1[subset1["size"] > sizeOfInterest2*0.001]
# subset2 = clean_data2[clean_data2["size"] < sizeOfInterest*0.001]
# subset2 = subset2[subset2["size"] > sizeOfInterest2*0.001]
# subset3 = clean_data3[clean_data3["size"] < sizeOfInterest*0.001]
# subset3 = subset3[subset3["size"] > sizeOfInterest2*0.001]
# subset4 = clean_data4[clean_data4["size"] < sizeOfInterest*0.001]
# subset4 = subset4[subset4["size"] > sizeOfInterest2*0.001]
# subset5 = clean_data5[clean_data5["size"] < sizeOfInterest*0.001]
# subset5 = subset5[subset5["size"] > sizeOfInterest2*0.001]


fig, ax = plt.subplots()
a_heights, a_bins = np.histogram(clean_data[axisOfInterest], nbOfBins)

# Width of histograms
width = (a_bins[1] - a_bins[0])/ (diams.size+1)

# If selected, shows histogram for all particles
# Below, I normalize the height of histogram with the number of particles
if (displayCombined): 
    if (normalized):
        ax.bar(a_bins[:-1], a_heights / (clean_data.size / nbOfColumns), width=width, facecolor='black', label='all particles')
    else:
        ax.bar(a_bins[:-1], a_heights, width=width, facecolor='black', label='all particles')

# myLabel=str(subset1.size/nbOfColumns) + ' particles below ' + str(sizeOfInterest)+'$\mu$m' + ' with ' + str(velo[0]) + ' m/s'
# myLabel2=str(subset2.size/nbOfColumns) + ' particles below ' + str(sizeOfInterest)+'$\mu$m' + ' with ' + str(velo[1]) + ' m/s'
# myLabel3=str(subset3.size/nbOfColumns) + ' particles below ' + str(sizeOfInterest)+'$\mu$m' + ' with ' + str(velo[2]) + ' m/s'
# myLabel4=str(subset4.size/nbOfColumns) + ' particles below ' + str(sizeOfInterest)+'$\mu$m' + ' with ' + str(velo[3]) + ' m/s'
# myLabel5=str(subset4.size/nbOfColumns) + ' particles below ' + str(sizeOfInterest)+'$\mu$m' + ' with ' + str(velo[4]) + ' m/s'
# b_heights, b_bins = np.histogram(subset1['y'], bins=a_bins)
# b_heights2, b_bins2 = np.histogram(subset2['y'], bins=a_bins)
# b_heights3, b_bins3 = np.histogram(subset3['y'], bins=a_bins)
# b_heights4, b_bins4 = np.histogram(subset4['y'], bins=a_bins)
# b_heights5, b_bins5 = np.histogram(subset5['y'], bins=a_bins)
# ax.plot(b_bins[:-1]+(width), b_heights/(subset1.size/nbOfColumns), label=myLabel)
# ax.plot(b_bins2[:-1]+(width), b_heights2/(subset2.size/nbOfColumns), label=myLabel2)
# ax.plot(b_bins3[:-1]+(width), b_heights3/(subset3.size/nbOfColumns), label=myLabel3)
# ax.plot(b_bins4[:-1]+(width), b_heights4/(subset4.size/nbOfColumns), label=myLabel4)
# ax.plot(b_bins5[:-1]+(width), b_heights5/(subset5.size/nbOfColumns), label=myLabel5)
# LOOP ON ALL DIAMETERS CONSIDERED
# for i in diams:
i = 0
while i < diams.size:
    # For first diameter, we pick the diameters that are below the specified value
    if i == 0:
        subset = clean_data[clean_data["size"] < diams[i]]

        myLabel=str(subset.size/nbOfColumns) + ' particles below ' + str(diams[i]*1000)+'$\mu$m'
        print ('- Loop 0: ' + str(subset.size/nbOfColumns) + ' particles ' + myLabel)

    # For last diameter, we pick the diameters that are greater than the specified value
    elif i == (diams.size - 1) :
        subset = clean_data[clean_data["size"] > diams[i]]
        myLabel=str(subset.size/nbOfColumns) + ' particles above ' + str(diams[i]*1000)+'$\mu$m'
        print ('- Last loop: ' + str(subset.size/nbOfColumns) + ' particles ' + myLabel)

    # Else, pick the one in between the previous and the current diameter
    else:
        subset = clean_data[clean_data["size"] > diams[i-1]]
        subset = subset[subset["size"] < diams[i]]
        myLabel=str(subset.size/nbOfColumns) + ' particles ' + str(diams[i-1]*1000)+'$\mu$m < diam < '+ str(diams[i]*1000)+'$\mu$m'
        print ('- Loop nb ' + str(i) + ' with ' + str(subset.size/nbOfColumns) + ' particles with ' + myLabel )

    # Create the bins and heights
    b_heights, b_bins = np.histogram(subset['y'], bins=a_bins)
    if (normalized):
        #ax.bar(b_bins[:-1]+(width*(i+1)), b_heights/(subset.size/nbOfColumns), width=width, facecolor=colors[i], label=myLabel)
        ax.bar(b_bins[:-1]+(width*(i+1)), b_heights/(subset.size/nbOfColumns), width=width, label=myLabel)
    else:
        ax.bar(b_bins[:-1]+(width*(i+1)), b_heights, width=width, facecolor=colors[i], label=myLabel)


    i+=1
#     # ------- End of While -------

# Add title and axis names
ax.set_xlabel(figXlabel)  # Add an x-label to the axes.
ax.set_ylabel(figYlabel)  # Add a y-label to the axes.
ax.set_title(figTitle)  # Add a title to the axes.

# Add legends
ax.legend()

plt.show()
fig.savefig( fileName+'.svg', dpi=150)


