# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import numpy as np
import rasterio
from osgeo import gdal

gdal.UseExceptions()


def scale_16to8_percentile(band_array, nodata_value=None, lower_percentile=0.1, upper_percentile=99.9):
    """
    Scale 16-bit raster to 8-bit raster with percentile stretch

    Parameters
    ----------
    band_array: numpy.ndarray
        The input band array.
    nodata_value: int or float, optional
        The NoData value. Default is None.
    lower_percentile: float, optional
        The lower percentile. Default is 0.1.
    upper_percentile: float, optional
        The upper percentile. Default is 99.9.

    Returns
    -------
    numpy.ndarray
        The 8-bit band array.
    """
    if nodata_value is not None:
        # 获取NoData值的掩膜
        mask = (band_array == nodata_value)

        # 对非NoData进行百分位拉伸
        valid_data = band_array[~mask]
        if len(valid_data) == 0:
            return np.full_like(band_array, 0, dtype=np.uint8)

        min_val = np.percentile(valid_data, lower_percentile)
        max_val = np.percentile(valid_data, upper_percentile)
        band_8bit = np.clip((band_array - min_val) / (max_val - min_val) * 255, 0, 255).astype(np.uint8)

        # 将NoData区域的值恢复为黑色
        band_8bit[mask] = 0
    else:
        # 如果没有NoData值，直接进行百分位拉伸
        min_val = np.percentile(band_array, lower_percentile)
        max_val = np.percentile(band_array, upper_percentile)
        band_8bit = np.clip((band_array - min_val) / (max_val - min_val) * 255, 0, 255).astype(np.uint8)

    return band_8bit


def scale_raster_16to8_percentile_gdal(input_raster, output_raster, lower_percentile=0.1, upper_percentile=99.9, output_format='GTiff'):
    """
    Scale 16-bit raster to 8-bit raster with percentile stretch using GDAL

    Parameters
    ----------
    input_raster: str
        The input raster file.
    output_raster: str
        The output raster file.
    lower_percentile: float, optional
        The lower percentile. Default is 0.1.
    upper_percentile: float, optional
        The upper percentile. Default is 99.9.
    output_format: str, optional
        The output raster format. Default is 'GTiff'.
    """

    in_dataset = gdal.Open(input_raster)

    # check if the dataset is opened successfully, if not, throw an exception
    if in_dataset is None:
        raise Exception(f"Can not open raster file {input_raster}")
    # check if the data type is uint16, if not, throw an exception
    if in_dataset.GetRasterBand(1).DataType != gdal.GDT_UInt16:
        raise Exception(f"Data type of raster file {input_raster} is not UInt16")

    # get the number of bands, xsize and ysize of the input raster
    num_bands = in_dataset.RasterCount
    xsize = in_dataset.RasterXSize
    ysize = in_dataset.RasterYSize

    # create the output raster dataset
    raster_driver = gdal.GetDriverByName(output_format)
    out_dataset = raster_driver.Create(output_raster, xsize, ysize, num_bands, gdal.GDT_Byte)
    out_dataset.SetGeoTransform(in_dataset.GetGeoTransform())
    out_dataset.SetProjection(in_dataset.GetProjection())

    # scale for each band.
    for band_idx in range(1, num_bands + 1):
        in_band = in_dataset.GetRasterBand(band_idx)

        nodata_value = in_band.GetNoDataValue()
        band_array = in_band.ReadAsArray()

        band_8bit = scale_16to8_percentile(band_array, nodata_value, lower_percentile, upper_percentile)
        out_band = out_dataset.GetRasterBand(band_idx)
        out_band.WriteArray(band_8bit)

        # 设置输出波段的NoData值
        if nodata_value is not None:
            out_band.SetNoDataValue(nodata_value)
    # for

    in_dataset = None
    out_dataset = None

    return output_raster


def scale_raster_16to8bit_percentile_rasterio(input_raster, output_raster, lower_percentile=0.1, upper_percentile=99.9):
    """
    Scale 16-bit raster to 8-bit raster with percentile stretch using Rasterio

    Parameters
    ----------
    input_raster: str
        The input raster file.
    output_raster: str
        The output raster file.
    lower_percentile: float, optional
        The lower percentile. Default is 0.1.
    upper_percentile: float, optional
        The upper percentile. Default is 99.9.
    """
    with rasterio.open(input_raster) as src:
        profile = src.profile
        profile.update(dtype=rasterio.uint8, count=src.count)
        with rasterio.open(output_raster, 'w', **profile) as dst:
            for i in range(1, src.count + 1):
                band_array = src.read(i)
                band_8bit = scale_16to8_percentile(band_array, src.nodata, lower_percentile, upper_percentile)
                dst.write(band_8bit, i)
        # with
    # with

    return output_raster
