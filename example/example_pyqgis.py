# -*- coding: utf-8 -*-
"""
pyqgis

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import pyqgis_lib
from pyqgis_lib import qgis_manager


def main_example():

    try:
        # 使用缓冲区算法
        buffer_algo = qgis_manager.get_algorithm('buffer')
        buffer_output = buffer_algo.run("../data/line.shp", 500, "../data/line_output.shp")
        print(f"Buffer output: {buffer_output}")
    finally:
        # QGIS 资源会在程序退出时自动释放
        pass


if __name__ == "__main__":
    main_example()
