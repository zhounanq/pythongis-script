# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import geopandas as gpd


def calculate_geometry_attribute_geopandas(input_shp, output_shp, geometry_property, coordinate_system=None):
    """
    Calculate geometry attributes for a shapefile using geopandas.

    AREA—An attribute will be added to store the area of each polygon feature.
    PERIMETER_LENGTH—An attribute will be added to store the length of the perimeter or border of each polygon feature.

    Parameters
    ----------
    input_shp : str
        The input shapefile.
    output_shp : str
        The output shapefile.
    geometry_property : list
        A list of geometry properties to calculate.
        Each element in the list is a list of two strings.
        The first string is the name of the geometry field.
        The second string is the name of the geometry property.
        The default value is [["area", "AREA"], ["length", "PERIMETER_LENGTH"]].
    coordinate_system : str like 'epsg:9822'
        The coordinate system in which the coordinates, length, and area will be calculated, in EPSG code.
        The coordinate system of the input features is used by default.
    """
    # Read the input shapefile
    gdf = gpd.read_file(input_shp)

    gdf_copy = gdf.copy()
    if coordinate_system:
        gdf_copy = gdf_copy.to_crs({'init': coordinate_system})

    # Calculate the geometry properties, and store in the new or existing fields
    for prop in geometry_property:
        if prop[1] == "AREA":
            gdf_copy[prop[0]] = gdf_copy['geometry'].area
        elif prop[1] == "PERIMETER_LENGTH":
            gdf_copy[prop[0]] = gdf_copy['geometry'].length

    # Write the output shapefile
    gdf_copy.to_file(output_shp)

    return output_shp
