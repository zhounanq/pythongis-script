# -*- utf-8 -*-
"""
pyqgis

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import os
from qgis.core import (QgsApplication, QgsProcessingContext, QgsProcessingFeedback, QgsProcessingException)
import processing


# To see the help, just run the following code by providing the algorithm id
# processing.algorithmHelp("native:buffer")


def run(input_file, output_file, distance):
    """
    缓冲区算法
    :param input_file: 输入矢量文件路径
    :param output_file: 输出路径
    :param distance: 缓冲距离
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
    algo = "native:buffer"
    parameters = {
        'INPUT': input_file,
        'DISTANCE': distance,
        'OUTPUT': output_file
    }

    try:
        result = processing.run(algo, parameters, context=context, feedback=feedback)
        return result['OUTPUT']
        # result = QgsApplication.processingRegistry().algorithmById(algo).run(parameters, context, feedback)
        # return result[0]['OUTPUT']
    except (QgsProcessingException, Exception) as e:
        print(f"Exception: {e}")
        return None
