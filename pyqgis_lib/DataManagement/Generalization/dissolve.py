# -*- utf-8 -*-
"""
pyqgis

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import os
from qgis.core import (QgsApplication, QgsVectorLayer, QgsProcessingContext, QgsProcessingFeedback, QgsProcessingException)
import processing


# To see the help, just run the following code by providing the algorithm id
# processing.algorithmHelp("native:buffer")


def run(input_path, output_path, field=None | list):
    """
    融合算法
    :param input_path: 输入矢量文件路径
    :param output_path: 输出路径
    :param field: 融合字段
    :return: 输出文件路径
    """
    # Initialize the feedback
    feedback = QgsProcessingFeedback()
    # Create the processing context
    context = QgsProcessingContext()
    context.setFeedback(feedback)

    # Load the input vector layer (shapefile)
    input_layer = QgsVectorLayer(input_path, "Input Layer", "ogr")
    if not input_layer.isValid():
        raise ValueError(f"Can't load: {input_path}")
    # Check if the layer has the specified field
    if field is not None:
        if isinstance(field, list):
            for f in field:
                if f not in input_layer.fields().names():
                    raise ValueError(f"Field {f} not found in the layer")
        else:
            if field not in input_layer.fields().names():
                raise ValueError(f"Field {field} not found in the layer")
    # 关闭图层
    input_layer = None

    # Run the algorithm
    algo = "native:dissolve"
    parameters = {
        'INPUT': input_path,
        'FIELD': field,
        'OUTPUT': output_path
    }

    try:
        result = processing.run(algo, parameters, context=context, feedback=feedback)
        return result['OUTPUT']
    except (QgsProcessingException, Exception) as e:
        print(f"Exception: {e}")
        return None
