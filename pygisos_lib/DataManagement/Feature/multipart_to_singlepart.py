# -*- coding: utf-8 -*-
"""
***

Author: Zhou Ya'nan
Date: 2021-09-16
"""
import geopandas as gpd
import fiona
from shapely.geometry import shape, mapping
from shapely.ops import unary_union


"""
from QGIS
This algorithm takes a vector layer with multipart geometries and generates a new one in which 
all geometries contain a single part. Features with multipart geometries are divided in 
as many different features as parts the geometry contain, and the same attributes are used for each of them.
"""


def multipart_to_singlepart_shapely(input_shp, output_shp):
    """
    Convert a multipolygon shapefile to a polygon shapefile using shapely.
    """
    # Read the input shapefile
    with fiona.open(input_shp) as source:
        # Create a schema for the output shapefile
        schema = source.schema.copy()
        schema['geometry'] = 'Polygon'

        # Write the output shapefile
        with fiona.open(output_shp, 'w', 'ESRI Shapefile', schema) as output:
            for elem in source:
                # Convert the multipolygon to a polygon
                geom = shape(elem['geometry'])
                if geom.geom_type == 'MultiPolygon':
                    geom = unary_union(geom)
                output.write({
                    'properties': elem['properties'],
                    'geometry': mapping(geom)
                })
            # for
        # with
    # with

    return output_shp


def multipart_to_singlepart_geopandas(input_shp, output_shp):
    """
    Convert a multipolygon shapefile to a polygon shapefile using geopandas.
    """
    # Read the input shapefile
    gdf = gpd.read_file(input_shp)

    # Convert the multipolygons to polygons
    gdf['geometry'] = gdf['geometry'].apply(lambda x: x.convex_hull)

    # Write the output shapefile
    gdf.to_file(output_shp)

    return output_shp



