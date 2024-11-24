# -*- coding: utf-8 -*-
"""
pyqgis

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import sys
import importlib

from qgis.core import (QgsApplication, QgsProcessingFeedback)
from qgis.analysis import QgsNativeAlgorithms

# Prepare the environment
# Append the path where processing plugin can be found (abs path)
plugins_path = r"D:/Program Files/QGIS 3.34.8/apps/qgis-ltr/python/plugins"
sys.path.append(plugins_path)


class QGISAlgorithmManager:
    """QGIS 算法管理类（单例模式）"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(QGISAlgorithmManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, qgis_path="./qgis/bin"):
        """
        初始化 QGIS 环境并加载指定算法模块。
        :param qgis_path: QGIS 安装路径
        """
        if not hasattr(self, "_initialized"):  # 确保 init 只调用一次
            self.qgis_path = qgis_path
            self.qgis_app = None
            self.algorithms = {}
            self._init_qgis()
            # self._load_algorithms() # 采用import模式，不需要手动加载
            self._initialized = True  # 标记为已初始化

    def _init_qgis(self):
        """初始化 QGIS 应用程序。"""
        # 设置 QGIS 环境
        sys.path.append(self.qgis_path)
        self.qgis_app = QgsApplication([], False)
        self.qgis_app.setPrefixPath(self.qgis_path, True)
        self.qgis_app.initQgis()

        # initialize processing algorithms
        # 我看到有很多教程：把这两句初始化放到文件开头。但这直接导致生成shp文件没有.prj文件。[2024-11-24]
        import processing
        processing.core.Processing.Processing.initialize()

        # Register the native algorithms provider, so that QGIS can find them.
        self.qgis_app.processingRegistry().addProvider(QgsNativeAlgorithms())
        # You can check all the algorithms you have access to by running the following code.
        algorithms = dict()
        for alg in self.qgis_app.processingRegistry().algorithms():
            algorithms[alg.displayName()] = alg.id()
        print(f'\nQGIS Algorithm: {algorithms}')

        print('\n============================================================')
        print("============ QGIS Environment Setup Completed! =============")
        print('============================================================\n')

    def _load_algorithms(self):
        """
        手动加载指定的算法模块。
        """
        modules_to_load = [
            # GeoAnalytics
            "pyqgis_lib.GeoAnalytics.Proximity.buffer",   # 缓冲区算法

            # RasterAnalysis
            "pyqgis_lib.RasterAnalyst.Statistical.zonal_statistics",  # 分区统计算法

            # TODO: 添加更多算法模块
        ]
        for module_path in modules_to_load:
            module = importlib.import_module(module_path)
            module_name = module_path.split(".")[-1]
            self.algorithms[module_name] = module

        print('\n============================================================')
        print(f"Available Algorithms: \n {list(self.algorithms.keys())}")
        print('============================================================\n')

    def get_algorithm(self, name):
        """
        获取指定算法模块。
        :param name: 算法模块名（文件名，无扩展名）。
        :return: 算法模块。
        """
        if name in self.algorithms:
            return self.algorithms[name]
        else:
            print(f"====== Warning: Algorithm '{name}' Unavailable! ======")
            return None

    def __del__(self):
        """释放 QGIS 资源。"""
        if self.qgis_app:
            self.qgis_app.exitQgis()
        print('\n============================================================')
        print("=============== QGIS Environment Cleaned Up! ===============")
        print('============================================================\n')


# Singleton instance, ensuring only one instance
# placed at the module level
qgis_path = r"D:/Program Files/QGIS 3.34.8/bin"
qgis_manager = QGISAlgorithmManager(qgis_path)


"""
把PYQGIS封装函数暴露出去也有两种方式：
1. 使用import语句。这样其他需要调用的地方，只需要import即可；而QGISAlgorithmManager的实例是隐藏的，只是为了初始化QGIS环境。
    from pyqgis_lib import buffer
    buffer_output = buffer("./data/line.shp", "./data/line_output.shp", 500)
    print(f"Buffer output: {buffer_output}")

2. 正如上面的代码，自己主动利用importlib.import_module()方法加载模块，并把模块对象保存在字典中；然后通过get_algorithm字典来调用。
   这样其他需要调用的地方，需要获取到QGISAlgorithmManager的实例。这其实并不方便。
    from pyqgis_lib import qgis_manager
    buffer_algo = qgis_manager.get_algorithm('buffer')
    buffer_output = buffer_algo.run("./data/line.shp", "./data/line_output.shp", 500)
    print(f"Buffer output: {buffer_output}")

目前我倾向于第一种方式。
"""
from .DataManagement import dissolve

from .GeoAnalytics import buffer

from .RasterAnalyst import zonal_statistics

"""
调用PYQGIS算法的两种方式：
1. 使用processing.run()方法
2. 使用QgsApplication.processingRegistry().algorithmById(algo).run()方法

这两种方法的区别在于：
1. processing.run()方法返回一个字典，其中包含输出参数的键值对。
2. QgsApplication.processingRegistry().algorithmById(algo).run()方法返回一个列表，其中包含输出参数的键值对。

更深层次的区别是：
1. processing.run()方法是QgsApplication.processingRegistry().algorithmById(algo).run()方法的封装。
2. QgsApplication.processingRegistry().algorithmById(algo).run()方法是直接调用QGIS的算法。

如果您需要快速调用现有算法，并以较少的代码实现功能，推荐使用 `processing.run`。
如果您需要深入控制算法的执行流程（例如调试、扩展功能、或自定义上下文），可以选择使用 `algorithmById().run

"""