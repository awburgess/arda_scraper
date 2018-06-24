import json
import argparse
from typing import Dict, List, Union
from pathlib import Path
import logging
import time
from random import randint

import config

import requests
import geopandas as gpd
from arcgis2geojson import arcgis2geojson
import geojson

_LOGGER = logging.basicConfig(level=logging.INFO)

_COUNTY_FILE = Path(__file__).parent / config.COUNTIES_PATH


def acquire_esri_geojson(url: str) -> Dict[str, Union[int, float, str, None]]:
    """
    Issue get request to the ARDA ESRI server for church locations as json

    Args:
        url (str): ESRI Endpoint with the bounding box already format

    Returns:
        Dictionary representation of ESRI's geojson response
    """
    r = requests.get(url, headers={'user-agent': config.USER_AGENT})
    return r.json()


def convert_esri_to_geojson_features(geojson: Dict[str, Union[int, float, str, None]]) -> List[dict]:
    """
    Take ESRI GeoJSON response as dict and convert to standard GeoJSON features

    Args:
        geojson: ESRI GeoJSON as dict

    Returns:
        Standard GeoJSON as list of features
    """
    features = geojson['features']
    return [arcgis2geojson(feature) for feature in features]


def get_county_bounding_boxes(state_fips: str) -> gpd.GeoDataFrame:
    """
    Load the IN Counties GeoDataFrame

    Args:
        state_fips:

    Returns:
        GeoDataFrame for Indiana counties

    """
    county_gdf = gpd.read_file(_COUNTY_FILE.as_posix())
    return county_gdf[county_gdf['STATEFP'] == state_fips].bounds


def create_get_urls(county_gdf: gpd.GeoDataFrame) -> List[str]:
    """
    Create a list of urls to issue get requests

    Args:
        county_gdf: GeoDataFrame representing Indiana counties

    Returns:
        List of formatted urls to issue GET requests
    """
    urls = []
    for index, row in county_gdf.iterrows():
        urls.append(config.ARDA_ESRI_REST_ENDPOINT.format(xmin=row.minx, ymin=row.miny, xmax=row.maxx, ymax=row.maxy))
    return urls


def create_feature_collection(urls: List[str]) -> Dict[str, Union[int, str, float, None]]:
    """
    Create GeoJSON Feature collection from all formatted urls

    Args:
        urls: List of formatted URLs for ESRI ARDA Endpoints

    Returns:
        GeoJSON Feature collection as dict
    """
    all_features = []
    for url in urls:
        esri_geojson = acquire_esri_geojson(url)
        features = convert_esri_to_geojson_features(esri_geojson)
        all_features += features
        time.sleep(randint(2, 6))

    return geojson.FeatureCollection(all_features)


def main():
    """
    Iterate over bounding boxes, convert each ESRI GeoJSON response, and return a GeoJSON feature collection from all
    responses

    """
    parser = argparse.ArgumentParser(description="Get GeoJSON for all churches from a given state FIPS from ARDA")
    parser.add_argument('state_fips', type=str, help="Needs to be a valid state FIPS code")
    parser.add_argument('output_file', type=str, help="File location to write the output (WILL OVERWRITE)")
    args = parser.parse_args()

    logging.info("Acquiring U.S. county bounding boxes")
    bounding_boxes_gdf = get_county_bounding_boxes(args.state_fips)

    logging.info("Formatting urls for your given state FIPS")
    formatted_urls = create_get_urls(bounding_boxes_gdf)

    logging.info("Acquiring and creating GeoJSON")
    geojson_of_all_responses = create_feature_collection(formatted_urls)

    logging.info("Serializing GeoJSON")
    with open(args.output_file, 'w') as outfile:
        json.dump(geojson_of_all_responses, outfile)

    logging.info("Run complete")


if __name__ == '__main__':
    main()
