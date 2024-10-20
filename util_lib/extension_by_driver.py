# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""


def file_extension_by_gdal_driver(driver_name):
    # 手动映射 driver_name 到常见文件扩展名
    driver_extension_map = {
        'GTiff'         : 'tif',
        'HFA'           : 'img',
        'PNG'           : 'png',
        'JPEG'          : 'jpg',
        'MEM'           : 'mem',     # 内存栅格
        'BMP'           : 'bmp',
        'AAIGrid'       : 'asc',     # ASCII Grid
        'netCDF'        : 'nc',
        'JP2OpenJPEG'   : 'jp2',
        'ENVI'          : 'hdr',
        'ECW'           : 'ecw',
        'MrSID'         : 'sid',
        'EHdr'          : 'bil',     # ESRI BIL
        'GeoJSON'       : 'geojson',
        'ESRI Shapefile': 'shp',
        'GPKG'          : 'gpkg',    # GeoPackage
        'KML'           : 'kml',
        'VRT'           : 'vrt'
    }
    # 获取指定 driver_name 的扩展名
    return driver_extension_map.get(driver_name, 'Unknown format')
