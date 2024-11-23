# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""
from osgeo import gdal, ogr, osr
import rasterio
import geopandas as gpd


def raster_to_polygon_rasterio(input_raster, output_shp):
    """
    Polygonize a raster using rasterio.

    Parameters
    ----------
    input_raster : str
        The input raster.
    output_shp : str
        The output shapefile.
    """
    # Open the input raster
    with rasterio.open(input_raster) as src:
        # Read the raster
        band = src.read(1)

        # Polygonize the raster
        mask = band != src.nodata
        results = ({'properties': {'raster_val': v}, 'geometry': s} for i, (s, v) in enumerate(rasterio.features.shapes(band, mask=mask, transform=src.transform)))

        # Convert results to GeoDataFrame and save as Shapefile
        gdf = gpd.GeoDataFrame.from_features(list(results))
        gdf.to_file(output_shp)

        # # Write the output shapefile
        # with fiona.open(output_shp, 'w', 'ESRI Shapefile', src.crs, src.schema) as dst:
        #     dst.writerecords(results)

    return output_shp


def raster_to_polygon_gdal(input_raster, output_shp, shp_format='ESRI Shapefile'):
    """
    Polygonize a raster using GDAL.

    Parameters
    ----------
    input_raster : str
        The input raster.
    output_shp : str
        The output shapefile.
    shp_format : str
        The format of the output shapefile. Default is 'ESRI Shapefile'.
    """
    # Open the input raster
    src_ds = gdal.Open(input_raster)
    band = src_ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()

    # Create the output shapefile
    dst_ds = ogr.GetDriverByName(shp_format).CreateDataSource(output_shp)
    if dst_ds is None:
        raise ValueError(f"Could not create the output shapefile: {output_shp}")

    # Create the output layer
    srs = osr.SpatialReference()
    srs.ImportFromWkt(src_ds.GetProjection())
    dst_layer = dst_ds.CreateLayer("raster", srs=srs)
    dst_field_name = 'raster_val'
    dst_layer.CreateField(ogr.FieldDefn("raster_val", ogr.OFTInteger))

    # Polygonize the raster
    band_data = band.ReadAsArray()
    mask = band_data != nodata
    gdal.Polygonize(band, mask, dst_layer, dst_field_name, [], callback=None)

    # Close the output shapefile
    dst_ds = None

    return output_shp

