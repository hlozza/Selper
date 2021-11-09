import sys
import os
import glob
import re
from osgeo import gdal
from osgeo import osr
from osgeo import ogr
import numpy
from math import floor
import matplotlib.pyplot as plt




def main(argc, argv):
    if (argc != 5):
        print ("Use {0} lon lat rel_dir prefix".format(sys.argv[0]))
        return 128

    lon = sys.argv[1]
    lat = sys.argv[2]
    rel_dir = sys.argv[3]
    prefix = sys.argv[4]

    # Create a point
    point1 = ogr.Geometry(ogr.wkbPoint)
    point1.AddPoint(float(lon), float(lat))
    print( point1.ExportToWkt() )

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


    # Open raster
    src_dir = os.path.abspath(rel_dir)
    src_files = glob.glob(os.path.join(src_dir, prefix + '*tif'))

    days = []
    values = []
    for src_filename in src_files:

        # Print date
        src_tif = re.search('(\d{8})', os.path.basename(src_filename))
        days.append(numpy.single(src_tif.group(1)[6:]))
        print( src_tif.group(1) )
        src_ds=gdal.Open(src_filename) 
        gt=src_ds.GetGeoTransform()
        rb=src_ds.GetRasterBand(1)

        feat = lyr[0]
        geom = feat.GetGeometryRef()
        mx,my=geom.GetX(), geom.GetY()  #coord in map units

        #Convert from map to pixel coordinates.
        #Only works for geotransforms with no rotation.
        px = floor((mx - gt[0]) / gt[1]) #x pixel
        py = floor((my - gt[3]) / gt[5]) #y pixel

        intval=rb.ReadAsArray(px,py,1,1)

        values.append(numpy.single(intval[0][0]))
        # print( intval[0] )#intval is a numpy array, length=1 as we only asked for 1 pixel value

        # Close Raster
        rb = None  # dereference band to avoid gotcha described previously
        src_ds = None  # save, close

    ## CLOSE VECTOR
    source = None

    print(days)
    print(values)

    # https://matplotlib.org/stable/tutorials/introductory/pyplot.html
    plt.plot(days, values)
    plt.ylabel('Humedad')
    plt.xlabel('Día de Octubre')
    plt.show()


    return 0


if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))


