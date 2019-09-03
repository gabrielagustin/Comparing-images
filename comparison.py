#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 05:57:59 2018

@author: gag

Script that calculates statistics:
 - Structural similarity (SSIM) index 
 - Mean squared error (MSE)
to the images. They allow comparisons between estimated variables.
"""


import numpy as np
import matplotlib.pyplot as plt
import functions

from mpl_toolkits.axes_grid1 import make_axes_locatable

from skimage.measure import compare_mse

from skimage.measure import compare_ssim as ssim
from sklearn.metrics import mean_squared_error

fechas= []
fechas.append("2016_05_15")

#### Et observada a 36km
fileETObs = "/media/gag/Datos/Imagenes_satelitales/ET/COMPARACION/"+fechas[0]+"/ETobs/mapa_ETobs36km.asc"
src_ds_ETObs, bandETObs, GeoTETObs, ProjectETObs = functions.openFileHDF(fileETObs, 1)

#### Et modelada a 36km
fileETModelada = "/media/gag/Datos/Imagenes_satelitales/ET/COMPARACION/"+fechas[0]+"/ETmodelada/ET_modelado_"+fechas[0]
src_ds_ETModelada, bandETModelada, GeoTETModelada, ProjectETModelada = functions.openFileHDF(fileETModelada, 1)

transform = GeoTETObs
xmin,xmax,ymin,ymax=transform[0],transform[0]+transform[1]*src_ds_ETObs.RasterXSize,transform[3]+transform[5]*src_ds_ETObs.RasterYSize,transform[3]
#print xmin
#print xmax

fig, ax = plt.subplots()
im1 = ax.imshow(bandETModelada, interpolation='none', cmap=plt.get_cmap('gray'), extent=[xmin,xmax,ymin,ymax], clim=(0, 1))
ax.xaxis.tick_top()
divider = make_axes_locatable(ax)
cax = divider.append_axes('bottom', size="5%", pad=0.05)
cb = plt.colorbar(im1, cax=cax, orientation="horizontal")
cb.set_label('Evapotranspiration Modeled')
#### (W/m^2)
print ("ET modelado:")
print ("Max:" + str(np.max(bandETModelada)))
print ("Min:" + str(np.min(bandETModelada)))
print ("Std:" + str(np.std(bandETModelada)))                


### mapas ET observado interpolado
fig, ax = plt.subplots()
bandETObs = bandETObs*1000
bandETObs = (bandETObs- np.min(bandETObs)) /(np.max(bandETObs)-np.min(bandETObs))
im0 = ax.imshow(bandETObs, cmap=plt.get_cmap('gray'), extent=[xmin,xmax,ymin,ymax], interpolation='none', clim=(0, 1))
ax.xaxis.tick_top()
divider = make_axes_locatable(ax)
cax = divider.append_axes('bottom', size="5%", pad=0.05)
cb = plt.colorbar(im0, cax=cax, orientation="horizontal")
cb.set_label('Evapotranspiration Observed')
#cb.set_clim(vmin=5, vmax=50)

print ("ET observado:")
print ("Max:" + str(np.max(bandETObs)))
print ("Min:" + str(np.min(bandETObs)))
print ("Std:" + str(np.std(bandETObs)))               

### error entre ET modelado y ET observado
print("Error entre ET modelado y observado")

mse_noise= mean_squared_error(y_true = bandETObs , y_pred = bandETModelada)
mse_noise = np.sqrt(mse_noise)
#mse_noise= compare_mse(bandET_modis, bandET_modeled)        
ssim_noise = ssim(bandETObs.flatten(), bandETModelada.flatten())

print("SSIM:" +str(ssim_noise))
print("RMSE:" + str(mse_noise))

fig, ax = plt.subplots()
errorModelado = np.sqrt((bandETModelada - bandETObs)**2)
im0 = ax.imshow(errorModelado, cmap=plt.cm.jet, extent=[xmin,xmax,ymin,ymax], interpolation='none', clim=(0, 1))
ax.xaxis.tick_top()
divider = make_axes_locatable(ax)
cax = divider.append_axes('bottom', size="5%", pad=0.05)
cb = plt.colorbar(im0, cax=cax, orientation="horizontal")
cb.set_label('RMSE')
#        cb.set_clim(vmin=5, vmax=50)
plt.show()               
