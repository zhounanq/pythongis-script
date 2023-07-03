# -*- coding: utf-8 -*-

"""
Environment settings.
https://pro.arcgis.com/zh-cn/pro-app/latest/tool-reference/environment-settings/an-overview-of-geoprocessing-environment-settings.htm

Author: Zhou Ya'nan
Date: 2021-09-16
"""

import arcpy


# Reset geoprocessing environment settings
arcpy.ResetEnvironments()
# Reset a specific environment setting
arcpy.ClearEnvironment("workspace")


# Set the workspace environment setting
arcpy.env.workspace = "c:/St_Johns/data.gdb"


# Set the workspace, outputCoordinateSystem and geographicTransformations
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984 UTM Zone 30N")
arcpy.env.geographicTransformations = "Arc_1950_To_WGS_1984_5; PSAD_1956_To_WGS_1984_6"


# Set the extent environment using a keyword
arcpy.env.extent = "MAXOF"
# Set the extent environment using the Extent class
arcpy.env.extent = arcpy.Extent(-107.0, 38.0, -104.0, 40.0)
# Set the extent environment using a space-delimited string
arcpy.env.extent = "-107.0 38.0 -104.0 40.0"
# Set the extent environment using a feature class
arcpy.env.extent = "C:/data/StudyArea_perim.shp"
# Set the extent environment using a raster
arcpy.env.extent = "C:/data/StudyArea.tif"

# Set Snap Raster environment
arcpy.env.snapRaster = "C:/data/my_snapraster.tif"


# Set the XY Domain to
#   xmin of -180
#   ymin of -90
#   xmax of 180
#   ymax of 90
arcpy.env.XYDomain = "-180 -90 180 90"
# Set the XYResolution environment to a linear unit
arcpy.env.XYResolution = "20 Meters"
# Set the XYTolerance environment setting
arcpy.env.XYTolerance = 2.5


# Set the resampling method environment to bilinear interpolation
arcpy.env.resamplingMethod = "CUBIC"




