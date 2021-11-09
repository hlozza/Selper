import sys
import os
from osgeo import gdal
from osgeo import osr
from osgeo import ogr
import numpy
from math import floor

# https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html
# Create a point
point1 = ogr.Geometry(ogr.wkbPoint)
point1.AddPoint(-60.34, -34.60)
print( point1.ExportToWkt() )

# Or 
# Create a point as WKT
wkt = "POINT (-61.54 -35.57)"
point2 = ogr.CreateGeometryFromWkt(wkt)
print( "%f,%f" % (point2.GetX(), point2.GetY()) )

# Reference System
srs = osr.SpatialReference()
srs.SetWellKnownGeogCS("EPSG:4326")

# CREATE in memory VECTOR layer
outdriver=ogr.GetDriverByName('MEMORY')
source=outdriver.CreateDataSource('memData')
lyr = source.CreateLayer( 'point', srs=srs, geom_type=ogr.wkbPoint)

# ADD a id FIELD
idField = ogr.FieldDefn("id", ogr.OFTInteger)
lyr.CreateField(idField)


feat = ogr.Feature( lyr.GetLayerDefn() )
feat.SetGeometryDirectly( point1 )
feat.SetField("id", 1)
lyr.CreateFeature( feat )
feat = None


feat = ogr.Feature( lyr.GetLayerDefn() )
feat.SetGeometryDirectly( point2 )
feat.SetField("id", 2)
lyr.CreateFeature( feat )
feat = None


# If shapefile is available
# shp_filename = 'points.shp'
# ds=ogr.Open(shp_filename)
# lyr=ds.GetLayer()

# Open raster
src_filename = 'Output/CONAE_MOD_MHS_DSS_MSM_20211020_v001.tif'
src_ds=gdal.Open(src_filename) 
gt=src_ds.GetGeoTransform()
rb=src_ds.GetRasterBand(1)

for feat in lyr:
    geom = feat.GetGeometryRef()
    mx,my=geom.GetX(), geom.GetY()  #coord in map units

    #Convert from map to pixel coordinates.
    #Only works for geotransforms with no rotation.
    px = floor((mx - gt[0]) / gt[1]) #x pixel
    py = floor((my - gt[3]) / gt[5]) #y pixel

    intval=rb.ReadAsArray(px,py,1,1)
    print( intval[0] )#intval is a numpy array, length=1 as we only asked for 1 pixel value

## CLOSE
source = None
rb = None  # dereference band to avoid gotcha described previously
src_ds = None  # save, close

