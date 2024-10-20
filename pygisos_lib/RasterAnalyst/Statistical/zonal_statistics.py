# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""

import geopandas as gpd
from rasterstats import zonal_stats


"""
从rasterstats库的源码来看，其基本上是模仿了ArcGIS的分区统计工具。因此相对于QGIS，其实现的并不好。

raster_stats(vectors, raster, layer_num=0, band_num=1, nodata_value=None, 
             global_src_extent=False, categorical=False, stats=None, 
             copy_properties=False, all_touched=False)
"""


def zonal_statistics_rasterstats(input_shp, input_raster, output_shp, stats=["mean", "min", "max", "median"]):
    """
    Summarizes the values of a raster within the zones of another dataset.

    Parameters:
    input_shp (str): The path to the input shapefile.
    input_raster (str): The path to the input raster file.
    output_shp (str): The path to the output shapefile.
    stats (list): A list of statistics to calculate. Optional values include 'mean', 'min', 'max', 'median', 'sum', 'std', etc.

    Returns:
    result (GeoDataFrame): The GeoDataFrame containing the calculated statistics.
    """

    # Read the shapefile
    shapes = gpd.read_file(input_shp)

    # Calculate zonal statistics
    results = zonal_stats(shapes, input_raster, stats=stats, geojson_out=True)

    # Append the statistics to the GeoDataFrame
    for stat in stats:
        shapes[stat] = [result['properties'][stat] for result in results]

    # Save the result to a new shapefile
    shapes.to_file(output_shp)

    return shapes


# TODO: 如果有时间，还是自己实现zonal statistics, 参考QGIS的实现方式提高精度，是否可以调用gdal库提升计算效率？
