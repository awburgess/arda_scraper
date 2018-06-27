"""
CLI tool for acquiring church location geojson data from ARDA web app
"""

import json
import argparse
from typing import Dict, List, Union
from pathlib import Path
import logging
import time
from random import randint

import requests
import pandas as pd
import geopandas as gpd
from arcgis2geojson import arcgis2geojson
import geojson

import config

logging.basicConfig(level=logging.INFO)

_COUNTY_FILE = Path(__file__).parent / config.COUNTIES_PATH
_FIPS_FILE = Path(__file__).parent / config.STATE_FIPS_XWALK


def acquire_esri_geojson(url: str) -> Dict[str, Union[int, float, str, None]]:
    """
    Issue get request to the ARDA ESRI server for church locations as json

    Args:
        url (str): ESRI Endpoint with the bounding box already format

    Returns:
        Dictionary representation of ESRI's geojson response
    """
    request = requests.get(url, headers={'user-agent': config.USER_AGENT})
    return request.json()


def convert_esri_to_geojson_features(geojson_dict: Dict[str, Union[int,
                                                                   float,
                                                                   str,
                                                                   None]]) -> List[dict]:
    """
    Take ESRI GeoJSON response as dict and convert to standard GeoJSON features

    Args:
        geojson_dict: ESRI GeoJSON as dict

    Returns:
        Standard GeoJSON as list of features
    """
    features = geojson_dict['features']
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
        urls.append(config.ARDA_ESRI_REST_ENDPOINT.format(xmin=row.minx, ymin=row.miny,
                                                          xmax=row.maxx, ymax=row.maxy))
    return urls


def get_state_fips(state_abbrev: str) -> str:
    """
    Load state to fips crosswalk and look up value

    Args:
        state_abbrev: Two character representation of state

    Returns:
        The FIPS code for the given state
    """
    fips_state_df = pd.read_csv(_FIPS_FILE, dtype={'fips_code': str})
    return fips_state_df[fips_state_df['state_abbrev'] == state_abbrev].iloc[0].fips_code


def create_feature_collection(urls: List[str],
                              state_abbrev: str) -> Dict[str, Union[int, str, float, None]]:
    """
    Create GeoJSON Feature collection from all formatted urls

    Args:
        urls: List of formatted URLs for ESRI ARDA Endpoints
        state_abbrev: Two character state abbreviation

    Returns:
        GeoJSON Feature collection as dict
    """
    all_features = []
    for url in urls:
        esri_geojson = acquire_esri_geojson(url)
        features = convert_esri_to_geojson_features(esri_geojson)
        all_features += [f for f in features if f['properties']['STATE'] == state_abbrev]
        time.sleep(randint(2, 6))

    return geojson.FeatureCollection(all_features)


def main():
    """
    Iterate over bounding boxes, convert each ESRI GeoJSON response,
    and return a GeoJSON feature collection from all responses

    """
    parser = argparse.ArgumentParser(description="Get GeoJSON for all churches from "
                                                 "a given state FIPS from ARDA")
    parser.add_argument('state_abbrev', type=str, help="Needs to be a valid two"
                                                       " character state code")
    parser.add_argument('output_file', type=str, help="File location to write the "
                                                      "output (WILL OVERWRITE)")
    args = parser.parse_args()

    state_abbrev = args.state_abbrev.upper()

    logging.info('Looking up state FIPS code')
    state_fips = get_state_fips(state_abbrev)
    logging.info("State FIPS code is %s" % state_fips)

    logging.info("Acquiring U.S. county bounding boxes")
    bounding_boxes_gdf = get_county_bounding_boxes(state_fips)

    logging.info("Formatting urls for your given state FIPS")
    formatted_urls = create_get_urls(bounding_boxes_gdf)

    logging.info("Acquiring and creating GeoJSON")
    geojson_of_all_responses = create_feature_collection(formatted_urls, state_abbrev)

    logging.info("Serializing GeoJSON")
    with open(args.output_file, 'w') as outfile:
        json.dump(geojson_of_all_responses, outfile)

    logging.info("Run complete")


if __name__ == '__main__':
    main()
