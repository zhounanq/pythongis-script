# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import os
import rasterio


def merge_tile_to_raster_rasterio(input_folder, output_raster, input_extension='.tif'):
    """
    Merge tiles to raster using rasterio

    Parameters
    ----------
    input_folder: str
        The folder of tiles.
    output_raster: str
        The output raster.
    input_extension: str, optional
        The extension of input tiles. Default is '.tif'.
    """
    # Get all the tile files
    tile_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(input_extension)]

    # Read metadata of first tile for reference
    with rasterio.open(tile_files[0]) as src:
        meta = src.meta.copy()

    # Create an array to store all tile data
    mosaic_data = []
    for file in tile_files:
        # Read each tile and append it to the mosaic_data array
        src = rasterio.open(file)
        mosaic_data.append(src)

    # Merge the tiles into a single mosaic dataset using the merge function from rasterio
    merged_data, merged_transform = rasterio.merge.merge(mosaic_data)

    # Update metadata with new dimensions and transform from merged dataset
    meta.update({
        'height': merged_data.shape[1],
        'width': merged_data.shape[2],
        'transform': merged_transform,
     })

    # Write out the final merged dataset to a new file
    with rasterio.open(output_raster, 'w', **meta) as dest:
        dest.write(merged_data)

    # return
    return output_raster
