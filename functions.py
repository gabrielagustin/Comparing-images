#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 05:57:59 2018

@author: gag


"""



import numpy as np
from osgeo import gdal, ogr, gdalconst
import sys



def openFileHDF(file, nroBand):
    #print "Open File"
    # file = path+nameFile
    #print file
    try:
        src_ds = gdal.Open(file)
    except (RuntimeError, e):
        print('Unable to open File')
        print(e)
        sys.exit(1)

    cols = src_ds.RasterXSize
    rows = src_ds.RasterYSize
    #print cols
    #print rows
    bands = src_ds.RasterCount
    #print bands

    # se obtienen las caracteristicas de las imagen HDR
    GeoT = src_ds.GetGeoTransform()
    #print GeoT
    Project = src_ds.GetProjection()

    try:
        srcband = src_ds.GetRasterBand(nroBand)
    except(RuntimeError, e):
        # for example, try GetRasterBand(10)
        print('Band ( %i ) not found' % band_num)
        print(e)
        sys.exit(1)
    band = srcband.ReadAsArray()
    #nRow, nCol = band.shape
    #nMin = np.min((nRow,nCol))
    ##print "minimo: "+ str(nMin)
    #nMin = int(nMin/2)*2
    ##print "minimo par: "+ str(nMin)
    #factor = int(np.log(nMin)/np.log(2))
    ##print "factor: " + str(factor)
    #tamanio = 2**factor
    ##print "tamanio:" + str(tamanio)
    #band = band[:tamanio,:tamanio]
    #### creo src_ds con nuevo tamanio
    #src_ds = gdal.GetDriverByName('MEM').Create('', tamanio, tamanio, 1, gdal.GDT_Float64)
    #src_ds.SetProjection(Project)
    #geotransform = GeoT
    #src_ds.SetGeoTransform(geotransform)
    #src_ds.GetRasterBand(1).WriteArray(np.array(band))
    #band = src_ds.ReadAsArray()
    return src_ds, band, GeoT, Project


