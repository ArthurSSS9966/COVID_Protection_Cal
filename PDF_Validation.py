import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

nbofbins = 60
# myIndex = np.array(['x', 'y', 'z','Diameter', 'cone_angle','velocity'])
myIndex = np.array(['x', 'y', 'z','Diameter','dose'])
# myIndex = np.array(['x', 'y', 'z','Diameter', 'cone_angle','air_vel','spray_vel'])

my_data = pd.read_csv('3000_68.txt',delim_whitespace = True, comment = '%', header = 0, names = myIndex)
clean_data = my_data.dropna()

Volume = 0
for diameter in clean_data['Diameter']:
    PartV = np.pi*(4/3)*((diameter*3/2)**3)
    Volume = Volume + PartV
VolumeTtl = np.pi*(4/3)*((clean_data['Diameter']*3/2)**3)*(10**9)

Newdata = pd.DataFrame()
Newdata['Diameter'] = clean_data['Diameter']
Newdata['Volume'] = VolumeTtl



# plt.figure()
# n,bins,patches = plt.hist(x = clean_data['Diameter'],bins = 'auto')
hist = (clean_data['Diameter']*1000).hist(bins = 60)
# hist2 = VolumeTtl.hist(bins = 20)
hist.set_xlabel('Size of Particle(um)')
hist.set_ylabel('Number of Particles')

# plt.plot(clean_data)
print(Volume)