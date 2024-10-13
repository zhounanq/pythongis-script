# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import geopandas as gpd


def add_increment_field_geopandas(input_shp, output_shp, field_name='increment'):
    """
    Add an increment field to a shapefile.
    The increment field is used to store the increment values starting from 1.
    The increment field will be created if it does not exist.
    Otherwise, the existing increment field will be overwritten.

    Parameters
    ----------
    input_shp: str
        The input shapefile.
    output_shp: str
        The output shapefile.
    field_name: str
        The name of the increment field. Default is 'increment'.
    """
    if field_name == '':
        raise ValueError("Field name cannot be empty.")
    if field_name in ['geometry']:
        raise ValueError(f'Field name \'{field_name}\' is reserved.')

    # Read the input shapefile
    gdf = gpd.read_file(input_shp)

    # Add an increment field if it does not exist
    # Otherwise, overwrite the existing increment field
    if field_name not in gdf.columns:
        gdf[field_name] = range(1, len(gdf) + 1)
    else:
        gdf[field_name] = range(1, len(gdf) + 1)

    # Write the output shapefile
    gdf.to_file(output_shp)

    return output_shp

