import matplotlib
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import pandas
import scipy.stats as sci

class nf(float):
    def __repr__(self):
        s = f'{self:.1f}'
        return f'{self:.0f}' if s[-1] == '0' else s


#===================== INPUT PARAMETERS ==========================
csvfile = '2021-04-20ang_dis_vel_600000_part_inhale1m.txt.csv'
myIndex = ['cone_angle','insertion_dis','spray_vel','Percent']
IndexofInterest = 'spray_vel'
totalsit = 120
Nbofinst = 30
nbofind = totalsit/Nbofinst
figXlabel = 'spray velocity(m/s)'
figYlabel = 'insertion depth(mm)'
figTitle = ['Deposition Percentage Contour plot in relationship with pi/2 cone angle',
            'Deposition Percentage Contour plot in relationship with pi/3 cone angle',
            'Deposition Percentage Contour plot in relationship with pi/4 cone angle',
            'Deposition Percentage Contour plot in relationship with pi/6 cone angle',]
#===================== END INPUT PARAMETERS ==========================


raw_data = pandas.read_csv(csvfile, delim_whitespace=False, comment='%', header=0)
# raw_data = raw_data.sort_values()
raw_data = raw_data[[x > 1 for x in raw_data['Percent']]].to_numpy()
for n in range(0,int(nbofind)):

    tep = raw_data[Nbofinst*n:(n+1)*Nbofinst,1:5]
    clean_data = pandas.DataFrame(data=tep, columns= myIndex)
    fig,ax = plt.subplots()
    X = np.zeros(Nbofinst)
    X = np.array(clean_data[myIndex[2]].to_numpy()).reshape(5,6)
    Y = np.array(clean_data[myIndex[1]].to_numpy()).reshape(5,6)
    Z = np.array(clean_data[myIndex[3]].to_numpy()).reshape(5,6)
    CS = ax.contour(X,Y,Z)

    CS.levels = [nf(val) for val in CS.levels]
    if plt.rcParams["text.usetex"]:
        fmt = r'%r \%%'
    else:
        fmt = '%r %%'
    ax.clabel(CS, CS.levels, inline=True, fmt=fmt, fontsize=10)
    ax.set_xlabel(figXlabel)
    ax.set_ylabel(figYlabel)
    ax.set_title(figTitle[n])
    plt.show()
F,p = sci.f_oneway(Z[0],Z[1],Z[2],Z[3])
print(F,p)
