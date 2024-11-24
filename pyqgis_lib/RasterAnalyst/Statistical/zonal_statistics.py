# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import sys
from qgis.core import (
    QgsApplication, QgsProcessingException,
    QgsProcessingContext, QgsProcessingFeedback,
    QgsVectorLayer, QgsRasterLayer
)
from qgis.analysis import QgsZonalStatistics
import processing


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


def run_app(zonal_path, raster_path, att_prefix='', raster_band=1):
    """
    Zonal statistics。相对于run, run_app实现更为底层，直接调用QgsZonalStatistics，并且操作的也是QGs对象。从封装角度看，run更好。
    :param zonal_path:
    :param raster_path:
    :param att_prefix:
    :param raster_band:
    :return:
    """
    # Initialize the feedback
    feedback = QgsProcessingFeedback()

    # open raster and polygon layers
    polygon_layer = QgsVectorLayer(zonal_path, 'zonal_polygons', "ogr")
    if not polygon_layer.isValid():
        raise ValueError(f"Can't load: {zonal_path}")

    raster_layer = QgsRasterLayer(raster_path, "value_raster")
    if not raster_layer.isValid():
        raise ValueError(f"Can't load: {raster_path}")

    # open editable model
    polygon_layer.startEditing()
    # QgsZonalStatistics (QgsVectorLayer, QgsRasterLayer, QString &attributePrefix="", int rasterBand=1, stats Union)
    zone_stat = QgsZonalStatistics(polygon_layer, raster_layer, att_prefix, raster_band, QgsZonalStatistics.Mean)
    # calculate
    zone_stat.calculateStatistics(feedback)
    # commit
    polygon_layer.commitChanges()

    return zonal_path


def run(zonal_path, raster_path, att_prefix='', raster_band=1, output_path=None, stats=QgsZonalStatistics.Mean):
    """
    Zonal statistics
    :param zonal_path:
    :param raster_path:
    :param att_prefix:
    :param raster_band:
    :param output_path:
    :param stats:
    :return:
    """
    # Initialize the feedback
    feedback = QgsProcessingFeedback()
    # Create the processing context
    context = QgsProcessingContext()
    context.setFeedback(feedback)

    # open raster and polygon layers
    polygon_layer = QgsVectorLayer(zonal_path, 'zonal_polygons', "ogr")
    if not polygon_layer.isValid():
        raise ValueError(f"Can't load: {zonal_path}")
    raster_layer = QgsRasterLayer(raster_path, "value_raster")
    if not raster_layer.isValid():
        raise ValueError(f"Can't load: {raster_path}")

    # Run the algorithm
    algo = "native:zonalstatistics"
    parameters = {
        'INPUT': zonal_path,
        'INPUT_RASTER': raster_path,
        'RASTER_BAND': raster_band,
        'COLUMN_PREFIX': att_prefix,
        'STATISTICS': stats,
        'OUTPUT': output_path
    }

    try:
        result = processing.run(algo, parameters, context=context, feedback=feedback)
        return result['OUTPUT']
        # result = QgsApplication.processingRegistry().algorithmById(algo).run(parameters, context, feedback)
        # return result[0]['OUTPUT']
    except QgsProcessingException as e:
        print(f"Qgs Processing Exception: {e}")
        return None
    except Exception as e:
        print(f"Other Exception: {e}")
        return None
