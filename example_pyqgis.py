# -*- coding: utf-8 -*-
"""
pyqgis

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import sys


def main_example():

    try:
        # 使用缓冲区算法
        from pyqgis_lib import buffer
        buffer_output = buffer("./data/line.shp", "./data/line_output.shp", 500)
        print(f"Buffer output: {buffer_output}")
    finally:
        # QGIS 资源会在程序退出时自动释放
        pass


if __name__ == "__main__":
    main_example()
