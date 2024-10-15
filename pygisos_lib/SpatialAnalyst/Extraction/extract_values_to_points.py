# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import geopandas as gpd
import rasterio


def extract_raster_values_to_points(input_raster, input_shp, output_shp, bands=None):
    """
    Extract values from multiple bands of a raster to points.
    The raster values will be stored in new fields named 'band_1', 'band_2', etc., in the output shapefile.

    Parameters
    ----------
    input_raster: str
        The input raster file.
    input_shp: str
        The input points shapefile.
    output_shp: str
        The output shapefile.
    bands: list
        A list of band indices to extract values from.
        If empty, values from all bands will be extracted.
    """
    # Load the points shapefile
    if bands is None:
        bands = []
    points = gpd.read_file(input_shp)

    # Load the raster file
    with rasterio.open(input_raster) as src:
        # Extract the affine transformation and data of the raster
        affine = src.transform
        raster_data = src.read()  # Read all bands of the raster

        # Prepare a list to save the raster values for each point
        values = {f'band_{band}': [] for band in bands} if bands else {f'band_{i + 1}': [] for i in range(src.count)}

        # Iterate over each point
        for geom in points.geometry:
            # Get the coordinates of the point
            x, y = geom.x, geom.y
            # Convert the coordinates to raster indices (row, col)
            row, col = ~affine * (x, y)
            row, col = int(row), int(col)

            # Check if the indices are within the raster extent
            if 0 <= row < raster_data.shape[1] and 0 <= col < raster_data.shape[2]:
                for band in bands:
                    value = raster_data[band - 1, row, col]  # Get the raster value
                    values[f'band_{band}'].append(value)
            else:
                for band in bands:
                    values[f'band_{band}'].append(None)  # Assign None if out of extent

    # Add the extracted raster values as new columns to the vector data
    for band, value_list in values.items():
        points[band] = value_list

    # Save the result as a new shapefile
    points.to_file(output_shp)

    return output_shp
