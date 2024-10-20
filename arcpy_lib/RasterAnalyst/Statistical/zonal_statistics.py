# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""


"""
https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/zonal-statistics.htm

ArcGIS：分区统计时，如果输入为矢量的feature，直接内部转换为栅格。
If the zone input is a feature dataset, a vector-to-raster conversion will be internally applied to it
当单个要素的面积小于或者接近于栅格的cell时，可能会不展示出来。
If the areas of single features are similar to or smaller than the area of single cells in the value raster, 
in the feature-to-raster conversion some of these zones may not be represented.
所以：ArcGIS的分区统计工具，做的并不好。

ZonalStatistics(in_zone_data, zone_field, in_value_raster, 
    {statistics_type}, {ignore_nodata}, {process_as_multidimensional}, {percentile_value}, 
    {percentile_interpolation_type}, {circular_calculation}, {circular_wrap_value})
"""
