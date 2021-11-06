# -*- coding: utf-8 -*-
"""
Created on Mon Dec  14 18:44:24 2020
    This script shows where particles have landed on a mesh and changes the color of these triangles. 

Parameters:
    2 inputs: (1) a mesh and (2) particles location

Notes: 
    - Must first install trimesh. To do this from anaconda command prompt:
        > conda install -c conda-forge trimesh
    - might want to install networkx too:
        > conda install -c conda-forge networkx
    - Must install numpy-stl:
        conda install -c conda-forge numpy-stl
    - Must install pandas too:
        conda install -c conda-forge pandas 
    - Must install pyrender
        pip install pyrender
    - Must install pyglet
        conda install -c conda-forge pyglet

    - more info on trimesh here:
        https://github.com/mikedh/trimesh
    - Has the functionality to evaluate distance between point and mesh 
        more info here: https://github.com/mikedh/trimesh/blob/master/examples/nearest.ipynb
    - Info on pyrender:
        https://readthedocs.org/projects/pyrender/downloads/pdf/stable/

    -other note: choose python library
        https://softwarerecs.stackexchange.com/questions/64807/which-mesh-processing-library-for-python-to-chose

    - Specs for OBJ file: https://en.wikipedia.org/wiki/Wavefront_.obj_file
@author: ashao, jmbouteiller

"""

import math
from Coverage_Functions import total_area, Particle_dep
import numpy as np
import matplotlib.pyplot as plt


##Input Parameter

inputFile = np.array(['ang_dis_vel_120000_part.txt'])
inputmesh = 'High_Reshalf.obj'
var = ['3mm','5mm','7mm','9mm']
myIndex = ['x', 'y', 'z', 'size']
xaxis = np.array([3,5,7,9])
show3D = True
export3Dmesh = False
figxlabel = 'Insertion Depth (mm)'
figtitle = 'Coverage percentage with a function of insertion depth'

##

##Main
figylabel = 'Coverage Percentage (%)'
# fig, ax = plt.subplots()
# fig.set_size_inches(18.5,10.5)
percent = np.zeros(inputFile.size)
mylabel = ['' for x in range(inputFile.size)]
i = 0
widthx = (max(xaxis) - min(xaxis))/xaxis.size
while i < inputFile.size:
    percent[i] = total_area(inputmesh, inputFile[i], myIndex, var[i], show3D, export3Dmesh)
    mylabel = str("{:.2f}".format(percent[i])) + '% is covered with ' + var[i] + 'mm insertion depth'
    # ax.bar(xaxis[i], percent[i], label=mylabel,width = widthx)
    i += 1
##Plot Histo

# ax.set_xlabel(figxlabel)
# ax.set_ylabel(figylabel)
# ax.set_title(figtitle)

# ax.legend()
# plt.show()
# fig.savefig(figxlabel +'.svg', dpi=150)