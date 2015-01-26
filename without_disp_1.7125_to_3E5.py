#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
#from matplotlib import contour
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
from matplotlib import cm, rcParams
# import pylab
# pylab.rcParams['xtick.major.pad']='80'
# pylab.rcParams['ytick.major.pad']='80'
# print pylab.rcParams.keys()
# rcParams['axes.formatter.use_locale']=1
X = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 
     5e3, 5e3, 5e3, 5e3, 5e3, 5e3, 5e3, 5e3, 5e3, 5e3, 
     1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 1e4, 
     1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 1.5e4, 
     2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 2e4, 
     2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 2.5e4, 
     3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4, 3e4]
Y = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
     0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
     0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
     0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
     0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
     0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
     0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818,
     0, 5, 10, 15, 20, 25, 30, 35, 40, 45.0818]
Z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0.00000001043739453, 0.00000002052395227, 0.00000003104905599, 0.00000004148645052, 0.00000005183613585, 0.0000000622735304, 0.0000000725355065, 0.0000000831483194, 0.0000000938488416,
     0, 0.00000005201155424, 0.0000001041985269, 0.0000001562977903, 0.0000002082216354, 0.0000002602331896, 0.000000312332453, 0.0000003643440073, 0.00000041653098, 0.0000004694196262,
     0, 0.0000001039353993, 0.0000002083970538, 0.0000003123324531, 0.0000004165309799, 0.0000005205540884, 0.0000006249280337, 0.0000007288634329, 0.0000008327988322, 0.0000009387515431,
     0, 0.0000001559469535, 0.0000003125955806, 0.0000004685425342, 0.0000005737058622, 0.000000780787278, 0.0000009369973592, 0.00000109329515, 0.000001249242103, 0.000001407995751,
     0, 0.0000002078707986, 0.0000004162678523, 0.0000006244894877, 0.0000008327988323, 0.000001040845049, 0.000001249066685, 0.00000145728832, 0.000001665597665, 0.000001876976831,
     0, 0.000000260408608, 0.0000005206417976, 0.000000780787278, 0.000001041108177, 0.000001301253657, 0.000001561662265, 0.000001821807746, 0.000002082128644, 0.000002346659585,
     0, 0.0000003122447438, 0.0000006246649061, 0.0000009369973592, 0.000001249154394, 0.000001561399138, 0.000001873731591, 0.000002186064044, 0.000002497870242, 0.000002815816083]
xi = np.linspace(np.min(X), np.max(X))
yi = np.linspace(np.min(Y), np.max(Y))
zi = griddata(X, Y, Z, xi, yi)
plt.contour(xi, yi, zi)
fig = plt.figure()
#ax = Axes3D(fig)
ax = fig.add_subplot(111, projection='3d')
ax.set_title(u"Without dispersion with n1=1.7127, Umax = 45.0818")
#ax.set_ylim(0,1)
ax.set_xlabel(u'Vo[m/s]')
ax.set_ylabel(u'Vd[m/s]')
ax.set_zlabel(u'ddle')
zlabs = ['{:1.1E}'.format(i*1E-7) for i in xrange(0, 35, 5)]
ax.set_zticklabels(zlabs)
ax.set_zticks(zlabs)
# xlabs = ['{:1.0E}'.format(i*1E2) for i in xrange(0, 350, 50)]
xlabs = ['{:1.1E}'.format(i) for i in xrange(0, 35000, 5000)]
print xlabs
ax.set_xticklabels(xlabs)
ax.set_xticks(xlabs)


# ax.get_xaxis().get_major_formatter().set_useOffset(False)
# print dir(ax.get_xaxis().get_major_formatter())
xim, yim = np.meshgrid(xi, yi) 
Gx, Gy = np.gradient(zi) #gradient with respect to x and y
G = (Gx**2+Gy**2)**.5 #gradient magitude
N = G/G.max()# normalize 0..1
ax.plot_surface(xim, yim, zi, rstride=1, cstride=1, facecolors=cm.jet(N), linewidth=0, antialiased=False, shade=False)
plt.show()