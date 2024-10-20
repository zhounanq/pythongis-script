# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import os
import math
from osgeo import gdal
import rasterio

from util_lib import file_extension_by_gdal_driver

gdal.UseExceptions()


def split_raster_to_tile_gdal(input_raster, output_folder, tile_size, overlap_size=0, output_format='GTiff'):
    """
    Split raster to tiles

    Parameters
    ----------
    input_raster: str
        The input raster file.
    output_folder: str
        The output directory.
    tile_size: int
        The tile size.
    overlap_size: int, optional
        The overlap size. Default is 0.
    output_format: str, optional
        The output format. Default is 'GTiff'.
    """

    # 打开栅格数据集
    src_ds = gdal.Open(input_raster)
    if src_ds is None:
        raise IOError('Cannot open raster file: {}'.format(input_raster))

    # 获取栅格数据集的基本信息
    src_geotransform = src_ds.GetGeoTransform()
    src_proj         = src_ds.GetProjection()
    src_nodata       = src_ds.GetRasterBand(1).GetNoDataValue()
    src_data_type    = src_ds.GetRasterBand(1).DataType
    src_width        = src_ds.RasterXSize
    src_height       = src_ds.RasterYSize
    src_band_count   = src_ds.RasterCount

    # 计算输出的行列数
    tile_width  = tile_size
    tile_height = tile_size
    overlap     = overlap_size
    n_cols      = math.ceil((src_width - overlap) / (tile_width - overlap))
    n_rows      = math.ceil((src_height - overlap) / (tile_height - overlap))

    image_name = os.path.basename(input_raster).split('.')[0]
    out_ext = file_extension_by_gdal_driver(output_format)
    raster_driver = gdal.GetDriverByName(output_format)

    # 逐个切割
    for i in range(n_rows):
        for j in range(n_cols):
            # 计算切割窗口
            x_off  = j * (tile_width - overlap)
            y_off  = i * (tile_height - overlap)
            x_size = min(tile_width, src_width - x_off)
            y_size = min(tile_height, src_height - y_off)

            # 读取数据
            tile_data = src_ds.ReadAsArray(x_off, y_off, x_size, y_size)

            # 创建输出栅格数据集
            out_raster = os.path.join(output_folder, f'{image_name}_{i}_{j}.{out_ext}')
            out_ds = raster_driver.Create(out_raster, x_size, y_size, src_band_count, src_data_type)
            out_ds.SetGeoTransform((src_geotransform[0] + x_off * src_geotransform[1], src_geotransform[1], 0, src_geotransform[3] + y_off * src_geotransform[5], 0, src_geotransform[5]))
            out_ds.SetProjection(src_proj)
            out_ds.WriteArray(tile_data)

            # 设置NoData值
            out_ds.GetRasterBand(1).SetNoDataValue(src_nodata)
            out_ds = None
        # for
    # for

    src_ds = None

    return output_folder


def split_raster_to_tile_gdal_translate(input_raster, output_folder, tile_size, overlap_size=0, output_format='GTiff'):
    """
    Split raster to tiles using gdal_translate

    Parameters
    ----------
    input_raster: str
        The input raster file.
    output_folder: str
        The output directory.
    tile_size: int
        The tile size.
    overlap_size: int, optional
        The overlap size. Default is 0.
    output_format: str, optional
        The output format. Default is 'GTiff'.
    """

    # 打开栅格数据集
    src_ds = gdal.Open(input_raster)
    if src_ds is None:
        raise IOError('Cannot open raster file: {}'.format(input_raster))

    # 获取栅格数据集的基本信息.
    src_width = src_ds.RasterXSize
    src_height = src_ds.RasterYSize

    # 计算输出的行列数
    tile_width  = tile_size
    tile_height = tile_size
    overlap     = overlap_size
    n_cols      = math.ceil((src_width - overlap) / (tile_width - overlap))
    n_rows      = math.ceil((src_height - overlap) / (tile_height - overlap))

    # 逐个切割
    image_name = os.path.basename(input_raster).split('.')[0]
    out_ext = file_extension_by_gdal_driver(output_format)
    for i in range(n_rows):
        for j in range(n_cols):
            # 计算切割窗口
            x_off = j * (tile_width - overlap)
            y_off = i * (tile_height - overlap)
            x_size = min(tile_width, src_width - x_off)
            y_size = min(tile_height, src_height - y_off)

            # 创建输出栅格数据集
            out_raster = os.path.join(output_folder, f'{image_name}_{i}_{j}.{out_ext}')
            gdal.Translate(out_raster, src_ds, srcWin=[x_off, y_off, x_size, y_size])
        # for
    # for
    src_ds = None

    return output_folder


def split_raster_to_tile_rasterio(input_raster, output_folder, tile_size, overlap_size=0, output_format='GTiff'):
    """
    Split raster to tiles using rasterio

    Parameters
    ----------
    input_raster: str
        The input raster file.
    output_folder: str
        The output directory.
    tile_size: int
        The tile size.
    overlap_size: int, optional
        The overlap size. Default is 0.
    output_format: str, optional
        The output format. Default is 'GTiff'.
    """
    # 打开栅格数据集
    src_ds = rasterio.open(input_raster)
    if src_ds is None:
        raise IOError('Cannot open raster file: {}'.format(input_raster))

    # 获取栅格数据集的基本信息
    src_width = src_ds.width
    src_height = src_ds.height

    # 计算输出的行列数
    tile_width = tile_size
    tile_height = tile_size
    overlap = overlap_size
    # include the marginal tiles
    n_cols = math.ceil((src_width - overlap) / (tile_width - overlap))
    n_rows = math.ceil((src_height - overlap) / (tile_height - overlap))
    # drop out the marginal tiles
    # n_cols = math.floor((src_width - overlap) / (tile_width - overlap))
    # n_rows = math.floor((src_height - overlap) / (tile_height - overlap))

    # 逐个切割
    image_name = os.path.basename(input_raster).split('.')[0]
    out_ext = file_extension_by_gdal_driver(output_format)
    for i in range(n_rows):
        for j in range(n_cols):
            # 计算切割窗口
            x_off  = j * (tile_width - overlap)
            y_off  = i * (tile_height - overlap)
            x_size = min(tile_width, src_width - x_off)
            y_size = min(tile_height, src_height - y_off)

            # Define the window coordinates for each tile (with overlapping)
            win = rasterio.windows.Window(x_off, y_off, x_size, y_size)
            # Read the data from the window and create a new dataset for each tile
            data = src_ds.read(window=win)
            # build data meta info.
            out_meta = src_ds.meta.copy()
            out_meta['width'] = win.width
            out_meta['height'] = win.height
            # Adjust geo-transform based on window position
            adjusted_geo_transform = list(src_ds.transform)
            adjusted_geo_transform[2] += x_off * src_ds.transform.a  # Adjust X coordinate of top-left corner
            adjusted_geo_transform[5] += y_off * src_ds.transform.e  # Adjust Y coordinate of top-left corner
            out_meta['transform'] = tuple(adjusted_geo_transform)

            out_raster = os.path.join(output_folder, f'{image_name}_{i}_{j}.{out_ext}')
            with rasterio.open(out_raster, 'w', **out_meta) as dest:
                dest.write(data)
        # for
    # for
    src_ds.close()

    return output_folder
