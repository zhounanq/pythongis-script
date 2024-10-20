# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""


"""
from qgis.analysis import QgsZonalStatistics

QGIS first makes an initial pass, checking to see if the center of each raster cell is within the polygon. 
If fewer than two cell centers are within the polygon, 
it performs a vector-based intersection for all intersecting cells, 
whether their center is within the polygon or not, 
and computes a weight that is the fraction of each cell that is covered by the polygon. 
If two or more cell centers are within the polygon, 
those cells are assigned a weight of 1 and all other cells are assigned a weight of 0.

相对于ArcGIS，QGIS的分区统计工具，做的更好。

__init__(polygonLayer: QgsVectorLayer | None, rasterLayer: QgsRasterLayer | None, attributePrefix: str | None = '', 
         rasterBand: int = 1, stats: Qgis.ZonalStatistics | Qgis.ZonalStatistic = Qgis.ZonalStatistic.Default)
"""
