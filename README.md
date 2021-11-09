# Selper
## Example scripts for the Selper 2021 training course  

These are example scripts for extracting values from a single raster or a stack of align rasters.

The examples where tested with python 3.9.6 and GDAL 3.2.2

points_py3.py gives the values at fixed point coordinates over the test raster available through ["9. Provincias de la Región Pampeana Argentina"](https://catalogos.conae.gov.ar/catalogo/catalogosatsaocomadel.html).

points_value_py3.py gives the values for a similar stack of images.

value_tool.py allows to enter the coordinates through the command line and plots a time series of the values at the given point using matplotlib.

