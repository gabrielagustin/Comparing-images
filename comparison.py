#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 05:57:59 2018

@author: gag

Script que calcula los estadísticos :
 - Structural similarity (SSIM) index 
 - Mean squared error (MSE)
sobre imagenes que permite realizar comparaciones entre 
variables estimadas. 
"""



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from skimage import data, img_as_float
from mpl_toolkits.axes_grid1 import make_axes_locatable

from skimage.measure import compare_mse


from osgeo import gdal

from skimage.measure import compare_ssim as ssim
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score

import functions

def mse(x, y):
    return np.linalg.norm(x - y)



gdal.UseExceptions()
fileET_modis = "/.../ET_modis.img"
src_ds_ET_modis, bandET_modis, GeoTET_modis, ProjectET_modis = functions.openFileHDF(fileET_modis,1)




fileET_modeled = "/.../ETSM_final.img"
src_ds_ET_modeled, bandET_modeled, GeoTET_modeled, ProjectET_modeled = functions.openFileHDF(fileET_modeled,1)


#### con ambas imagenes se crea un objeto pandas, y luego se realiza el filtrado por 
#### pixel segun el valor de evapotranspiracion
dataset = pd.DataFrame({'ET_modis':bandET_modis.flatten(),'ET_mod':bandET_modeled.flatten()})

dataset = dataset[dataset.ET_modis < 500]

print (dataset)
print(np.max(dataset.ET_modis))


#### comparación inicial sin ruido, imagen ET modis
#mse_none = mse(bandET_modis, bandET_modis)
#mse_none = compare_mse(bandET_modis, bandET_modis)
mse_none = mean_squared_error(y_true = dataset.ET_modis , y_pred = dataset.ET_modis)
mse_none = np.sqrt(mse_none)

ssim_none = ssim(bandET_modis, bandET_modis, data_range = 350- 0)


#### comparacion entre imagen ET de modis y la imagen de ET modelada
#mse_noise = mse(bandET_modis, bandET_modeled)

mse_noise= mean_squared_error(y_true = dataset.ET_modis , y_pred = dataset.ET_mod)
mse_noise = np.sqrt(mse_noise)
#mse_noise= compare_mse(bandET_modis, bandET_modeled)

ssim_noise = ssim(bandET_modis, bandET_modeled, data_range= 350- 0)



label = 'RMSE: {:.2f}, SSIM: {:.2f}'

transform = GeoTET_modis
xmin,xmax,ymin,ymax=transform[0],transform[0]+transform[1]*src_ds_ET_modis.RasterXSize,transform[3]+transform[5]*src_ds_ET_modis.RasterYSize,transform[3]




#### se grafican las imágenes con sus respectivos estadísticos

fig, ax = plt.subplots()
im1 = ax.imshow(bandET_modis, extent=[xmin,xmax,ymin,ymax], interpolation='None', cmap=plt.cm.gray, vmin=0, vmax=300)
ax.xaxis.tick_top()
divider = make_axes_locatable(ax)
cax = divider.append_axes('bottom', size="5%", pad=0.05)
cb = plt.colorbar(im1, cax=cax, orientation="horizontal")
#cb.set_label('Volumetric SM (%)')
cb.set_label('ET Modis (W/m^2)')
#cb.set_clim(vmin=5, vmax=55)
#ax.set_xlabel(label.format(mse_none, ssim_none))
#ax.set_title('ET MODIS')

fig, ax = plt.subplots()
im2 = ax.imshow(bandET_modeled, extent=[xmin,xmax,ymin,ymax], interpolation='None', cmap=plt.cm.gray, vmin=0, vmax=300)
ax.xaxis.tick_top()
divider = make_axes_locatable(ax)
cax = divider.append_axes('bottom', size="5%", pad=0.05)
cb = plt.colorbar(im2, cax=cax, orientation="horizontal")
#cb.set_label('Volumetric SM (%)')
cb.set_label('ET Modeled (W/m^2)')
#cb.set_clim(vmin=5, vmax=55)
ax.set_xlabel(label.format(mse_noise, ssim_noise))
#ax.set_title('ET MODIS')

print("SSIM:" +str(ssim_noise))

print("RMSE:" + str(mse_noise))

#im2 = ax[1].imshow(bandET_modeled,extent=[xmin,xmax,ymin,ymax], interpolation='None', cmap=plt.cm.gray, vmin=0, vmax=350)
#ax[1].set_xlabel(label.format(mse_noise, ssim_noise))
#ax[1].set_title('ET modeled')

#ax[2].imshow(img_const, cmap=plt.cm.gray, vmin=0, vmax=1)
#ax[2].set_xlabel(label.format(mse_const, ssim_const))
#ax[2].set_title('Image plus constant')
#cbar = fig.colorbar(cax)

#divider = make_axes_locatable(ax[0])
#cax = divider.append_axes("right", size="5%", pad=0.3)
#cba = plt.colorbar(pa, cax=cax)

#axlist = [ax[0],ax[1]]
#
#divider = make_axes_locatable(axlist)
#cax = divider.new_vertical(size="5%", pad=0.7, pack_start=True)

#fig.colorbar(im2, cax=cax, orientation="horizontal")

#fig.colorbar(im2, ax=axes, orientation='horizontal', fraction=.1)

#fig.colorbar(im1, orientation='horizontal') 
plt.tight_layout()
plt.show()
