# -*- utf-8 -*-
"""
pyqgis

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import os
from qgis.core import (QgsApplication, QgsProcessingContext, QgsProcessingFeedback, QgsProcessingException)
import processing


# NOTE: QGIS本身就有自增ID的功能，可以直接调用
def add_autoincrement_field(input_file, output_file, field_name='id'):
    """
    添加自增字段
    :param input_file: 输入矢量文件路径
    :param output_file: 输出路径
    :param field_name: 字段名称
    :return: 输出文件路径
    """
    # Initialize the feedback
    feedback = QgsProcessingFeedback()
    # Create the processing context
    context = QgsProcessingContext()
    context.setFeedback(feedback)

    # 这里算法主要采用console方式，因此这里仅判断文件存在与否即可。
    # 并不判断是否为shp文件，或者文件是否有效
    if not os.path.exists(input_file):
        raise ValueError(f"Can't load: {input_file}")
    # Load the input vector layer (shapefile)
    # input_layer = QgsVectorLayer(input_path, "Input Layer", "ogr")
    # if not input_layer.isValid():
    #     raise ValueError(f"Can't load: {input_path}")

    # Run the algorithm
    algo = "native:addautoincrementalfield"
    parameters = {
        'INPUT': input_file,
        'FIELD_NAME': field_name,
        'START': 1,
        'GROUP_FIELDS': [],
        'SORT_EXPRESSION': '',
        'SORT_ASCENDING': True,
        'OUTPUT': output_file
    }

    try:
        result = processing.run(algo, parameters, context=context, feedback=feedback)
        return result['OUTPUT']
    except (QgsProcessingException, Exception) as e:
        print(f"Exception: {e}")
        return None
